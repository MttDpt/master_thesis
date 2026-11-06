---
title: RQ2 Analysis Contract
description: Living subquestion, evidence, metric, operation, and interpretation contract for RQ2.
type: rq_analysis_contract
rq: RQ2
tags:
  - analysis
  - rq2
---
# RQ2 Analysis Contract

## Cross-RQ analysis route

Use the [adopted Chapter 4 specification](inference_ch4.md) and [RQ3 mean-score subquestion](contract_RQ3.md#1f-mean-outcome-scores-and-animation-comparisons). Overall and animated Q1–Q2 mean-accuracy tests reuse the cross-outcome Holm-18 family. Within-condition binary accuracy uses Holm-four; numerical confidence retains the expanded Holm-15 family. Earlier sign tests and other cross-RQ models/corrections are superseded for current inference.

## Research-question reference

Use the wording and thesis-level framing in [RQ2: Discrimination](../context/thesis_backbone.md#rq2-discrimination). This file does not restate the research question.

## Evidence roles

The discrimination questionnaire is the primary evidence. Q1 concerns recognition of the visible element, Q2 concerns recognition of the displayed change, and confidence is an ordinal companion measure rather than evidence of correctness by itself.

## Current inferential evidence

The current RQ2 results use paired t-tests of 24 participant mean accuracies overall and animated (within Holm-18), exact McNemar for Q1/Q2 within four conditions (Holm-four), and paired numerical-confidence t-tests overall, animated and within each condition (existing expanded Holm-15). All earlier inferential approvals outside these families are superseded; participant-direction sign tests are historical only. Numerical confidence assumes equal 1–4 rating steps and does not test correctness or calibration.

## Related records

These links are optional routes, not required reading. Open only what the current subquestion needs.

- [Methodology Study Record](../context/methods_study-methodology.md): study setup, prototype, apparatus, procedure, and collected measures.
- [Methods: Data Preparation, Analysis, Validity and Scope](../context/methods_data-preparation.md): methodology-facing preparation, analysis boundaries, and validity.
- [Pre-processing rules](rules_preprocessing.md): exclusions, source selection, pseudonyms, and cross-modal joins.
- [RQ1 analysis contract](contract_RQ1.md): detection and contextual gaze.
- [RQ3 analysis contract](contract_RQ3.md): immediate and retrospective interpretation.

## Data sources

Choose only the source needed for the current subquestion; this list is not a mandatory reading sequence.

| Source | What it provides |
|---|---|
| [Aggregated workbook](dataset/originals/questionnaire-data/data-aggregated.xlsx), sheet `02_DiscriminationQ` | Participant, trial, condition, response, existing score, and confidence fields |
| [Raw questionnaire export](dataset/originals/questionnaire-data/discrimination-questionnaire.xlsx), sheet `Form responses 1` | Original wording and source verification; contains an identifying name field that must not enter analysis outputs |
| [72-trial map](dataset/trial-data/trial-data-crosswalk/72-trial-map.csv) | Included participant-trial-condition crosswalk |
| Dataset registry | Provenance and routes to the exact files |

## Subquestion schema

Every subquestion records: the question; evidence and data; unit of analysis and denominator; measures; operation and comparison; uncertainty and diagnostics; output; and interpretation boundary. Update the current specification in place when a deep dive establishes new information or a decision; do not add dated decision logs.

## Subquestions

### 1. Visible-element discrimination

- **Question:** How accurately did participants identify the visible element in each condition?
- **Evidence and data:** Q1 response, paired Q1 confidence, the approved scoring key, and the participant-trial-condition crosswalk.
- **Unit and denominator:** one crosswalk-matched aggregated response per eligible participant-trial; retain exactly 72 rows. Each Q1 denominator is the number of non-missing eligible Q1 responses in that condition; do not impute a missing response and stop the run if a crosswalk key has zero or multiple matches.
- **Measures:** reconstructed Q1 correctness and the full response-option distribution.
- **Operation and comparison:** derive correctness from the approved expected answer; treat the existing `score` field as a reconciliation diagnostic, not as the authority. Report correct counts and proportions by condition before any comparison.
- **Uncertainty and diagnostics:** use 95% participant-clustered bootstrap percentile intervals for condition-specific proportions, resampling participants with all of their rows intact. Report missing responses, duplicate keys, score disagreements, sparse response options, and condition denominators.
- **Output:** exact response-option table and 100%-stacked response bars by condition; accuracy dots with 95% intervals and displayed numerators and denominators.
- **Boundary:** Q1 concerns the visible element only and does not establish recognition of the change or its intended meaning.

### 2. Change discrimination

- **Question:** How accurately did participants identify whether a change occurred and what changed in each condition?
- **Evidence and data:** Q2 response, paired Q2 confidence, the approved scoring key, and the participant-trial-condition crosswalk.
- **Unit and denominator:** one crosswalk-matched aggregated response per eligible participant-trial; retain exactly 72 rows. Each Q2 denominator is the number of non-missing eligible Q2 responses in that condition; do not impute a missing response and stop the run if a crosswalk key has zero or multiple matches.
- **Measures:** reconstructed Q2 correctness and the full response-option distribution.
- **Operation and comparison:** derive correctness from the approved expected answer; treat the existing `score 2` field as a reconciliation diagnostic, not as the authority. Report correct counts and proportions by condition before any comparison.
- **Uncertainty and diagnostics:** use 95% participant-clustered bootstrap percentile intervals for condition-specific proportions, resampling participants with all of their rows intact. Report missing responses, duplicate keys, score disagreements, sparse response options, and condition denominators.
- **Output:** exact response-option table and 100%-stacked response bars by condition; accuracy dots with 95% intervals and displayed numerators and denominators.
- **Boundary:** Q2 concerns recognition of whether a displayed change occurred and, when applicable, what changed; it does not establish interpretation of the change’s meaning.

### 3. Confidence

- **Question:** How was confidence distributed, and did higher confidence accompany correct responses?
- **Evidence and data:** the Q1 and Q2 1–4 confidence ratings, where 1 means guessing and 4 means very sure according to the [Methodology Study Record](../context/methods_study-methodology.md#32-research-process-and-rq-to-method-alignment).
- **Unit and denominator:** one non-missing confidence response paired only with correctness for the same question; keep Q1 and Q2 separate. For each question and confidence level, the accuracy denominator is all eligible responses at that level.
- **Measures:** ordinal confidence frequencies and level-specific accuracy: correct responses at confidence level *k* divided by all responses at level *k*.
- **Operation and comparison:** describe all four response levels and accuracy at each level, keeping Q1 and Q2 separate and never mapping a rating directly to a probability. For the adopted numerical mean comparisons in section 8, retain the original 1–4 values and state the equal-step assumption; this is a separate numerical analysis of the recorded ordinal ratings, not a change to scoring or an average of Q1 with Q2.
- **Uncertainty and diagnostics:** report denominators, impossible values, missing ratings, ties, sparse levels, and participant clustering.
- **Output:** exact ordinal-frequency and level-specific-accuracy tables plus confidence-by-correctness distribution figures.
- **Boundary:** confidence is self-reported certainty, not correctness, reliability, or causal evidence; an observed rise in accuracy across ratings is descriptive calibration evidence only.

### 4. Descriptive condition comparisons and full discrimination

- **Question:** how do observed Q1 correctness, Q2 correctness and joint success vary across the complete conditions?
- **Evidence and data:** verified separate Q1/Q2 correctness under the approved key.
- **Unit and denominator:** one eligible participant-trial; NT 24 and each animation 16, subject to the corresponding non-missing response denominator.
- **Measures:** question-specific accuracy; both correct, Q1 only, Q2 only and neither correct. Full discrimination is secondary and equals 1 only when both questions are correct.
- **Operation and comparison:** retain exact condition counts and response distributions descriptively. Use section 7 for overall/animated mean comparisons and section 10 for within-condition exact accuracy comparisons.
- **Uncertainty and diagnostics:** report denominators, missing responses, sparse/all-success cells and participant dependence. Historical descriptive bootstrap summaries and Bayesian ranking models remain archived; they are not the selected inferential results.
- **Output:** descriptive counts from the validated paired input.
- **Boundary:** contrasts describe complete bundled mappings and cannot isolate abstraction or animation form; no condition ranking or individual test–retest reliability claim is established.

### 5. Animated detection-to-discrimination profile

- **Question:** Where does the observed animated-trial chain from trigger-event detection to questionnaire discrimination break?
- **Evidence and data:** the approved RQ1 animated trial detection profile and the reconstructed RQ2 full-discrimination state, joined under the shared cross-modal rule in [pre-processing rules](rules_preprocessing.md).
- **Unit and denominator:** one animated participant-trial; 48 total and 16 in each of V1, V2, and V3. Questionnaire denominators remain trial-based, not event-based.
- **Measures:** RQ1 `both detected`, `onset only`, `completion only`, or `neither`; RQ2 `both correct`, `Q1 only`, `Q2 only`, or `neither`.
- **Operation and comparison:** cross-tabulate the two profiles overall and by animated condition with exact counts and within-scope proportions.
- **Uncertainty and diagnostics:** show join completeness, unique keys, condition denominators, and sparse cells. If uncertainty is added, resample whole participants; it is not required for the exact descriptive cross-tab.
- **Output:** sanitized one-row-per-trial join, exact cross-tab, and condition panels.
- **Boundary:** describe only where the observed detection-to-discrimination chain breaks; do not attribute a questionnaire state to detection or infer causality.

### 6. NT behavioural-questionnaire consistency

- **Question:** How does an RQ1 NT false-alarm trial flag co-occur with Q2 correct `no change` discrimination and Q2 confidence?
- **Evidence and data:** the approved RQ1 NT trial false-alarm count and reconstructed RQ2 Q2 correctness and ordinal confidence, joined at participant-trial grain.
- **Unit and denominator:** one NT participant-trial; 24 total. The 17 individual false-alarm presses remain secondary descriptive records and are never a questionnaire denominator.
- **Measures:** any versus no false alarm, Q2 correct `no change`, and paired Q2 confidence on the 1–4 ordinal scale.
- **Operation and comparison:** tabulate exact trial counts/proportions by false-alarm flag and Q2 correctness, and retain the ordinal confidence frequency table by false-alarm flag.
- **Uncertainty and diagnostics:** report key uniqueness, 24-trial denominator, and the 17-press secondary reconciliation; do not impute missing values.
- **Output:** sanitized NT trial join, exact tables, and a trial-count figure.
- **Boundary:** this is behavioural-questionnaire consistency only; it does not show causation.

### 7. Participant-level Q1–Q2 accuracy difference

- **Question:** Is mean Q1 accuracy higher than mean Q2 accuracy overall and in animated trials?
- **Evidence and data:** reconstruct binary correctness from the unchanged answer key and verified participant-trial joins.
- **Unit and denominator:** 24 paired participant means over three trials overall (72) or two animated trials (48); retain misses and incorrect answers.
- **Measures:** Q1 and Q2 accuracy on 0–1 scales; first-minus-second mean gaps.
- **Operation and comparison:** two-sided paired t-tests on participant averages; reuse the two corresponding rows in the 18-comparison cross-outcome family, without a separate two-test correction or duplicate corroboration.
- **Uncertainty and diagnostics:** mean-gap t intervals, whole-participant bootstrap and leave-one-participant-out diagnostics in the [retained matching cross-outcome uncertainty](RQ3/20261016-compound-detection-outcomes/retained_uncertainty.csv); independent participant bundles and appropriate paired-mean assumptions.
- **Output:** [pooled accuracy tests](RQ2/statistical-tests/20261015-ch4-inference-adoption/pooled_accuracy.csv) and RQ2 results.
- **Boundary:** post hoc mean-score comparisons under the observed exposure schedule, not participant-direction tests, every-condition superiority or causality.

### 8. Participant-level Q1–Q2 confidence difference

- **Question:** Does mean numerical confidence differ between Q1 and Q2 overall, animated and within each condition?
- **Evidence and data:** original 1–4 ratings paired within trial, with the unchanged crosswalk and no dichotomisation or imputation.
- **Unit and denominator:** 24 paired participant means overall and animated; 24 NT pairs and 16 pairs per animation for condition-specific comparisons.
- **Measures:** numerical means and Q1-minus-Q2 gaps; equally spaced rating steps are assumed.
- **Operation and comparison:** two-sided paired t-tests, retaining the original expanded Holm-15 family. Recompute all nine numerical t-tests and six ordinal-model contrasts described in the [current specification](inference_ch4.md); only six within-scope/condition numerical question contrasts lead Results. Participant-direction sign tests are superseded, not members of this family.
- **Uncertainty and diagnostics:** t intervals, paired counts, missingness and cumulative-logit model convergence/gradient/Hessian checks; preserve the family even for unselected supporting members.
- **Output:** [confidence results](RQ2/statistical-tests/20261015-ch4-inference-adoption/mean_confidence_tests.csv), [complete family](RQ2/statistical-tests/20261015-ch4-inference-adoption/confidence_family15.csv) and [rerun code](RQ2/statistical-tests/20261015-ch4-inference-adoption/rerun_confidence.R).
- **Boundary:** means are not marginal medians, probability calibration, confidence predicting correctness or ordinal participant direction; post hoc selection and order/exposure limits remain.

### 9. Direct confidence-median comparisons

The earlier median-comparison package is historical and superseded for current inferential reporting. Preserve original ratings and descriptive medians/IQRs without adding median claims to the adopted numerical-confidence results.

### 10. Accuracy gaps within and between animations

- **Question:** Within each condition, does Q1 accuracy differ from Q2?
- **Evidence and data:** unchanged reconstructed binary correctness, paired by participant-trial.
- **Unit and denominator:** 16 distinct paired participants for each animation and 24 NT pairs.
- **Measures:** exact binary paired counts, Q1/Q2 proportions and Q1-minus-Q2 mean gap.
- **Operation and comparison:** exact two-sided conditional McNemar for NT, sun-to-moon, buildings and red-sphere; Holm across these four tests. The NT comparison also occurs in Holm-18, so retain both family labels and do not count it as independent evidence.
- **Uncertainty and diagnostics:** verify paired counts, unique participants and exact binomial arithmetic; report raw and adjusted p-values. No between-animation difference-of-gaps model is selected for current Results.
- **Output:** [current within-condition accuracy](RQ2/statistical-tests/20261015-ch4-inference-adoption/within_condition_accuracy.csv); the earlier gap-interaction package remains historical.
- **Boundary:** comparisons concern each observed condition separately; unequal significance labels do not establish an interaction, animation ranking, causation or equivalence.

## Current definitions

- **Approved scoring key:** NT = Q1 `None of these` and Q2 `I did not witness any changes`; V1 = Q1 `Sun and moon` and Q2 `A day-to-night timelapse`; V2 = Q1 `Buildings` and Q2 `Landscape changing`; V3 = Q1 `A red glowing sphere` and Q2 `A progressive camera close up on the scene`.
- Existing score fields are diagnostic; reconstructed correctness under this key is authoritative.
- Preserve 72 crosswalk-matched responses from 24 participants; stop on missing or duplicate aggregate matches, then report any question-specific missing outcome/confidence pairs without imputation.

- Only the adopted paired-mean accuracy, within-condition McNemar and numerical-confidence families above supply current RQ2 inference; all older approvals are superseded.
- Preserve original numerical outputs as historical provenance; use the validated adopted rerun for current reporting. Adoption does not imply preregistration or publication of revised thesis prose.
