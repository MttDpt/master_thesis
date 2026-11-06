---
name: prj-local-asset
description: Use for local thesis asset intake, lifecycle management, inventory,
  and archiving.
---
# Local Thesis Assets

Manage the local thesis asset tree as its source of truth. This skill owns intake, inspection, naming, promotion, inventory, logging, and archiving under `assets/`; it does not modify the Overleaf checkout.

## Scope

- Intake: `assets/inbox/`
- Publication-ready local sources: `assets/chapter-XX/` or `assets/appendix/`
- Retired local sources: `assets/archive/`
- Canonical local inventory: `assets/index.md`
- Append-only local history: `assets/log.md`

## Local workflow

1. Before changing local assets, inspect `AGENTS.md`, the repository Git state, the asset tree, `assets/index.md`, and `assets/log.md`. Preserve unrelated changes.
2. Receive every new local asset into `assets/inbox/` first. Inspect its filename, format, dimensions, visual content, and provenance; assign a stable descriptive filename.
3. When the user approves local publication, move the asset into its matching `assets/chapter-XX/` folder or `assets/appendix/`, then update the inventory and append the dated lifecycle record to the log.
4. When replacing a local source, archive the superseded asset under `assets/archive/`; keep its provenance and replacement relationship in the inventory and log.
5. For an explicit Overleaf publication request, complete this local preparation first, then hand off the exact approved filename and intended use to [overleaf-asset](../overleaf-asset/SKILL.md). Do not copy assets into the Overleaf checkout from this workflow.
6. For a direct Overleaf addition, replacement, or removal, wait for [overleaf-asset](../overleaf-asset/SKILL.md) to provide the verified mirror and TeX details, then reconcile the local tree, inventory, and log in this workflow.

## Completion

Run a scoped OpenKnowledge audit on changed indexes or logs and `git diff --check -- <changed-paths>` in this repository. Do not stage, commit, or push unless the user explicitly requests it.
