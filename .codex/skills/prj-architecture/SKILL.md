---
name: prj-architecture
description: Use when a project area grows or is restructured
---
# Project Architecture

Use when creating, expanding, or restructuring a substantial project area whose contents are difficult to navigate. Do not use it to add empty documentation scaffolding to small or stable folders.

## Outcome

Keep each substantial area discoverable through a short, accurate hierarchy of indexes, with concise change records where a local history is useful. The repository contract should direct agents to the relevant top-level indexes; each index should direct readers only to the relevant child indexes or documents.

## Before changing architecture

1. Run `git status --short` and preserve unrelated work.
2. Map the target folder, its direct children, and any existing `index.md` or `log.md`.
3. Identify the smallest boundary that needs navigation or change tracking. Do not reorganise, move, delete, or rename existing content unless the user explicitly authorises it.

## Maintain the navigation

- Add or revise an `index.md` when a folder has enough depth, volume, or distinct concerns that a reader needs a map. State the folder's purpose, describe its direct contents, and link to relevant child indexes or key documents.
- Apply the same pattern to deeper child folders only when their contents also need a local map. Do not require indexes in trivial or empty folders.
- Keep directory overviews descriptive. Put workflow order, procedures, and decision rules in the relevant skill or operational document, not in an index.
- Add or revise a `log.md` only when changes to that area need a durable local record. Keep entries dated, factual, and scoped to architecture-relevant changes.
- When a top-level route changes, update the relevant `AGENTS.md` guidance so it points to the appropriate parent index rather than duplicating the full hierarchy.
- Update affected parent indexes and logs in the same change; remove stale links and descriptions.

## Verification and handoff

1. Validate every changed Markdown file through the OpenKnowledge workflow and resolve broken internal links.
2. Run `git diff --check`. Run any project-specific structural check required by the changed area.
3. Report the folders assessed, indexes or logs added or revised, any intentionally deferred areas, and the checks run.

## Guardrails

- Prefer a focused map over a recursive documentation expansion.
- Preserve existing sources of truth and workflow ownership.
- Ask before a structural choice that would materially change content ownership, directory names, or external references.
