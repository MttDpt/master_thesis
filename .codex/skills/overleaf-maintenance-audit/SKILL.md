---
name: overleaf-maintenance-audit
description: Use for a requested whole-thesis audit, completed-chapter quality
  gate, or final submission checks; routine edits use overleaf-build-audit.
---
# Whole-Thesis Maintenance Audit

Use for an explicitly requested whole-thesis audit, a completed-chapter quality gate, or final submission preparation. Routine scoped edits use `overleaf-build-audit` and do not invoke this checklist automatically.

Work in the paired local checkout. Use the Overleaf web UI or computer use only when explicitly requested.

For the requested chapter or whole thesis:

- Use a PDF built from the current source revision; load `overleaf-build-audit` if a fresh build is needed.
- Check internal references, citations, URLs/DOIs, and relevant clickable PDF destinations.
- Inspect page composition, figure-only pages, stranded floats, excessive whitespace, and collisions.
- Reconcile used terminology with acronym definitions and the generated acronym list.
- Reconcile current captions, numbering, and ordering with the Lists of Figures and Tables.
- Distinguish source-level checks, rendered evidence, accepted warnings, and unresolved findings.

An audit diagnoses by default. Apply repairs only when requested or already authorised, using `overleaf-local-edit`; rerun affected checks after a repair. Stop when the requested scope has no material unresolved finding. Do not synchronise or publish without authorisation.
