---
name: overleaf-review-ingest
description: Use when annotations in a locally rendered thesis PDF must be
  extracted and mapped to likely TeX source locations without editing.
---
# Overleaf Review Ingest

Create a local review queue from annotations in a locally rendered thesis PDF and map each item to the most likely TeX source location.

## Boundary

- Never use computer use or the Overleaf web UI unless the user explicitly requests computer use in the current task.
- This skill does not read native Overleaf comments and does not edit TeX.
- Require the annotated PDF and identify the matching source revision when possible; report a PDF/source mismatch rather than guessing.

## Extraction

1. Load `pdf:pdf` for PDF inspection and workspace PDF dependencies.
2. Run `scripts/extract_pdf_annotations.py` with the bundled workspace Python:
   `python extract_pdf_annotations.py --pdf <review.pdf> --output <queue.json> --source-revision <git-revision>`.
3. Preserve the PDF SHA-256, page, annotation type, comment, marked or nearby text, rectangle, and stable annotation ID.

## Source mapping

Map each item in this order:

1. SyncTeX reverse lookup when a matching `.synctex.gz` and `synctex` executable are available.
2. Exact or normalised marked-text search in the checked-out TeX sources.
3. Section, caption, label, table, and nearby-text context.

Record `source_file`, one-based `source_line`, method, and confidence `high`, `medium`, or `low`. Leave ambiguous items `unmapped` or `needs-user-decision`; never invent a location.

## Output

Return the queue path, PDF hash, source revision, counts by mapping status, and unresolved items. Keep every item `pending`; `overleaf-local-edit` owns resolution.