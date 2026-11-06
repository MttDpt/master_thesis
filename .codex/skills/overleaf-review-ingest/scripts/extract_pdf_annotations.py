#!/usr/bin/env python3
"""Extract PDF annotations into a stable JSON review queue."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import pdfplumber
from pypdf import PdfReader


EXCLUDED_SUBTYPES = {"Link", "Widget", "Popup"}


def plain(value: Any) -> str:
    if value is None:
        return ""
    try:
        value = value.get_object()
    except AttributeError:
        pass
    return str(value)


def numbers(value: Any) -> list[float]:
    if value is None:
        return []
    try:
        value = value.get_object()
    except AttributeError:
        pass
    return [float(item) for item in value]


def clipped_text(page: Any, rect: list[float], padding: float) -> str:
    if len(rect) != 4:
        return ""
    x0, y0, x1, y1 = rect
    left = max(0.0, min(x0, x1) - padding)
    right = min(float(page.width), max(x0, x1) + padding)
    top = max(0.0, float(page.height) - max(y0, y1) - padding)
    bottom = min(float(page.height), float(page.height) - min(y0, y1) + padding)
    if left >= right or top >= bottom:
        return ""
    return (page.crop((left, top, right, bottom)).extract_text() or "").strip()


def annotation_id(
    pdf_hash: str,
    page_number: int,
    subtype: str,
    rect: list[float],
    comment: str,
) -> str:
    payload = json.dumps(
        [pdf_hash, page_number, subtype, rect, comment],
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]


def extract(pdf_path: Path, source_revision: str | None) -> dict[str, Any]:
    pdf_bytes = pdf_path.read_bytes()
    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()
    reader = PdfReader(str(pdf_path))
    annotations: list[dict[str, Any]] = []

    with pdfplumber.open(str(pdf_path)) as text_pdf:
        for page_index, pdf_page in enumerate(reader.pages):
            text_page = text_pdf.pages[page_index]
            for annotation_ref in pdf_page.get("/Annots", []):
                annotation = annotation_ref.get_object()
                subtype = plain(annotation.get("/Subtype")).lstrip("/")
                if subtype in EXCLUDED_SUBTYPES:
                    continue
                rect = numbers(annotation.get("/Rect"))
                quad_points = numbers(annotation.get("/QuadPoints"))
                comment = plain(annotation.get("/Contents"))
                item = {
                    "id": annotation_id(
                        pdf_hash, page_index + 1, subtype, rect, comment
                    ),
                    "page": page_index + 1,
                    "type": subtype or "Unknown",
                    "comment": comment,
                    "subject": plain(annotation.get("/Subj")),
                    "author": plain(annotation.get("/T")),
                    "modified": plain(annotation.get("/M")),
                    "rect": rect,
                    "quad_points": quad_points,
                    "selected_text": clipped_text(text_page, rect, 0.0),
                    "nearby_text": clipped_text(text_page, rect, 36.0),
                    "mapping": {
                        "status": "unmapped",
                        "source_file": None,
                        "source_line": None,
                        "confidence": None,
                        "method": None,
                    },
                    "resolution_status": "pending",
                }
                annotations.append(item)

    return {
        "schema_version": 1,
        "pdf": {
            "path": str(pdf_path.resolve()),
            "sha256": pdf_hash,
            "pages": len(reader.pages),
        },
        "source_revision": source_revision,
        "annotations": annotations,
        "summary": {
            "annotation_count": len(annotations),
            "mapped_count": 0,
            "unmapped_count": len(annotations),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-revision")
    args = parser.parse_args()

    if not args.pdf.is_file():
        parser.error(f"PDF not found: {args.pdf}")

    queue = extract(args.pdf, args.source_revision)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Extracted {queue['summary']['annotation_count']} annotations "
        f"to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
