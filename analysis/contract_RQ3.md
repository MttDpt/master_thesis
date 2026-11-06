---
title: RQ3 Analysis Contract
description: Living subquestion, evidence, method, operation, and interpretation contract for RQ3.
type: rq_analysis_contract
rq: RQ3
tags:
  - analysis
  - rq3
---
# RQ3 Analysis Contract

## Research-question reference

Use the wording and thesis-level framing in [RQ3: Interpretation](../context/thesis_backbone.md#rq3-interpretation). This file does not restate the research question.

## Evidence roles

Immediate trial responses are the primary evidence for interpretation of the just-experienced stimulus. Final interviews are retrospective contextual evidence and remain separate until an explicitly defined integration step. NASA-TLX is contextual workload evidence collected after each trial; the original UEQ is contextual post-playback experience evidence and is not condition-linked in the response sheet. Neither questionnaire substitutes for the interpretation evidence.

## Related records

These links are optional routes, not required reading. Open only what the current subquestion needs.

- [Methodology Study Record](../context/methods_study-methodology.md): study setup, prototype, apparatus, procedure, and collected measures.
- [Methods: Data Preparation, Analysis, Validity and Scope](../context/methods_data-preparation.md): methodology-facing preparation, analysis boundaries, and validity.
- [Pre-processing rules](rules_preprocessing.md): exclusions, source selection, pseudonyms, and participant-trial joins.
- [RQ1 analysis contract](contract_RQ1.md): detection and contextual gaze.
- [RQ2 analysis contract](contract_RQ2.md): discrimination and confidence.

## Data sources

Choose only the source needed for the current subquestion; this list is not a mandatory reading sequence.

| Source | What it provides |
|---|---|
| `dataset/originals/transcripts/trials/P##_t1–P##_t3.docx` | Immediate post-trial interpretation responses |
| `dataset/originals/transcripts/semi-structured-interviews/P##_z.docx` | Final retrospective interviews |
| [Interview guide](dataset/semi-structured-interview.md) | Prompt structure and intended interview coverage |
| [72-trial map](dataset/trial-data/trial-data-crosswalk/72-trial-map.csv) | Participant-trial-condition crosswalk |
| Dataset registry | Transcript inventory, provenance, and routes to exact files |
| `03_NASA` questionnaire export and condition crosswalk | Trial-level NASA-TLX context: six 1–10 dimensions and an unweighted overall mean; one row per participant-trial |
| `04a_UEQ` questionnaire export | Post-playback original UEQ context: 26 bipolar items and six scale scores; one row per participant, with no condition field |

## Subquestion schema

Every subquestion records: the question; evidence and data; unit of analysis and denominator; concepts or measures; operation and comparison; dependability and diagnostics; output; and interpretation boundary. Update the current specification in place when a deep dive establishes new information or a decision; do not add dated decision logs.

## Analytical approach

Use the current [two-layer coding rules](RQ3/provisional/coding/coding-rules.md) for immediate responses. Layer 1 records one meaning-success outcome per participant-trial: `success = yes` with `specificity = full|partial`, or `success = no` with `failure = alternative|unknown|false-change`; the inactive branch is `NA`. Layer 2 records zero or more transcript-supported details for object, transformation, stage, interpretation, reason, certainty, and reaction, with per-item accuracy for objects and transformations. Every assignment retains exact evidence and a participant-trial timestamp locator. The framework is post hoc and hybrid deductive–inductive: intended mappings structure meaning-success coding, while participant-described alternatives and details are retained rather than forced into intended categories.

The canonical crosswalk condition remains the denominator and intended-reference authority. Unexpected descriptions are participant responses, not proof of a source mismatch without independent provenance evidence. The current 72-trial corpus is provisional and single-coder; the earlier independent calibration rounds informed rule clarification but do not provide reliability estimates for the final full-corpus assignments.

## Subquestions

### 1. Immediate interpretation

- **Question:** How did participants describe and interpret the visual condition immediately after each trial?
- **Evidence and data:** condition-linked `P##_t1–P##_t3` transcripts only, joined through the canonical crosswalk; neither NASA-TLX nor discrimination responses are coded as interpretation evidence.
- **Unit and denominator:** one included participant-trial transcript is one Layer 1 row; one transcript-supported detail is one Layer 2 evidence row. The current corpus contains 72 included trials from 24 participants: NT 24 and V1, V2, and V3 16 each.
- **Concepts or measures:** Layer 1 binary meaning success, success specificity (`full` or `partial`), and failure type (`alternative`, `unknown`, or NT `false-change`). Layer 2 records object, transformation, stage, interpretation, cue-to-meaning reason, certainty about meaning, and explicit reaction; object and transformation assignments carry `full`, `partial`, or `incorrect` accuracy. For V1--V3, visible content alone is insufficient: success requires an explicit or directly prompted link to the intended information. NT success is condition-consistent recognition of no meaningful animation or the continuous baseline landscape-colour shift and is not metaphor decoding.
- **Operation and comparison:** apply the versioned rules to the 72 transcripts, preserve exact evidence and locators, and summarise Layer 1 counts and proportions by condition. Summarise Layer 2 as the number of distinct participant-trials carrying each code; codes can co-occur and therefore do not sum to condition totals. Keep full and partial success separate in descriptive reporting unless an explicitly defined analysis combines them.
- **Dependability and diagnostics:** validate unique participant-trial keys, complete crosswalk coverage, expected condition denominators, valid Layer 1 branches, permitted Layer 2 labels and accuracy qualifiers, exact evidence and locators, semantic-match rules for animated success, reviewed NT assignments, and agreement between derived summaries and trial-level codes. Calibration was used to refine the rules, but the full corpus remains single-coder and no inter-rater reliability or saturation claim is supported.
- **Output:** the [coding package index](RQ3/provisional/coding/index.md), [descriptive coding report](RQ3/provisional/coding/coding-report.md), participant-trial code table, long-form code-evidence table, source manifest, machine-readable summaries, inclusion receipt, validation receipt, and reproducible build script, all grouped under `analysis/RQ3/provisional/coding/`.
- **Boundary:** immediate answers followed the discrimination questions and may have been primed by them. The codes describe post-trial reports, not perception during driving, visual salience, causal effectiveness, or prevalence beyond this sample.

### 1a. Exploratory condition comparison of meaning success

- **Question:** Does binary intended-meaning success differ between the three animations?
- **Evidence and data:** unchanged provisional Layer 1 codes, verified against the crosswalk under the [shared rules](rules_preprocessing.md).
- **Unit and denominator:** 48 animated trials from 24 participants, 16 per animation; each paired animation contrast uses the eight participants exposed to both animations. NT is excluded.
- **Measures:** failure = 0; full or partial intended-meaning success = 1. Report whole-condition descriptive proportions separately from matched-pair means and gaps.
- **Operation and comparison:** exact two-sided conditional McNemar for buildings–sun-to-moon, buildings–red-sphere and sun-to-moon–red-sphere; Holm across three. The binary exact label-swap permutation test is numerically equivalent; do not use the weighted 0/0.5/1 variant.
- **Uncertainty and diagnostics:** verify keys, coding branches, eight complete pairs, paired binary counts and exact enumeration; retain single-coder status and small overlap.
- **Output:** [current interpretation tests](RQ3/provisional/20261015-ch4-inference-adoption/interpretation_tests.csv), [paired records](RQ3/provisional/20261015-ch4-inference-adoption/interpretation_pairs.csv) and validated package.
- **Boundary:** post hoc paired subset comparison without order/carryover adjustment; no complete ranking, causal interpretation or zero population probability from 0/16. Earlier Bayesian approval is superseded for current reporting.

### 1b. Exploratory cross-RQ links and all-success

The initial cross-RQ models and exact tests are historical and superseded for current inferential reporting. Preserve the verified source join and original outputs; use subquestion 1f for current score comparisons.

### 1c. Exploratory participant-level cross-RQ success gaps

The earlier sign-test gap supplement is historical and superseded. Participant-direction hypotheses and their corrections are not the current mean-score tests.

### 1d. Combined detection score and confidence across RQs

The earlier combined-score/confidence supplement is historical and superseded for inference. Preserve animated D = (onset + completion)/2 and separate event scores; current confidence belongs to the [RQ2 contract](contract_RQ2.md#8-participant-level-q1q2-confidence-difference), with no adopted confidence–outcome association model.

### 1e. NT-inclusive response, recognition and oral-outcome comparisons

The earlier 49/79-test extension is historical and superseded for inference. Preserve its verified 72-trial source reconstruction and unchanged operational S/M definitions; current all-trial and NT comparisons follow subquestion 1f. NT correct rejection and unchanged-condition recognition remain distinct from animated event detection and metaphor interpretation.

### 1f. Mean outcome scores and animation comparisons

- **Question:** How do detection/correct-rejection, separate Q1/Q2 accuracy and condition-appropriate binary interpretation scores differ within each trial scope?
- **Evidence and data:** canonical crosswalk, cleaned trigger trials/presses, raw questionnaire answers and unchanged Layer 1 coding; reconstruct the verified join under the [shared rules](rules_preprocessing.md).
- **Unit and denominator:** 72 trials/24 participants overall, 48 animated trials/24 participants and 24 NT trials/24 participants. Each participant contributes three overall and two animated trials; t-tests use one mean per participant, not independent pooled trials.
- **Measures:** all trials use Q1, S, Q2 and M; animations use compound detection S = (onset + completion)/2, Q1, Q2 and M; NT uses Q1, binary correct rejection S, Q2 and unchanged-condition recognition M. Animated S is 0/0.5/1; M combines full and partial success as 1. NT has no onset/completion or D.
- **Operation and comparison:** all six overall pairs, all six animated pairs and all six NT pairs form one Holm family of 18. Use two-sided paired t-tests on 24 participant means for overall/animated comparisons and exact McNemar for NT binary pairs. Reuse Q1–Q2 rows in the RQ2 summary; the separate RQ1 pooled onset–completion result retains its previously adopted Holm-22 adjustment. Between-animation model-based score contrasts and the former model-based 30/48-test corrections are superseded for current reporting; only subquestion 1a supplies current between-animation interpretation inference.
- **Uncertainty and diagnostics:** independently check paired t tails, exact binary arithmetic and the Holm-18 calculation. Retain matching historical 18-family t intervals, bootstrap intervals and single-participant deletions; do not present the previous Holm-22 diagnostics as diagnostics of the replacement family. Bootstrap coverage is approximate; report supported results sensitive to participant deletion.
- **Output:** [current 18 tests](RQ3/provisional/20261016-compound-detection-outcomes/tests.csv), [current participant means](RQ3/provisional/20261016-compound-detection-outcomes/participant_means.csv), [validation receipt](RQ3/provisional/20261016-compound-detection-outcomes/receipt.json) and [retained uncertainty/deletion diagnostics](RQ3/provisional/20261016-compound-detection-outcomes/retained_uncertainty.csv). The separate phase comparison retains [the earlier 22 tests](RQ3/provisional/20261015-ch4-inference-adoption/cross_outcome_tests.csv), [participant means](RQ3/provisional/20261015-ch4-inference-adoption/participant_means.csv), [deletion diagnostics](RQ3/provisional/20261015-ch4-inference-adoption/cross_outcome_leave_one_out.csv), merged results and validated rerun.
- **Boundary:** operational score comparisons are post hoc and do not establish a common ability scale, causality, equal task difficulty, equivalence or a complete ranking. Event windows differ and coding remains provisional and single-coder. The [adopted family specification](inference_ch4.md) overrides earlier inferential approvals.

### 1g. Within-animation outcome ordering

The earlier 30-test within-animation ordering package is historical and superseded for current inference. Current per-animation onset–completion tests retain Holm-three, and Q1–Q2 accuracy retains Holm-four; do not substitute Holm-30 p-values or report the remaining ordering tests as adopted claims.

The user-requested combined-detection within-animation run is exploratory and provisional, not adopted for thesis inference. It compares all six pairs of combined detection, element recognition, change recognition and interpretation separately in sun-to-moon, buildings and red-sphere (16 distinct paired participant-trials each). Combined detection averages onset and completion (0, 0.5, 1); interpretation retains binary full-or-partial success. Two-sided paired t-tests handle comparisons involving combined detection; exact McNemar tests handle binary-stage pairs. One Holm family covers all 18 comparisons, separate from the adopted pooled Holm-18 and existing per-RQ families. Participants overlap across animations; this run tests within-animation differences, not differences between animations. Interpretation remains provisional and single-coder.

### 2. Retrospective interview themes

- **Question:** What themes appear in participants’ retrospective accounts of peripheral availability, metaphor legibility, ambiguity, trust, usability, and design suggestions?
- **Evidence and data:** `P##_z` final interviews analysed separately from immediate trial responses.
- **Unit and denominator:** the unit of coding and treatment of absent, short, or ambiguous passages remain to be defined.
- **Concepts or measures:** themes and subthemes supported by excerpt-to-code-to-theme links, including contradictory and negative cases.
- **Operation and comparison:** define and then apply a qualitative framework to the final interviews as a distinct corpus; retain provenance and codebook version.
- **Dependability and diagnostics:** define theme review, disagreement resolution, revision rules, saturation or stopping logic, and quotation selection/redaction.
- **Output:** a theme matrix, analytical narrative, and pseudonymous quotation ledger.
- **Boundary:** retrospective explanations cannot prove what a participant perceived or understood during a specific trial.

### 3. Integration of immediate and retrospective evidence

- **Question:** Where do immediate interpretations and retrospective themes converge, complement, contradict, or remain silent?
- **Evidence and data:** an approved immediate-response matrix and a completed final-interview theme matrix, with NASA-TLX and overall post-playback UEQ used only as contextual qualifiers when directly relevant.
- **Unit and denominator:** integration occurs at the level defined for the two completed analyses; the corpora are not merged into one undifferentiated dataset.
- **Concepts or measures:** convergence, complementarity, contradiction, and silence; any condition-level counts must be explicitly justified.
- **Operation and comparison:** compare the two independently analysed evidence sets only after an integration rule is defined. Connections to RQ1 or RQ2 require their own stated evidence boundary.
- **Dependability and diagnostics:** preserve traceability from every integrated claim to both source analyses and retain negative cases.
- **Output:** an integration matrix or structured narrative showing the relationship between evidence sources.
- **Boundary:** integration does not convert retrospective material into trial-time evidence or qualitative counts into prevalence estimates.

### Supplementary interpretation-score comparisons across animations

The weighted interpretation package is historical and superseded. The binary permutation rerun supplies matching historical arithmetic for the adopted exact McNemar comparisons in subquestion 1a; use the current package as reporting authority. Neither weighted scores nor the earlier Bayesian model remain selected.

## Current definitions to resolve

- Whether the provisional single-coder immediate-response assignments require a second-coder or structured-review pass before approval, and how any revisions would be reconciled and versioned.
- Unit of coding, coding framework, dependability procedure, stopping logic, and quotation-selection/redaction rules for the final retrospective interviews.
- The integration rule across immediate responses, final interviews, and any later quantitative evidence.
- Questionnaire context remains at its source grain: NASA-TLX may be linked to a participant-trial-condition record through the verified crosswalk; UEQ remains participant-level post-playback context because its export contains no condition field. Do not duplicate UEQ scores across conditions or interpret either questionnaire as direct evidence of what was perceived or understood during driving.
