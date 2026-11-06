# Master's thesis — final archival project

Private archival repository for Matteo Del Prato's master's thesis on aesthetic ambient information in BMW Panoramic Vision.

| Area | Retained material |
| --- | --- |
| [Thesis](overleaf/examplethesis.tex) | [Final PDF](overleaf/final-thesis.pdf), final Overleaf LaTeX source, required KTH template/runtime and all 34 referenced figures |
| [Study records](context/index.md) | Realised methodology, research questions and preparation definitions |
| [Evidence map](evidence/index.md) | Final supporting evidence for Chapters 3–6 and appendices |
| [Analysis authority](analysis/inference_ch4.md) | Adopted correction families, scoring and reporting limits |
| [Cited sources](references/index.md) | Cited-paper ZIP with Zotero annotations and citation manifests |
| [Selection manifest](provenance/selection.json) | Exact source paths, hashes and retention reasons |
| [Privacy and rights](PRIVACY.md) | Why this repository is private and what requires review before sharing |

The archive starts with fresh Git history. Literature notes, the literature wiki, unused exploratory reports/models/posteriors, cached dependencies, temporary files, previous builds and the original repository's Git history are excluded.

Some selected analyses retain historical `provisional/` or `archive/` path names because the final generators and validation receipts read those exact paths. Only adopted final packages and the predecessor input files/numerical checks they actually use are retained; these directory names do not grant reporting authority to old analyses. The five families in the analysis authority determine current inference.

## Verify

```sh
python3 scripts/verify_archive.py
uv run --with numpy --with pandas --with scipy --with statsmodels --with openpyxl python scripts/verify_results.py
```

These commands read frozen evidence and do not regenerate approved outputs. The original analysis generators and validation receipts are retained for inspection; generation can overwrite their local outputs, so use a disposable clone for reruns. Full confidence-family refitting additionally needs R and its `ordinal` package; the complete 15-member family is retained even though only six question contrasts lead the thesis.

## Build the thesis

From `overleaf/`, use Tectonic with bibliography support:

```sh
tectonic --keep-logs --outdir ../.build examplethesis.tex
```

Create `.build/` first. The final PDF is supplied separately in this repository. The paired Overleaf source was copied unchanged; successful local compilation does not establish hosted Overleaf state.

Raw simulator exports were already unavailable in the source checkout; the retained 72 derived, end-aligned simulator logs and their original provenance hashes are preserved. Quantitative findings retain post-hoc selection, unequal detection windows, incomplete exposure/order effects and single-coder interpretation limitations.
