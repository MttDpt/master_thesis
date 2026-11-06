# Project routing

## Standalone capabilities

- `prj-architecture`: map or restructure a substantial project area.
- `prj-local-asset`: manage local thesis assets and their inventory.
- `gen-todo`: maintain the stored thesis task list.
- `prj-change-audit`: reconcile task-owned repository changes before final handoff.
- `open-knowledge`: mandatory read/write interface for repository Markdown and managed project skills.

These skills are directly routable and need not belong to a predefined workflow.

## Established workflows

- Structural project change: `prj-architecture → prj-change-audit`.
- Local asset publication to Overleaf: `prj-local-asset → overleaf-asset → overleaf-build-audit`; add `overleaf-git-sync` only when synchronization is requested.
- Any repository mutation: apply `prj-change-audit` once after the complete logical task.

When no established workflow matches, dynamically compose the smallest applicable set from the live skill descriptions.