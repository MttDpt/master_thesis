---
name: zotero-maintenance
description: "Use to keep Zotero metadata aligned with the thesis wiki and chapter citations."
---

# Zotero Maintenance

Use this skill to keep Zotero metadata aligned with the thesis wiki and chapter citations.

## Canonical Entry Point

Start automated, scheduled, hook-triggered, and manual maintenance through:

```bash
python3 scripts/zotero_maintenance.py plan --trigger manual
python3 scripts/zotero_maintenance.py run --trigger manual --foreground
```

The first command performs the cheap deterministic preflight and returns JSON. The second performs the same preflight and launches Codex only when the decision is `delta` or `full-audit`.

Supported triggers are `manual`, `daily`, `post-merge`, `post-rewrite-rebase`, and `pre-push-delayed`. Use `--fetch` when a manual plan must inspect current `origin/main`. Use `--force-delta` when the user explicitly requests maintenance despite an already-audited revision, and use `--force-full` only when the user explicitly requests a full audit.

Treat the returned `decision`, revision range, and audit mode as authoritative routing. Stop immediately on `no-op` or `defer-full-audit`. Do not load Zotero, scan thesis files, or write a maintenance note for those outcomes.

Use `--check-helper` for a read-only availability check. When work is due, the entry point automatically resolves the current installed Zotero skill and helper, reads `status --json`, and blocks before launching an agent if the local API is unavailable.

`scripts/run_overleaf_zotero_maintenance.sh` is only a compatibility wrapper for existing Git hooks. Do not add maintenance logic to it.

## Non-Negotiable Scope

Always redirect Zotero work to the `_LLM_wiki` collection and its child subcollections.

- Do not act on Zotero items outside `_LLM_wiki` or its children.
- If the selected Zotero collection is not `_LLM_wiki`, ignore the selected target and locate `_LLM_wiki`.
- If `_LLM_wiki` cannot be found, stop and ask the user.
- If an item match exists outside `_LLM_wiki` but not inside it, ask the user whether to add or move it before tagging.

When unsure, ask the user. Do not assume anything.

Ask before proceeding when any of these are unclear:

- which chapter files are the current source of truth;
- whether a draft, exported chapter, Overleaf file, Proof document, or wiki note is authoritative;
- which chapter number maps to a citation;
- whether two Zotero records are duplicates or the same paper;
- whether a source is actually ingested;
- whether to remove or overwrite existing tags.

## Required Tags

Apply these tags only to Zotero resources in `_LLM_wiki` or its child subcollections:

- `👍` means the resource has been ingested into the thesis wiki.
- `⚠️` means ingestion was attempted or requested but the resource could not be deeply ingested.
- `💬` means the resource is cited in current thesis chapter material.
- Chapter-number emoji tags identify where the resource is cited:
  - `1️⃣` for Introduction.
  - `2️⃣` for Related Work.
  - `3️⃣`, `4️⃣`, and later numbers only when the user or current chapter source clearly defines the chapter mapping.
- If a resource is cited across multiple chapters, keep all applicable chapter-number tags.
- If a resource later becomes deeply ingested, ask before removing `⚠️`; do not silently clean up existing warning tags.

Do not invent chapter mappings. If the chapter number is not explicit in the cited source material, ask.

## Zotero Tag Source of Truth

Treat the live Zotero library as the source of truth for tag names, tag spelling, and tag semantics that are not defined in this skill.

- Before interpreting, filtering, rewriting, or reporting on mutable semantic tags, enumerate the current tags in Zotero for `_LLM_wiki` and relevant child collections.
- This is mandatory for user-maintained tags such as the read-status tag and the high-value or fire-style tag. These tags may have been renamed; do not use older remembered names, prior-run notes, or hard-coded aliases when the live Zotero tag vocabulary differs.
- If a requested tag appears to have been renamed, state the observed current tag and treat that as authoritative for the operation. Do not recreate the deprecated tag unless the user explicitly asks for that exact tag string.
- If multiple current tags could plausibly match the user's phrase, ask before changing anything.
- When applying or removing tags, preserve unrelated Zotero tags exactly as they currently exist.
- In the final report, mention any live tag-name resolution that affected the work, especially when replacing a deprecated tag name with the current Zotero tag.

## Evidence Sources

Use the current repo state, not memory, as the authority for wiki ingestion status:

1. Read `wiki/index.md`, `wiki/log.md`, and relevant `wiki/sources/*.md`.
2. Treat a source as ingested only when a durable wiki source record exists and the repo log or source record supports that status.
3. If source status is partial, missing, ambiguous, or only present in `wiki/raw/`, do not apply `👍` unless the user explicitly decides that it counts.
4. Treat a thematic-cluster ingestion handoff, final ingestion report, or explicit user instruction as authority for applying `⚠️` to resources that could not be deeply ingested.

For citation status:

1. Treat approved files in `writing/handoff/` as the default citation source of truth for chapter and subchapter placement.
2. If the user explicitly names Overleaf, or no matching handoff file exists, inspect the paired local Overleaf checkout at `/Users/matteodelprato/Documents/Education/master_thesis/overleaf` and use the current chapter file there.
3. If the user names a bibliography, Proof document, exported draft, wiki source record, or other citation source, use that named source.
4. If the user did not name a source and handoff or Overleaf mapping is unclear, inspect likely repo surfaces only to form a question, then ask which source of truth to use.
5. Use headings and chapter filenames from the selected source to determine chapter-number tags.
6. Do not infer cited-resource placement from old planning notes or removed graph nodes.
7. Extract all cited resources and map each citation to Zotero item keys before tagging.
8. Keep Zotero item keys distinct from BibTeX keys.

Chapter drafts and Overleaf files identify cited or intended thesis placement. They do not prove that a resource is deeply ingested; ingestion status still comes from `wiki/sources/`, `wiki/log.md`, ingestion reports, or explicit user instruction.

## Cleanup Mode

When the user asks to clean up, tidy up, reconcile, or audit the Zotero collection:

1. Treat approved drafts in `writing/handoff/` as the citation source of truth unless the user names a different approved source.
2. Read every approved handoff draft needed for the requested scope. If scope is unspecified, inspect `writing/handoff/` and ask whether to clean all chapter files or only selected chapters.
3. Extract every cited item from each handoff draft. Support LaTeX citations such as `\cite{key}` and unresolved author-year citations, but ask before mapping ambiguous citations.
4. Browse Zotero `_LLM_wiki` and child subcollections.
5. Search for every cited item and map it to a Zotero item key and BibTeX key.
6. Compare the handoff-derived citation set against current Zotero tags.
7. Add missing citation tags for verified cited items:
   - `💬`;
   - applicable chapter-number emoji tags.
8. Always remove stale citation-placement tags during cleanup/tidying once the item is verified as no longer cited in the approved handoff scope. This includes `💬` and chapter-number emoji tags. Do not ask again for this removal policy.
9. Do not remove `👍` or `⚠️` merely because a source is uncited. Ingestion-status tags are governed by `wiki/sources/`, `wiki/log.md`, ingestion reports, or explicit user instruction.
10. Ask before changing tags for duplicate, ambiguous, missing, or out-of-scope Zotero records.

## Zotero Access

Resolve the installed Zotero skill and helper through:

```bash
python3 scripts/zotero_maintenance.py plan --trigger manual --check-helper
```

Read the returned `zotero.skill_file`, then use the returned `zotero.helper`. Do not search for or hard-code plugin cache hashes elsewhere in the workflow.

For Zotero writes, retry the normal helper or local API path once when practical. If the write path fails with `501 Method not implemented`, read-only/local-only behavior, or another confirmed write-surface blocker, use the SQLite fallback without asking again:

1. Quit Zotero.
2. Wait for `zotero.sqlite-wal`, `zotero.sqlite-shm`, and `zotero.sqlite-journal` lock files to clear.
3. Back up the active Zotero database, usually `/Users/matteodelprato/Zotero/zotero.sqlite`, with a timestamped filename.
4. Apply only the verified `_LLM_wiki` or child-collection tag/collection changes.
5. Preserve item versions; mark changed items unsynced and update modified timestamps so Zotero treats the edits as local changes.
6. Reopen Zotero and verify through the local API.

Do not use SQLite fallback for duplicate, ambiguous, missing, or out-of-scope records unless the user has explicitly approved those records.

## Automatic-Run Safety

- Keep the launcher prompt short and treat this skill as the only detailed procedure.
- Do not launch an agent for `nothing-needed`, `larger-review-deferred`, or blocked preflight outcomes.
- Before any SQLite fallback, make a timestamped database backup and verify that it opens before changing the database.
- After every write, reopen or query Zotero and verify the exact affected items and tags.
- Allow only one maintenance process at a time. If the lock reports another active process, stop without launching a second agent.
- Report one explicit outcome: `nothing-needed`, `small-update-completed`, `larger-review-completed`, or `blocked-human-or-app-action-needed`.

## Workflow

1. Run the canonical entry point in `plan` mode. Stop on `no-op` or `defer-full-audit`.
2. Check `git status --short` and note unrelated repo changes without reverting them.
3. Confirm or identify the citation source of truth, ingestion handoff, cleanup scope, and chapter/subchapter mapping. For cleanup/tidying and chapter or subchapter cited-resource work, start with approved files in `writing/handoff/`. For a `daily` or hook plan, use the paired Overleaf checkout and the exact revision range returned by the entry point. Ask if an interactive request remains ambiguous.
4. Locate `_LLM_wiki` and its child subcollections in Zotero.
5. Enumerate live Zotero tags for the relevant `_LLM_wiki` scope before interpreting any user-maintained semantic tag, including read-status and high-value/fire-style tags.
6. Build a candidate table with:
   - citation string or BibTeX key;
   - paper title;
   - chapter number tag or tags;
   - ingestion outcome: ingested, failed, partial, not matched, or unknown;
   - failure reason when `⚠️` is intended;
   - Zotero item key;
   - current collection path;
   - current tags;
   - intended tag additions or removals;
   - live tag-name resolution, if a user phrase maps to a current Zotero tag;
   - uncertainty or blocker.
7. Cross-check ingested status against `wiki/sources/` and `wiki/log.md`.
8. Apply tags only for unambiguous items in `_LLM_wiki` scope:
   - add `👍` for ingested resources;
   - add `⚠️` for resources that could not be deeply ingested;
   - add `💬` for cited resources;
   - add chapter-number emoji tags.
9. During cleanup/tidying, remove verified stale citation-placement tags by default. Do not remove `👍` or `⚠️` as part of stale citation-placement cleanup.
10. Verify the Zotero tags after writing, persist the state for the routed revision, and return a concise status.

## Final Report

Report:

- `_LLM_wiki` collection path used;
- citation source of truth used;
- number of resources inspected;
- number tagged as ingested with `👍`;
- number flagged as failed ingestion with `⚠️`;
- number tagged as cited with `💬`;
- chapter-number tags applied;
- stale citation-placement tags removed;
- live Zotero tag-name resolutions used, including read-status or high-value/fire-style tag names when relevant;
- skipped items and exact reason;
- questions that still need user decisions.
