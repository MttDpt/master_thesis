---
name: da-preprocessing
description: Use to update and maintain analysis/rules_preprocessing.md whenever the user establishes or changes a pre-processing rule
---
# Update Pre-processing Rules

Maintain `analysis/rules_preprocessing.md` as the light source of truth for current study-data pre-processing rules.

## When to update

Use this skill during any thesis data or RQ deep dive that establishes or changes a rule about source selection, exclusions, naming, participant-trial mapping, joins, missingness, duplicates, retained intervals, time alignment, cleaning, classification, transformation, or derived-input provenance.

The user has authorised these in-project updates as part of deep-dive conversations. Write a rule when the user states it directly or clearly confirms it; do not turn an unresolved option or agent suggestion into a rule.

## How to maintain the file

- Load `open-knowledge` and use its tools for every project Markdown read or write.
- Run `git status --short` and preserve unrelated work.
- Read the current rules file first. Follow its optional links only when the missing context is needed.
- Add or revise the smallest current rule in place. Consolidate overlaps instead of repeating an older version.
- Keep only operative rules. Do not add dates, statuses, checkpoints, receipts, evidence logs, decision history, readiness statements, or validation narratives.
- Keep shared pre-processing here; put RQ-specific subquestions, metrics, operations, comparisons, uncertainty, figures, and interpretation boundaries in the matching RQ contract.
- Never alter raw data, expose identifying fields, or infer an outcome-changing rule from ambiguous names or observed condition results.
- Re-read the changed section, check broken links, run a scoped OpenKnowledge audit, and run `git diff --check`.

If the conversation is about execution rather than defining a rule, use `da-code`.
