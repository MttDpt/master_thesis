# Overleaf routing

Use the paired local checkout. Computer use and the Overleaf web UI require an explicit request in the current task; unavailable native comments, online-only logs, or History labels do not justify a browser fallback.

- Prose edit: `wr-general` + matching chapter skill → `overleaf-local-edit` → `overleaf-build-audit`.
- PDF annotations: `overleaf-review-ingest` to map comments; `overleaf-local-edit` to apply actionable changes; `overleaf-build-audit` to verify.
- Approved asset: `prj-local-asset` when intake/inventory work is needed → `overleaf-asset` → `overleaf-build-audit`.
- Build problem: `overleaf-build-audit` diagnoses; `overleaf-local-edit` repairs; rerun affected checks.
- Requested chapter milestone, whole-thesis audit, or final submission: `overleaf-maintenance-audit`.
- Requested commit or synchronisation: `overleaf-git-sync`.

Read-only discussion and chat drafts need no build. Batch related edits into one build and inspect affected pages; expand only for concrete failures. Do not load the full maintenance checklist for routine changes.

Use approved results directly. New analytical definitions or calculations belong to the relevant `da-*` workflow. Preserve the existing asset inventory and unrelated dirty work.
