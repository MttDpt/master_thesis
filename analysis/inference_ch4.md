---
title: Current Chapter 4 inferential evidence
description: Adopted test families, correction scopes, supersession and validated rerun evidence for RQ1–RQ3.
type: analysis_specification
status: adopted_for_reporting
tags:
  - analysis
  - statistics
  - results
---
# Current Chapter 4 inferential evidence

## Authority and supersession

The user adopted the Chapter 4 main-text tests on 15 October 2026 in chat `01a13f05-e6c5-71e2-93a8-bccf8ecaf9e3`, instructed a rerun and made them override all earlier inferential approvals. See the adoption record and validated coordinated rerun. The inventoried Overleaf source revision was `7405d76`.

Only the five families below supply current inference. Every earlier inferential approval or selection outside these families is superseded, including participant-direction sign tests, Bayesian detection/recognition/interpretation models, older cross-RQ association/gap families, gaze/rank tests, median comparisons, reaction-time tests and extra within/between-animation models. Preserve historical data, code, reports and numerical outputs unchanged; their former approval labels do not override this specification. Previously run exact tests retained below are adopted with their specified corrections, not as independent replications.

The old appendix sign tests and Bayesian contrasts remain physically present in the inventoried Overleaf revision but are historical evidence. This documentation update does not revise, compile or publish thesis prose.

## Adopted families

All tests are two-sided; Holm-adjusted p < .05 is the reporting threshold. Separate families address separate adopted questions and do not control the entire historical analytical search.

| Family | Comparisons and unit | Current source |
| --- | --- | --- |
| Cross-outcome Holm-18 | Six pairs among Q1, S, Q2 and M in each of all trials (72), animated trials (48) and NT (24). Animated S = (onset + completion)/2; NT S is correct rejection. Overall/animated comparisons use paired t-tests of 24 participant means; NT uses exact McNemar. | [All 18 tests](RQ3/20261016-compound-detection-outcomes/tests.csv), [validation](RQ3/20261016-compound-detection-outcomes/receipt.json) |
| RQ1 detection Holm-three | Exact McNemar, onset versus completion separately in each animation, 16 paired binary records per animation. The separate pooled onset–completion result retains the previously adopted Holm-22 t-test. | [Three tests](RQ1/statistical-tests/20261015-ch4-inference-adoption/within_animation_detection.csv) |
| RQ2 accuracy Holm-four | Exact McNemar, Q1 versus Q2 separately in NT and each animation; 24 NT pairs and 16 per animation. Overall/animated comparisons reuse Holm-18. | [Four tests](RQ2/statistical-tests/20261015-ch4-inference-adoption/within_condition_accuracy.csv) |
| RQ2 confidence Holm-15 | Six selected paired numerical-confidence t-tests: overall and animated participant means (24 each), NT (24 pairs), and three animations (16 pairs each); retain the existing expanded 15-member family. | [Six selected tests](RQ2/statistical-tests/20261015-ch4-inference-adoption/mean_confidence_tests.csv), [complete family](RQ2/statistical-tests/20261015-ch4-inference-adoption/confidence_family15.csv) |
| RQ3 interpretation Holm-three | Exact McNemar between buildings–sun-to-moon, buildings–red-sphere and sun-to-moon–red-sphere; eight shared participants per contrast, not independent groups of 16. | [Three tests](RQ3/20261015-ch4-inference-adoption/interpretation_tests.csv), [paired records](RQ3/20261015-ch4-inference-adoption/interpretation_pairs.csv) |

The confidence correction family includes nine t-tests (three scopes, three between-animation differences in confidence gaps and three within-animation Q1–Q2 comparisons) and six ordinal-model contrasts (three scopes and three animations). Refit all 15 members to preserve the existing correction; only six within-scope/condition numerical question contrasts lead Results. The ordinal model uses a cumulative logit link, question-by-condition and question-by-categorical-position fixed terms, and participant and participant-trial random intercepts. Supporting ordinal and between-animation members are not additional selected claims; older participant-direction sign tests are not family members. See the [R rerun code](RQ2/statistical-tests/20261015-ch4-inference-adoption/rerun_confidence.R).

The NT Q1–Q2 raw test appears in Holm-18 and Holm-four; retain both correction labels (adjusted p = 0.34375 versus 0.09375), without treating it as independent corroboration. Repeated pooled rows in RQ-specific sections are also the same tests.

## Inputs and scoring

Apply unchanged source selection, exclusions and [preprocessing rules](rules_preprocessing.md). Retain 24 participants with one NT and two distinct animated trials each, 72 trials overall and 16 trials per animation. Keep misses in binary detection denominators, preserve missing/inapplicable values and stop on duplicate or mismatched join keys.

- Onset is 30,90) seconds; completion [90,120). Exactly 120 seconds is trial_end. NT correct rejection is no retained press over inclusive 0–120 s.
- Animated S = (onset + completion)/2, giving 0, 0.5 or 1; NT S is binary correct rejection. NT has no onset/completion or D event score.
- Q1 and Q2 remain separate binary correctness scores under the unchanged scoring key.
- M = 1 for full or partial intended-meaning success and 0 for failure; NT M is unchanged-condition recognition. Do not use half-credit interpretation scoring.
- Preserve separate original 1–4 confidence ratings. Numerical means assume equally spaced rating steps; no probability mapping, dichotomisation, sign recoding or imputation.
- Between-animation interpretation tests use the eight matched participants; whole-condition descriptive proportions use 16 and must remain separately labelled.

## Current findings and validation

The rerun reproduces the inventoried chapter: three all-trial Q1 advantages and three animated Q1 advantages; no supported NT-only cross-outcome differences; higher onset detection for sun-to-moon and buildings; higher within-condition Q1 accuracy for red-sphere; higher mean Q1 confidence overall, animated, buildings and red-sphere; higher interpretation success for buildings than red-sphere only. Other adopted comparisons are inconclusive. See [RQ1 results, RQ2 results, RQ3 results and the merged synthesis.

The [main receipt](RQ3/20261015-ch4-inference-adoption/receipt.json) records 2,129 passing checks of reconstructed sources, paired means, exact arithmetic, confidence refits and unchanged historical outputs. The [independent validation](RQ3/20261015-ch4-inference-adoption/independent_validation.json) passed 126 checks, including independent Holm and exhaustive binary-null enumeration. Mean-gap diagnostics retain 200,000 whole-participant bootstrap draws (seed 20261014) and every single-participant deletion; bootstrap coverage is approximate. Those diagnostics describe the retained phase-based package. The [compound-score rerun](RQ3/20261016-compound-detection-outcomes/receipt.json) independently reproduces the historical 18-family raw and adjusted tests and retains its matching uncertainty and deletion outputs; no new bootstrap simulation was performed.

## Interpretation boundaries

All inference remains post hoc, selected after inspection of earlier analyses; validation does not make the design confirmatory. Paired t-tests target mean participant-score differences, while McNemar tests target paired binary marginal differences. Confidence means are not population medians, participant-direction tests, calibration or confidence predicting correctness.

Unequal 60-/30-second detection windows, incomplete overlapping exposure, possible trial-order/carryover effects and provisional single-coder interpretation limit generalisation. The adopted pairwise tests do not adjust for order. Operational score gaps do not establish a common ability scale, causal sequence, safety or complete ranking. Zero observed red-sphere interpretations do not imply zero population probability; inconclusive does not mean equivalent.

Reaction times, gaze, driving behaviour, workshop, NASA-TLX and UEQ are descriptive in current Results; no replacement inferential tests are added for them.
