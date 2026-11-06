---
name: overleaf-build-audit
description: Use to compile and audit the paired Overleaf checkout locally,
  inspect diagnostics, and verify rendered PDF output.
---
# Local Thesis Build

Use when a local build is requested or an applied TeX change needs verification. Chat drafts and read-only prose discussion do not require compilation.

1. Inspect the checkout instructions, source revision, compiler configuration, and relevant diff once; preserve unrelated work.
2. Compile once after the coherent edit batch. Check errors, undefined citations/references, duplicate labels, missing files, bibliography failures, and relevant overfull boxes.
3. Inspect affected pages and neighbouring pages where pagination changes. Check changed links, captions, or numbering in the generated PDF when relevant.
4. Repeat only after a repair or when a concrete unresolved diagnostic requires it. Use `overleaf-maintenance-audit` for a requested chapter milestone or whole-thesis audit.
5. Report the command/toolchain, PDF path, pages inspected, and material diagnostics. Local success does not establish hosted Overleaf parity.

## Existing local recipe

The paired checkout is `../overleaf`; the entry point is `examplethesis.tex`. The working bundled executable is:

`/Users/matteodelprato/.codex/plugins/cache/openai-bundled/latex/0.2.7/bin/tectonic`

From that checkout, create the output directory first, then run:

```sh
mkdir -p build/review
/Users/matteodelprato/.codex/plugins/cache/openai-bundled/latex/0.2.7/bin/tectonic --synctex --keep-logs --keep-intermediates --outdir build/review examplethesis.tex
```

Verify the executable and entry point still exist. Load `latex:latex-compile` only if this recipe is unavailable, fails, or the compiler requirements changed; avoid rediscovering the toolchain on every edit.

For PDF text or rendering, use available `pdftotext`/`pdftoppm`; use bundled workspace Python with `pypdf` for structural inspection. Resolve its path through workspace dependencies if needed, rather than assuming system Python has PDF packages. Load `pdf:pdf` when specialised PDF handling is needed.

Use local files only unless the user explicitly requests computer use. Hand source repairs to `overleaf-local-edit`; this skill does not commit or synchronise.
