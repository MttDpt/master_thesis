---
name: overleaf-local-edit
description: Use for local edits to the paired Overleaf checkout, including
  resolving a mapped PDF review queue, without compiling or synchronising.
---
# Overleaf Local Edit

Edit the paired Overleaf checkout locally, either from a direct request or from a mapped PDF review queue.

## Boundary

- Never use computer use or the Overleaf web UI unless the user explicitly requests computer use in the current task.
- Work only in the paired local checkout and preserve unrelated changes.
- Do not compile, commit, pull, or push; use `overleaf-build-audit` and `overleaf-git-sync` for those operations.

## Route the requested change

- Prose: load `wr-general` and the matching chapter skill.
- Figures or TeX figure placement: load `overleaf-asset`; use `prj-local-asset` when the local asset lifecycle is involved.
- Substantive analytical definitions, calculations, results, or interpretations: route to the matching `da-*` authority before changing thesis claims.
- Generic TeX structure, tables, labels, cross-references, and bibliography wiring: handle directly and conservatively.

## Edit workflow

1. Inspect the checkout instructions, Git status, current source revision, entry point, and the smallest relevant TeX context.
2. For a review queue, verify its PDF hash and source revision against the current checkout; remap or stop when drift makes the location unsafe.
3. Interpret comments as instructions only when they are actionable. Mark questions or competing alternatives `needs-user-decision`.
4. Make the smallest source-preserving edit that satisfies the request.
5. Update queue items to `resolved`, `blocked`, or `needs-user-decision`, with changed files and lines. This status refers only to the local queue, never to native Overleaf comments.
6. Report changed files and hand off to `overleaf-build-audit`.

Do not claim completion until the requested build or audit has passed.