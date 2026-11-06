---
title: "Methods: Data Preparation, Analysis, Validity and Scope"
description: Study-data preparation, analysis boundaries, and validity context.
type: methodology_methods_data_preparation
status: partially_specified
updated: 2026-10-06
provenance: user-confirmed and study-artifact-derived project context
---

# Methods: Data Preparation, Analysis, Validity and Scope

This standalone record contains the detailed Sections 3.6 and 3.7 from the [Methodology Study Record](methods_study-methodology.md). It preserves confirmed methodology facts and intended chapter claims.

## Related records

These links are optional routes, not required reading. Open only the record needed for information that is not defined here.

- [Methodology Study Record](methods_study-methodology.md): study setup, prototype, apparatus, procedure, and collected measures.
- [Pre-processing rules](../analysis/rules_preprocessing.md): current cleaning, exclusion, source-selection, alignment, and classification rules.
- [RQ1 analysis contract](../analysis/contract_RQ1.md): detection, trigger, gaze, and lane-positioning subquestions and operations.
- [RQ2 analysis contract](../analysis/contract_RQ2.md): discrimination, correctness, confidence, and comparison subquestions.
- [RQ3 analysis contract](../analysis/contract_RQ3.md): immediate interpretation, interview, coding, and integration subquestions.

## 3.6 Data Preparation and Analysis

Status: partially specified

### 3.6.1 Data preparation and exclusions

#### Confirmed facts

- Data were organised by pseudonymous participant, trial number, and scheduled condition.
- The aggregate workbook contained demographics, discrimination, NASA-TLX, original-UEQ responses, and trigger data.
- Gaze and simulator time series were stored separately; transcripts were stored by participant and task suffix. The inspected gaze export contains timestamp, two gaze-coordinate fields, gaze source, and validity status. Current coordinate, display-region, missingness, and fixation definitions are maintained in the [pre-processing rules](../analysis/rules_preprocessing.md).
- P00 was excluded as a pilot. P06 and P07 were excluded from all modalities because of the five-trigger capacity issue. P25 and P26 replaced them across all measures.
- No gaze cleaning, validity filtering, interpolation, outlier handling, imputation, or manual correction had been performed at the interview stage. No files, trials, or questionnaire responses were known to be missing or manually corrected beyond the P00/P06/P07 exclusion and replacement logic. Some additional trial retakes may have occurred, but the affected sessions and reasons are unknown.

Source of confirmation: user interview, 2026-07-14 and 2026-07-15; attached driving CSV `_20260311_160838.csv` inspected 2026-07-15; existing Chapter 3 handoff and backbone inspected 2026-07-14.

#### Exact intended chapter insertion or claim

Report the confirmed organisation and exclusions. State that data cleaning and analysis-specific quality procedures had not yet been performed at the interview stage. Do not imply that filtering, imputation, or manual correction occurred. Mark unknown retakes and unconfirmed timestamp or modality-quality procedures as unavailable limitations.

### 3.6.2 Detection analysis

#### Confirmed facts

- The nominal transition anchors are 30 seconds for onset and 90 seconds for completion.
- Trigger data include up to five timestamps and a trigger count.
- NT can support a false-alarm or no-change analysis only if that analysis was actually computed or used.
- Gaze around a trigger may contextualise visual orientation, but gaze alone cannot establish perception or comprehension.
- The [RQ1 analysis contract](../analysis/contract_RQ1.md) contains the current trigger, gaze, lane-positioning, metric, operation, and reporting specification; shared classifications remain in the [pre-processing rules](../analysis/rules_preprocessing.md). Current gaze reporting uses display-looking time, contact durations, contact counts and contacts per minute; display share (%) is retired, while coverage and missingness remain quality diagnostics.
- The supplemental event-specific spatial view uses equal 30-second snapshots after the scheduled transitions: onset `30 <= time < 60 s` and completion `90 <= time < 120 s`. The equal duration standardises the spatial comparison and prevents the onset panel from spanning the next scheduled transition at 90 seconds; it is not the full onset response window, which runs from 30 to 90 seconds.

Source of confirmation: user interview, 2026-07-14; existing Chapter 3 handoff inspected 2026-07-14; validated RQ1 plan decision entry, 2026-08-20.

#### Exact intended chapter insertion or claim

Describe trigger occurrence and timing as the planned or available RQ1 evidence, anchored to the common animation schedule. Use the current [pre-processing rules](../analysis/rules_preprocessing.md) for hit, miss, false-alarm, and gaze-window definitions, and the [RQ1 analysis contract](../analysis/contract_RQ1.md) for metrics, comparisons, uncertainty, and outputs.

For the supplemental spatial gaze figure, explain that onset `30–60 s` and completion `90–120 s` were selected as equal-length post-transition snapshots. State that `30–90 s` remains the full onset-to-completion phase and would answer a different question; the fixed snapshots are not intended to represent the complete onset response opportunity.

### 3.6.3 Discrimination analysis

#### Condition answer and interpretation key

The following table records the expected answers used to score the two discrimination questions and the intended meaning used to interpret the post-task interview. Q1 identifies the visible element; Q2 identifies the graphical change. The interview column is an interpretation key, not a binary questionnaire answer: participants' spoken accounts remain qualitative evidence and must be coded from the post-task transcripts.

| Condition | Correct answer for Q1 (visible element) | Correct answer for Q2 (graphical effect) | Correct answer from post-task interview (meaning of the feature/information) |
| --- | --- | --- | --- |
| NT | None of these | I did not witness any changes | No animated feature or information was presented; static shared-idle baseline |
| V1 | Sun and moon | A day-to-night timelapse | Time of day |
| V2 | Buildings | Landscape changing | Current landscape/geolocation context |
| V3 | A red glowing sphere | A progressive camera close up on the scene | Distance and time to destination / estimated time of arrival; the red sphere represents the arrival point |

These meanings are the intended design mappings, not evidence that participants understood them. Interpretation analysis must compare participants' descriptions with this key while preserving uncertainty, alternative descriptions, and the distinction between immediate trial-level responses and the final post-playback interview.

#### Confirmed facts

- Q1 measured the visible element and Q2 measured the type of change.
- Each item had a binary correctness field and a 1–4 confidence rating.
- Q1 and Q2 can be reported separately from the current data structure.
- Each participant encountered a given animated condition at most once, so individual test–retest reliability for an animated condition cannot be estimated.
- The current [RQ2 contract](../analysis/contract_RQ2.md) adopts paired t-tests of participant mean Q1/Q2 accuracy overall and animated within the cross-outcome Holm-22 family; exact within-condition McNemar accuracy tests use Holm-four; numerical-confidence t-tests retain the expanded Holm-15 family. Earlier sign-test approvals are superseded. See current RQ2 results and the adoption record.

Source of confirmation: user interview, 2026-07-14; existing Chapter 3 handoff inspected 2026-07-14.

#### Exact intended chapter insertion or claim

Describe Q1 and Q2 as separate primary RQ2 measures. Report the adopted paired-mean accuracy, within-condition exact accuracy and numerical-confidence comparisons using their labelled correction families; confidence-by-correctness patterns remain descriptive. State that the tests are post hoc question contrasts, not evidence that confidence predicts correctness; avoid condition-ranking, causal, individual-reliability or probability-calibration claims.

### 3.6.4 Interpretation analysis

#### Confirmed facts

- Immediate trial-level oral responses followed the discrimination questions. `P##_t1`, `P##_t2`, and `P##_t3` identify these condition-linked responses; `P##_z` identifies the separate final post-playback interview corpus.
- Transcription was automatic and all transcripts were in English. The researcher checked the automatic transcripts, conducted and recorded the sessions alone, collected no separate interpretation-confidence measure, and used P## pseudonyms for quotations and reporting.
- The immediate-response analysis uses the post hoc hybrid deductive–inductive [two-layer coding rules](../analysis/RQ3/coding/coding-rules.md). Layer 1 records meaning success, success specificity, or failure type once per participant-trial; Layer 2 records transcript-supported objects, transformations, stages, interpretations, reasons, certainty, and explicit reactions, with exact evidence and timestamp locators.
- The current corpus contains 72 included participant-trials: NT 24 and V1, V2, and V3 16 each. It is provisional and single-coder; earlier independent calibration rounds refined the rules but do not establish reliability for the final assignments.
- The current descriptive package reports Layer 1 outcomes by condition and Layer 2 counts as distinct trials carrying each code. For V1--V3, visual description alone is not meaning success; the response must link the visual to the intended information. NT success instead records condition-consistent baseline recognition.
- Current interpretation inference uses exact paired McNemar tests between the three animations, with eight shared participants per contrast and Holm across three. Full and partial success both score 1. The former Bayesian mixed-effects model and weighted-score supplement are preserved historical evidence; their inferential approval is superseded. See the [RQ3 contract](../analysis/contract_RQ3.md) and current interpretation results.
- The discrimination questions may have primed later descriptions. Immediate responses and final interviews remain procedurally distinct, and no final-interview coding or cross-corpus integration rule has been completed.

Source of confirmation: user interview, 2026-07-14 and 2026-07-15; current [RQ3 contract](../analysis/contract_RQ3.md), coding package, and validated exploratory model inspected 2026-10-01.

#### Exact intended chapter insertion or claim

Describe the immediate-response procedure and current two-layer coding method before reporting results. Present observed condition counts before the adopted paired-test results, distinguish the eight shared participants per contrast from full-condition groups of 16 and animated metaphor decoding from NT baseline recognition, and label inference post hoc and coding provisional and single-coder. Preserve the possible priming effect and do not imply that immediate reports prove perception during driving, that the condition caused understanding, or that final-interview integration has been completed.

### 3.6.5 Cross-cutting measures and evidence integration

#### Confirmed facts

- NASA-TLX, UEQ-family responses, gaze, simulator traces, and final interviews are supporting or cross-cutting sources rather than substitutes for the three RQ-specific outcomes.
- The available data could relate workload, UX, visual orientation, and simulator behaviour to RQ-specific responses, but no integration rule is confirmed.
- A display-directed fixation would qualify the interpretation of a discrimination response; it would not automatically invalidate the response, and gaze away from the display would not prove comprehension.

Source of confirmation: user interview, 2026-07-14; existing Chapter 3 handoff inspected 2026-07-14.

#### Exact intended chapter insertion or claim

Describe these modalities as complementary evidence and state the exact integration rule only if it was used. If no formal integration was performed, say that explicitly and treat cross-modal relationships as unavailable or exploratory rather than as mixed-methods confirmation.

The [adopted Chapter 4 specification](../analysis/inference_ch4.md) also defines the current Holm-22 cross-outcome comparisons: paired participant-mean t-tests overall/animated and exact McNemar in NT. All former inferential approvals outside its five families are superseded; gaze, reaction times, driving behaviour and additional questionnaires remain descriptive in current Results.

## 3.7 Validity, Reliability, and Scope

Status: partially specified

### Confirmed facts

- Trigger presses are overt reports of perceived change, but their timing also reflects motor response, uncertainty, and interpretation of onset or completion.
- Gaze can contextualise visual orientation under a defined coordinate and area-of-interest model, but cannot alone prove perception or comprehension.
- The instruction to keep eyes on the road created a controlled peripheral-exposure test but reduced natural freedom to glance at the display.
- The five-trigger capacity limited the observable response stream and caused two full-session exclusions and replacements.
- Extra presses, missing end presses, and NT presses mean onset and completion cannot be inferred by trigger position alone.
- The discrimination questions may have primed the oral interpretation prompt.
- Researcher-delivered directions, lane/building/street safety corrections, and verbal speed interventions introduced social and cognitive influences. These interventions were not logged. The fixed 50 km/h prototype-speed constraint and lack of real-time Spline–simulator integration limited ecological fidelity. Mild simulator sickness was reported by a few participants but did not lead to session termination.
- Repeated use of one route may introduce learning, anticipation, and fatigue. The incomplete exposure design prevents full within-participant comparison of all four conditions. Residual order effects remain possible because the six sequences were not full counterbalancing.
- Information type, animation form, and abstraction changed together, preventing a pure abstraction claim.
- The mappings were independent of simulated time, location, and destination, limiting ecological interpretation.
- One exposure per animated condition prevents individual test–retest assessment.
- The study supports short, controlled simulator exposure. It does not establish real-road safety, long-term acceptance, habituation, or performance under changing environmental and configuration conditions.

Source of confirmation: user interview, 2026-07-14; existing Chapter 3 handoff inspected 2026-07-14.

### Exact intended chapter insertion or claim

Use the confirmed limitations as the chapter's validity and scope boundaries. Distinguish threats inherent in the design from mitigations that were actually used. Do not claim a mitigation merely because a threat was recognised.
