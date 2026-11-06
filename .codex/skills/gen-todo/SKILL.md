---
name: gen-todo
description: Autonomously maintain the user’s stored thesis to-do list by adding requested tasks and crossing out tasks supported by conversation or verified recent work.
---

# To-do list

Use the canonical list at `/Users/matteodelprato/.codex/memories/extensions/ad_hoc/notes/20260916-thesis-todo-list.md`.

## Hard scope boundary

When this skill is invoked, statements about things that need doing are to-do items, not implementation instructions. The only permitted edits are additions, Markdown strikethroughs, or user-authorised `‼️` priority markers within the canonical to-do list above. Do not edit, create, delete, move, inspect for implementation, run checks against, or otherwise modify any project file, Overleaf file, external system, or other local file unless the user gives a separate, explicit instruction to do so.

- Store only user-requested to-dos as bullet points.
- Review the current conversation and relevant work completed in the current day or week whenever the skill is invoked, and update the list autonomously.
- Cross out a task when there is strong evidence that it is complete: an explicit completion or approval, a verified artifact or successful scoped check that fulfils it, or a clear decision that it is no longer worth doing. Do not infer completion from partial progress, discussion alone, or an unrelated change.
- If evidence is ambiguous, leave the task active; do not ask the user merely for confirmation.
- When a task is completed, explicitly crossed out, or agreed to be no longer relevant, cross it out with Markdown `~~...~~`; do not delete it.
- Prefix every resolved item with `✔️` when reporting the list.
- Prefix an unresolved item with `‼️` only when the user explicitly identifies that specific to-do as important. Preserve that marker in the canonical list; never infer importance.
- When returning the full list, always place all unresolved `‼️` items first. Within that flagged group, order items by the latest added-or-modified time, newest first; this recency rule takes precedence over their original list order. Then show unmarked unresolved items, followed by resolved items.
- If the user says a to-do is “not so important”, “least important”, or equivalent, preserve that as a low-priority marker and place it last among unresolved items when returning the list.
- Add new tasks as bullets and preserve the existing order unless the user asks to reorder them.
- Keep the file concise: no status tables, commentary, dates, or extra sections.
- When the user asks to see the list, show unresolved to-dos first, followed by resolved (struck-through) items. Within unresolved items, place explicit important items first, ordinary items next, and explicit low-priority items last; preserve recency order within each group. Within resolved items, order from most recently added or modified to oldest. Show only bullet points unless the user asks for explanation.
