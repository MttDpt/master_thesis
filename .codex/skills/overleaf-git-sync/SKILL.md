---
name: overleaf-git-sync
description: Use to inspect or synchronise the paired Overleaf checkout safely
  through Git and maintain Git-based checkpoints.
---
# Overleaf Git Sync

Synchronise the paired local thesis checkout through Git and maintain safe local checkpoints without using the Overleaf web interface.

## Boundary

- Never use computer use or the Overleaf web UI unless the user explicitly requests computer use in the current task.
- Fetching and inspection are read-only. Commit, tag, pull, or push only when the user's request authorises that action.
- Detect remotes and branches from the checkout; never hard-code `master` or `main`.
- Never default to rebase.

## Preflight

1. Inspect checkout instructions, `git status --short --branch`, remotes, upstream, and current revision.
2. Identify the Overleaf remote from its configured URL and identify any normal Git remote that supports branches and tags.
3. Fetch the relevant remote and calculate ahead/behind counts before changing state.
4. Preserve unrelated dirty work. Do not hide it in a broad automatic stash or include it in a task checkpoint.

## Synchronisation

- Clean and behind-only: update with `git pull --ff-only <remote> <branch>`.
- Clean and ahead-only: push only when requested, using the detected Overleaf branch mapping.
- Diverged: stop and request an explicit reconciliation choice; do not rebase, merge, reset, or force-push by assumption.
- Dirty: create only an authorised task-scoped commit/checkpoint, or stop and report the blocking paths.
- After transfer, verify revision equality, ahead/behind counts, and tracked diff.

## Checkpoints

Use a commit for each coherent provisional batch. Include the current Codex task ID in the commit details.

Use annotated `approved` and `baseline` tags only on a normal Git repository or remote that supports tags. The Overleaf Git bridge does not support normal branch or tag workflows; never push tags to it or claim that a local tag is an Overleaf History label. If no suitable secondary remote exists, report that approval tags are local-only and not durably shared.

Report the exact revisions, remote/branch mapping, checkpoint status, verification, and unresolved divergence.