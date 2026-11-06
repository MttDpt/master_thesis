---
title: Pre-processing Rules
description: Current rules for preparing, excluding, aligning, classifying, and deriving study data.
type: preprocessing_rules
tags:
  - analysis
  - pre-processing
  - rules
---
# Pre-processing Rules

This file is the source of truth for study-data pre-processing rules. It contains rules only: no progress checkpoints, validation status, receipts, dated decisions, or change history.

## Related records

These links are optional routes, not required reading. Open only the record needed for information that is not defined here.

- [Methodology Study Record](../context/methods_study-methodology.md): study setup, prototype, apparatus, procedure, and collected measures.
- [Methods: Data Preparation, Analysis, Validity and Scope](../context/methods_data-preparation.md): methodology-facing account of preparation, exclusions, analysis boundaries, and validity.
- [RQ1 analysis contract](contract_RQ1.md): detection, trigger, gaze, and lane-positioning subquestions and operations.
- [RQ2 analysis contract](contract_RQ2.md): discrimination, correctness, confidence, and comparison subquestions.
- [RQ3 analysis contract](contract_RQ3.md): immediate interpretation, interview, coding, and integration subquestions.

## Source preservation and selection

- Never alter or delete raw study data.
- Organise participant material with P## pseudonyms and never copy identifying fields into derived data or analysis outputs.
- Select one canonical export per participant-trial after checking participant, trial, modality, duration, and content; preserve duplicate, alternate, aborted, and diagnostic recordings outside the working set.
- Do not exclude a short or incomplete-looking trial from duration alone. First determine whether a complete replacement exists and record the selected canonical source in the dataset manifest.
- Use the participant-trial and condition crosswalk rather than filename order or row order when joining modalities.
- For an RQ1–RQ2 comparison, join derived RQ1 trial records to the RQ2 questionnaire record only on `participant_trial_key`, after verifying the participant and condition agree. Retain one row per participant-trial; event-level RQ1 records must never multiply an RQ2 questionnaire denominator. Stop a run on a zero, duplicate, or mismatched join key rather than selecting by row order.
- For the animated-trial combined detection score, derive `D = (onset_detected + completion_detected) / 2` from the existing binary event statuses: both detected = 1, exactly one = 0.5, neither = 0. Retain the separate statuses; missing event status makes D missing, and NT has no applicable score because it has no scheduled animation events. Join each question's original ordinal confidence by the same verified participant-trial key; retain Q1 and Q2 separately.
- For the adopted all-trial comparison, derive a separate operational response score `S`: use `D` for an animated trial; use 1 for an NT trial with zero retained presses across inclusive `0–120 s`, and 0 for an NT trial with any retained press. Missing trigger information makes S missing. Preserve NT onset, completion and D as inapplicable; do not invent NT events or latencies. Retain Q1/Q2 correctness separately and label the oral outcome as condition-appropriate success: animated full-plus-partial intended meaning, NT recognition of the no-animation condition. A full-only sensitivity changes animated interpretation only. Join all measures once per verified participant-trial and retain participant and condition for the repeated-trial comparisons.
- Preserve modality-specific missingness at the participant-trial grain. A missing or inapplicable RQ1 event value does not make a questionnaire response missing, and an NT false-alarm press count remains a secondary trial attribute rather than a questionnaire row or denominator.
- Preserve original-export hashes separately from hashes of derived files. Analyses using the end-aligned simulator files must reconcile against `derived_simulator_sha256` in the [derived simulator manifest](dataset/simulator-data/simulator-data-provenance/derived-simulator-manifest.csv), not against the source-export hash.

## Participant and recording inclusion

- Exclude P00 because it is the pilot session.
- Exclude P06 and P07 from every modality because their trials exceeded the five-trigger recording capacity.
- Include P25 and P26 as the replacements for P06 and P07.
- Exclude the discarded P13 gaze recording identified in the [dataset manifest](dataset/manifest.csv).
- For P12 simulator data, exclude the aborted `_161753` pair and use the complete `_161923` pair.
- Treat the unavailable `P07_t3` transcript as missing without substitution; P07 remains excluded from analysis.
- For RQ3 immediate-response coding, retain one included transcript per crosswalk participant-trial key and use the crosswalk condition for corpus membership, the intended-meaning reference, and all condition-specific denominators. Treat unexpected transcript descriptions as participant responses; do not infer a source mismatch or add a source-consistency flag from response content alone. Investigate a source mismatch only when independent recording or metadata evidence supports it. NT retains a subtle background terrain-colour animation, so an explicit report of that colour change is valid NT detail evidence and must not be treated as a false V1–V3 transition.
- Preserve one Layer 1 trial-code row per included RQ3 participant-trial and zero or more Layer 2 evidence rows, each with exact transcript wording and a participant-trial timestamp locator. For binary interpretation comparisons, derive `success = 1` from Layer 1 `yes` and `success = 0` from `no`; both `full` and `partial` specificity remain successes, while inactive branch values remain `NA`. Never convert missing or unassigned detail codes into failure values, and do not derive model outcomes from Layer 2 codes.
- Preserve the exact validated RQ3 trial-code CSV and its upstream validation receipt used by a statistical run, record their hashes, and include byte-identical copies with the reproducible statistical-test package. Rerun when explicitly authorised, preserving the exact coding input and validation snapshots; descriptive summaries must reconcile to those codes.

## Questionnaire preprocessing and scoring

- Preserve the raw Google Forms exports and use the canonical participant-trial-condition crosswalk to attach NASA-TLX conditions; never infer a condition from row order, trial-response order, or a questionnaire timestamp alone.
- Keep NASA-TLX at one row per participant-trial. Retain the six dimensions as numeric 1–10 values only when the response is a valid recorded number; preserve dimension-level missingness and report the denominator for each summary. The form anchors Performance from “Perfect performance” at 1 to “Failed completely” at 10, so do not reverse-code it. Calculate the overall NASA-TLX score as the unweighted mean of the six dimensions only when all six dimensions are present.
- For the original UEQ, retain one row per participant at post-playback grain. Exclude blank or placeholder participant rows and require numeric 1–7 responses for item scoring; preserve item-level missingness rather than imputing or copying responses across conditions.
- Recode each UEQ item to the standard −3 to +3 direction using the favourable adjective pole: response − 4 when the favourable pole is on the right and 4 − response when it is on the left. Aggregate the verified original-UEQ item mapping into Attractiveness (6 items) and Perspicuity, Efficiency, Dependability, Stimulation, and Novelty (4 items each).
- Do not assign UEQ responses to NT, V1, V2, or V3 and do not duplicate participant-level UEQ scores across trials. Condition-level UEQ comparisons are unsupported unless a future source records the condition evaluated.

- For RQ2, match the aggregate discrimination responses one-to-one to the canonical 72 participant-trial keys and verify participant, trial and condition agreement; stop on zero, duplicate or mismatched aggregate matches. Reconstruct Q1/Q2 correctness from the [approved RQ2 scoring key](contract_RQ2.md#current-definitions); existing score fields are diagnostic and must not override it.
- Pair each question's confidence only with its own correctness, preserving the original 1–4 value. For adopted numerical-confidence comparisons, preserve Q1/Q2 pairing and original 1–4 values; calculate participant means only after the verified join. Never replace the ratings with high/low categories or signs. Equal numerical spacing is an analysis assumption specified in the RQ2 contract. Missing correctness or confidence stays missing and invalid ratings are flagged rather than coerced or imputed. The former high/low coding remains a historical specification only.
- Pair Q1 and Q2 correctness within the same participant-trial for the paired-question analysis; retain participant IDs as grouping/pairing identifiers and the crosswalk condition. After verifying all trial keys, derive one mean per participant over the intended scope (three trials overall, two animated trials); do not replace a participant mean with a pooled event row. For a between-animation interpretation contrast, join the two observed conditions by participant and retain only complete shared pairs; never fabricate an unobserved condition or fill missing interpretation with failure. Report missing pairs and eligible denominators separately for each operation; do not turn missing outcomes into incorrect answers.

## Time alignment and retained intervals

- Use the iPad clock for gaze and trigger alignment.
- Retain gaze and trigger values only within the inclusive `0–120 s` trial interval; ignore values after 120 seconds.
- Before any simulator analysis or trigger join, create the end-aligned derived simulator file: set the final recorded simulator timestamp to trial time `120 s`, calculate `aligned_trial_time = SimTime − (final SimTime − 120 s)` for every row, and retain only `0 ≤ aligned_trial_time ≤ 120 s`. This reverse alignment uses the operationally synchronized trial end to remove the earlier simulator-start offset. Verify monotonic aligned time and the retained 0–120-second span, and record the original and derived hashes plus the alignment values in the derived simulator manifest.
- Use only the end-aligned derived simulator files for analysis and for joins to iPad-clock trigger timestamps; never compare raw `SimTime` directly with an iPad timestamp. Treat any residual manual-stop timing error or clock drift as an alignment limitation.
- Do not interpolate across missing timestamp coverage.

## Trigger classification

- In animated trials, assign the earliest press in `[30,90)` seconds to onset and the earliest press in `[90,120)` seconds to completion. A press at exactly `120 s` is outside the completion window and is therefore not an eligible completion detection.
- Classify the absence of an eligible onset or completion press as an event-specific miss; a completion press at exactly `120 s` is a completion miss.
- Classify presses before 30 seconds as early. Retain an animated-trial press at exactly 120 seconds as a separate `trial_end` boundary record, not as a completion detection or an ordinary extra; classify remaining unassigned animated-trial presses as extra.
- Classify every NT press as a false alarm.
- Retain five-press-cap trials in the primary data and expose the sensitivity-exclusion flag rather than excluding those trials during pre-processing.
- Calculate onset latency from 30 seconds and completion latency from 90 seconds only for matched detections; never assign a latency to a miss.

## Gaze classification and AOI contact construction

- The configured display plane is 3840 × 656 px. Classify a valid in-canvas sample as driver_axis when 0 ≤ X < 1280 px and 0 ≤ Y < 656 px, or as ambient-display AOI contact when 1280 ≤ X < 3840 px and 0 ≤ Y < 656 px. Treat the full ambient-display region as one AOI.
- Use off_display for a sample exported or derived as Invalid or unclassified, including an out-of-canvas sample stored at (0,0). Do not infer off_display from stored coordinates alone, and do not treat it as evidence of road gaze.
- Treat an interval with no recorded sample as missing coverage, not as an AOI class.
- Define an ambient-AOI contact as a continuous run of valid ambient-display samples calculated from observed timestamps. Do not label contacts as foveal, sustained, or brief and do not apply a duration threshold.
- Keep consecutive valid ambient-display samples in the same contact only when each adjacent timestamp interval is at most 25 ms; any longer interval is missing coverage and breaks the contact without becoming off_display. Do not interpolate across a broken contact.
- Calculate gaze-state durations with sample-centred midpoint allocation. For each adjacent sample pair separated by at most 25 ms, split the elapsed interval at its midpoint: assign the first half to the earlier sample's class and the second half to the later sample's class. Clip assigned intervals at the applicable event-window or trial-window boundaries, and assign no duration across gaps longer than 25 ms. Treat the resulting state intervals as half-open `[start, end)`, so a timestamp exactly at a midpoint belongs to the later sample's interval. For any press-state measure, assign the class of the unique sample-centred interval containing the press timestamp; return `ambient_display` or `driver_axis` only for the corresponding valid class, and return `indeterminate` when the timestamp is assigned `off_display`, falls outside an assigned valid interval, or lies within missing coverage or a gap longer than 25 ms. Retain combined valid ambient-display and driver-axis duration for coverage checks and the valid-minute frequency sensitivity; report `off_display` and missing coverage separately.
- For duration/frequency analyses, construct contacts from the full retained trial stream before clipping to the chosen half-open window. Count each ambient-sample run once when it has an ambient sample inside the window or positive allocated ambient duration overlapping it; include a carried-in contact once and flag contacts truncated by either window boundary. Calculate each contact's duration from its assigned ambient midpoint intervals clipped to the window, excluding intervening driver-axis, off-display, and unassigned time. Sum these durations for each window's total ambient duration; calculate the median and maximum across individual contacts for the within-window typical and longest duration, without applying a minimum-duration threshold. In condition summaries, take the median of evaluable window measures; typical contact is therefore the median of within-window medians and uses only evaluable windows with at least one contact (`contact window n`). Retain isolated sample contacts and flag any zero allocated duration.
- Label primary contact frequency **contacts per minute** and calculate it as window contact count divided by the full analysis-window duration in minutes (`60 × contact_count / window_length_s`). Retain contacts per valid allocated gaze minute (ambient-display plus driver-axis duration) as a sensitivity measure on exactly the same evaluable windows. Keep the existing coverage criterion and positive valid-duration requirement for both rates; report valid duration and coverage separately. The primary rate describes recorded contact segments per scheduled minute, not the true contact rate during unobserved time or confirmed intentional glance entries; neither denominator repairs contact fragmentation. An adequately covered window with no contacts has zero total ambient duration, count and frequency; median/longest individual-contact duration is not applicable. With zero valid duration or insufficient coverage, report allocation and contact summaries as indeterminate rather than zero. Use the existing valid-samples/expected-samples coverage criterion separately for every window.
- No fixation-construction algorithm or velocity threshold is approved.
- For detected animated events, use the event anchor through the matched press. For misses, use the event anchor through its scheduled response deadline. In both cases, calculate gaze availability as valid samples divided by the samples expected from interval duration at the nominal 60 Hz rate, following the valid-versus-expected-sample operationalisation in [Niehorster et al. (2026), retained in the cited-source archive](../references/cited-papers.zip). Treat availability at or above 80% as adequate and lower availability as indeterminate. The 80% threshold is an investigator-specified completeness criterion; it has not been directly validated for this event-to-press application. Do not use post-press gaze.
- Current window-level gaze measures are total and median contact duration, longest contact, contact count, contacts per minute, state at press when applicable, and time since the last contact. Do not use display share (%) / ambient-layer share as a gaze descriptor or derive replacement proportions of window time. Preserve existing share fields and historical outputs for provenance only, without deleting or rewriting source data. Keep the existing valid-sample coverage and positive valid-duration requirements; report availability, the `off_display` proportion among recorded samples, and missing-sample count as data-quality diagnostics, not gaze descriptors. Do not derive duration-based attention categories, clusters, or sensitivity thresholds.
- For fixed gaze-phase comparisons in every included condition, calculate each eligible trial's measures separately over `[30,90)` and `[90,120)`, regardless of when an onset or completion press occurred; these clock-fixed windows include gaze after a press. For NT trials, retain full-trial allocation over 0–120 s and calculate the same `[30,90)` and `[90,120)` windows as no-animation clock-matched baselines, not as event phases. NT onset/completion event-to-press/deadline windows are not applicable; do not create pseudo-events or use false-alarm presses as matched detections. For a false-alarm press, derive only the AOI state at that press; do not create an event, latency, or lookback window.

## Simulator sample eligibility

- Retain a simulator sample for the lane-positioning measure only when `laneId != 0`, both signed border offsets are finite, and `laneOffsetRight - laneOffsetLeft > 0`.
- Preserve the signed border offsets. Flag a non-positive signed clearance when `laneOffsetLeft >= 0` or `laneOffsetRight <= 0`; do not convert that flag into a physical lane-departure claim.
- For a matched detection or NT false-alarm press, pair the timestamp with the nearest eligible simulator sample; do not interpolate and retain the press-to-sample time gap.
