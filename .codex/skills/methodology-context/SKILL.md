---
name: methodology-context
description: Retrieve and maintain the thesis project's evolving methodology
  knowledge. Use for questions, drafting, reviews, or decisions about the
  realised study design, prototype, apparatus, participants, procedure,
  measures, raw-data schemas, statistical analysis, qualitative analysis,
  exclusions, validity, missing setup details, or Chapter 3 methodology context.
---

# Methodology Context

Use `context/index.md` as the routing entry point. Load only the matching sections and exact underlying data needed for the task.

## Retrieval workflow

1. Read `context/index.md`.
2. Identify the applicable research question, design level, data modality, participants, trials, and conditions.
3. Read the matching section of `context/methods_study-methodology.md` and the matching RQ analysis plan.
4. For analysis work, also read the relevant RQ and canonical study-source route in `context/thesis_backbone.md`.
5. Start local study-data retrieval at `analysis/dataset/manifest.csv`, then inspect the exact XLSX sheet, CSV schema, transcript set, or questionnaire before making a participant-level claim or selecting an analytical method. Use the manifest's Drive ID when provenance or freshness must be checked.
6. Label the answer or output as source-reported, analysis-derived, externally supported, or thesis interpretation where the distinction matters.

## Analysis recommendations

- Derive candidate methods from the realised design, measurement scales, repeated structure, imbalance, exclusions, missingness, and actual distributional diagnostics.
- Distinguish confirmatory choices from exploratory choices and from decisions made after viewing results.
- State the estimand, unit of analysis, model or comparison, assumptions, effect size, uncertainty reporting, diagnostics, and sensitivity checks.
- Do not choose a statistical test from variable names alone.
- Do not invent cleaning, scoring, coding, AOI, trigger-window, or integration rules that remain open in the matching RQ plan.
- When a meaningful choice cannot be resolved from the current data and context, present the bounded options and record the chosen outcome only after user confirmation or empirical validation.

## Maintaining context

- Add newly confirmed study facts to the smallest matching section of `study-record.md`, with provenance and date.
- Add an unresolved gap to the matching RQ plan.
- When an analysis decision is made, use the decision-entry schema in that plan; preserve superseded choices rather than silently replacing them.
- Reconcile compact summaries in `thesis_backbone.md` when a new confirmed fact makes them stale.
- Keep methodology context out of `wiki/claims/` unless it is evidence from an external source; keep chapter prose in `writing/`.
- Preserve P## pseudonyms and never copy participant-identifying data.
