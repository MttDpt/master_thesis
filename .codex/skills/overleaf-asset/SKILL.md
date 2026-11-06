---
name: overleaf-asset
description: Use for approved asset publication and TeX figure management inside
  the paired local Overleaf checkout.
---
# Overleaf Asset Publication

Publish approved thesis assets and manage their TeX figure placement inside the paired local Overleaf checkout.

## Boundary

- Never use computer use or the Overleaf web UI unless the user explicitly requests computer use in the current task.
- Own asset copying and TeX figure wiring only; `overleaf-build-audit` owns compilation and rendered verification, and `overleaf-git-sync` owns commits and synchronization.
- Use this skill after `prj-local-asset` has accepted and prepared a local source, or for an explicitly authorised direct Overleaf asset change that must later be reconciled locally.

## Workflow

1. Inspect the paired checkout instructions, Git state, matching local asset record, relevant TeX references, and actual entry point. Preserve unrelated changes.
2. Publish only an approved local asset. Mirror its exact approved filename into `figures/`; do not create an untracked Overleaf-only source asset.
3. Before replacing or deleting a figure, confirm that no required TeX reference is lost and state the reconciliation needed in `prj-local-asset`.
4. Keep the checkout lightweight using the smallest visually adequate format and resolution.
5. Edit the smallest clear TeX region. Give each independently discussed image or grouped sequence a factual caption and label; use `\caption[Short title]{Full caption}` when the List of Figures should contain only the title.
6. Hand the changed checkout to `overleaf-build-audit` for compilation and page-level visual QA.
7. Do not stage, commit, pull, or push; use `overleaf-git-sync` only when the user requested synchronization.

## Completion

Report the mirrored filename, TeX references, local reconciliation requirement, and build-audit handoff.