---
name: thesis-router
description: Use when facing uncertain thesis-repo requests to route the
  smallest applicable project skill set or workflow.
---
# Thesis Router

Route thesis-repository requests to the smallest applicable project skill set.

## Invariants

- A standalone skill remains directly routable even when it is not part of an established workflow.
- Established workflows are precedents, not an allowlist.
- For paired Overleaf work, never use computer use or the Overleaf web UI unless the user explicitly requests computer use in the current task; never treat a local limitation as permission to open the browser.
- The router selects skills and order only. The selected skills own execution and safety.

## Routing layers

1. **Standalone capability:** when one skill clearly matches, load only that skill.
2. **Established workflow:** when the request matches a maintained sequence, load the skills in that sequence.
3. **Dynamic composition:** otherwise combine the smallest set whose scopes cover the requested outcome, preserving each skill's boundaries and mandatory companions.

## Lazy domain maps

Read only the map needed for the request; read a second map only when the task genuinely crosses domains.

- [Overleaf workflows](references/overleaf.md)
- [Writing workflows](references/writing.md)
- [Analysis workflows](references/analysis.md)
- [Project workflows](references/project.md)

Use the live skill name and description as the trigger authority. The maps define combinations, handoffs, and established sequences without duplicating full skill instructions.

After repository changes, apply `prj-change-audit` once to the complete task.