---
name: da-rq-contract
description: Use when new RQ-specific subquestions, evidence, metrics, operations, comparisons, diagnostics, figures, or interpretation boundaries are established to update the matching RQ contract.
---
# Update RQ Analysis Contract

Maintain exactly one living contract: `analysis/contract_RQ1.md`, `analysis/contract_RQ2.md`, or `analysis/contract_RQ3.md`.

Use this skill during any thesis RQ or dataset deep dive that establishes or changes an RQ-specific subquestion, evidence role, data source, unit of analysis, denominator, metric, operation, comparison, uncertainty method, diagnostic, sensitivity, table, graph, or interpretation boundary.

Load [$da-explainer](../da-explainer/SKILL.md) when the conversation includes analytical choices or statistical concepts.

## Contract maintenance

- Load `open-knowledge` and use its tools for every project Markdown read or write.
- Run `git status --short` and preserve unrelated work.
- Resolve the matching RQ and read its contract first. Follow related links only when the current decision needs information not stored there.
- Treat the user's direct statements and clearly accepted choices as authority. Keep unresolved definitions concise; do not promote an option or agent suggestion to the current specification.
- Update the current specification in place during the deep dive. Do not append a dated history.
- Never restate the full research question. Link to the matching anchor in `context/thesis_backbone.md`.
- Do not add decision logs, dates, status checkpoints, scope contracts, required-reading chains, readiness checks, deliverables, stop conditions, or repeated pre-processing rules.
- Route shared cleaning, exclusion, alignment, classification, and derived-input definitions to `da-preprocessing` and link to `analysis/rules_preprocessing.md`.
- Use the common subquestion schema already present in the RQ files: question; evidence and data; unit and denominator; measures; operation and comparison; uncertainty or dependability and diagnostics; output; interpretation boundary.
- Prefer the smallest coherent edit; add a new subquestion only when the conversation identifies a distinct analytical question.
- Re-read the changed section, check broken links, run a scoped OpenKnowledge audit, and run `git diff --check`.

Use `da-code` when the user asks to compute, plot, validate, or produce an analysis package.
