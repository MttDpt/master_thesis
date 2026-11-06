---
name: prj-change-audit
description: Use after repository changes to reconcile affected references,
  indexes, logs, and skills before finalising.
---
# Change Audit

Run once after repository changes and before the final response. Reconcile only task-owned changes and their direct dependencies; never expand scope or modify unrelated user work.

## 1. Classify impact

Using the pre-change status and final diff, classify the task-owned change set as:

* **No mutation** — no repository files changed.
* **Content-local** — content changed without affecting paths, purpose, routing, ownership, discoverability, or public behavior.
* **Structural** — paths, purpose, canonical sources, ownership, routing, or public behavior changed.
* **Skill-affecting** — a skill or its trigger, dependencies, paths, commands, or routing changed.

Use the highest applicable class.

## 2. Reconcile

### No mutation

Skip reconciliation.

### Content-local

* Update indexes only if they became inaccurate.
* Update existing logs only when the governing workflow requires it.
* Run originating-skill checks and `git diff --check`.

### Structural

* Load `prj-architecture`.
* Repair current references to changed paths, names, routes, or ownership.
* Update only affected indexes, instructions, and existing relevant logs.
* Run scoped Markdown/link checks; use whole-project link auditing only when distant callers may be affected.

### Skill-affecting

* Load `skill-creator`.
* Inspect direct callers, router entries, instructions, and commands referencing the changed skill.
* Validate each changed skill with:

```bash
uv run --with pyyaml python /Users/matteodelprato/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-path>
```

* Audit all skills only when a shared convention, router, template, topology, rename, or deprecation can affect them globally.

## 3. Verify

* Preserve unrelated dirty files.
* Do not create indexes or logs solely for this gate.
* Record at most one log entry per logical task.
* Run required repository-specific checks; report unavailable named checks rather than substituting others.
* Confirm no stale current references, missing required reconciliation, or unintended task-owned edits remain.

## Handoff

Return the impact class, files changed, checks run, and any intentionally skipped reconciliation with its reason.
