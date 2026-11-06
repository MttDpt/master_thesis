---
title: RQ1 Analysis Contract
description: Living subquestion, evidence, metric, operation, and interpretation contract for RQ1.
type: rq_analysis_contract
rq: RQ1
tags:
  - analysis
  - rq1
---
# RQ1 Analysis Contract

## Cross-RQ analysis route

Use the [adopted Chapter 4 specification](inference_ch4.md) and the [mean-score cross-RQ subquestion](contract_RQ3.md#1f-mean-outcome-scores-and-animation-comparisons). Pooled onset–completion uses a paired t-test of 24 participant averages within the 22-test family; within-animation onset–completion uses exact McNemar tests with Holm across three. All other previous inferential routes are historical and superseded; retain their packages without rerunning them for current Results.

## Research-question reference

Use the wording and thesis-level framing in [RQ1: Detection](../context/thesis_backbone.md#rq1-detection). This file does not restate the research question.

## Evidence roles

Trigger responses are the primary evidence. Animated gaze-duration and contact analyses use the entire fixed onset `[30,90)` and completion `[90,120)` periods specified in subquestions 6 and 8, regardless of press timing; outcome-defined event-to-trigger gaze windows are out of scope. Current gaze descriptors are total display-looking time, median and longest contact duration, contact count and contacts per minute; display share (%) / ambient-layer share is retired from reporting. Preserve existing share fields and historical analyses only for provenance. Gaze does not replace trigger detection or establish causality or safety.

## Related records

These links are optional routes, not required reading. Open only what the current subquestion needs.

- [Methodology Study Record](../context/methods_study-methodology.md): study setup, prototype, apparatus, procedure, and collected measures.
- [Methods: Data Preparation, Analysis, Validity and Scope](../context/methods_data-preparation.md): methodology-facing preparation, analysis boundaries, and validity.
- [Pre-processing rules](rules_preprocessing.md): exclusions, source selection, time alignment, trigger classes, gaze classes, fixations, and derived event categories.
- [RQ2 analysis contract](contract_RQ2.md): discrimination and confidence.
- [RQ3 analysis contract](contract_RQ3.md): immediate and retrospective interpretation.

## Data sources

Choose only the source needed for the current subquestion; this list is not a mandatory reading sequence.

| Source | What it provides |
|---|---|
| [72-trial map](dataset/trial-data/trial-data-crosswalk/72-trial-map.csv) | Participant-trial-condition crosswalk and registered source mapping |
| [Trial-level trigger table](dataset/trigger-data/trigger-data-cleaning/trigger_trials.csv) | Detection, latency, press-count, and sensitivity fields |
| [Press-level trigger table](dataset/trigger-data/trigger-data-cleaning/trigger_presses.csv) | Early, matched, extra, and false-alarm press records |
| Dataset registry | Routes to canonical gaze and simulator files and their provenance |
| [Derived simulator manifest](dataset/simulator-data/simulator-data-provenance/derived-simulator-manifest.csv) | Derived simulator paths and hashes |

## Subquestion schema

Every subquestion records: the question; evidence and data; unit of analysis and denominator; measures; operation and comparison; uncertainty and diagnostics; output; and interpretation boundary. Update the current specification in place when a deep dive establishes new information or a decision; do not add dated decision logs.

## Statistical comparison questions

| Question | Current operation |
| --- | --- |
| Is onset detection higher than completion overall? | Paired t-test on 24 participants' two-animation mean event scores; reuse the 22-comparison cross-outcome family. |
| Does onset differ from completion within an animation? | Exact two-sided conditional McNemar on 16 participant-trial pairs for each animation; Holm across three. |
| Which animation is detected faster or receives more gaze? | Descriptive reaction-time and gaze summaries only; earlier models, sign/rank tests and inferential bootstrap contrasts are superseded for current reporting. |

The [current specification](inference_ch4.md) owns correction scopes and supersession.

## Subquestions

### 1. Detection success

- **Question:** How often did participants report the onset and completion of each animated condition?
- **Evidence and data:** trial-level trigger table; triggers are primary evidence.
- **Unit and denominator:** the primary unit is one eligible event, with 16 onset events and 16 completion events in each of V1, V2, and V3; misses remain in these denominators. Secondary pooled summaries use 48 eligible onset events and 48 eligible completion events. Each participant contributes two animated trials, so the participant-level denominator is four eligible events overall, two onset events, and two completion events.
- **Measures:** binary onset detection and completion detection; exact detected count and proportion for every condition-event cell, pooled event type, and participant.
- **Operation and comparison:** summarise each condition-event pair and calculate V1–V2, V1–V3, and V2–V3 percentage-point contrasts separately for onset and completion. Add pooled onset and completion proportions only as an orientation layer. Calculate each participant's overall, onset, and completion detected-event proportions and show which two animated conditions that participant encountered.
- **Diagnostics:** verify condition/event denominators, four eligible events per participant, incomplete exposure, sparse cells and misses. Current inferential uncertainty and p-values follow the adopted paired tests; older between-animation bootstrap intervals remain historical.
- **Output:** exact tables; one condition-by-event detection-success dot-and-whisker figure labelled with detected `n/16`; and a pooled onset/completion table labelled with detected `n/48`. Do not produce a pooled detection figure or anonymous participant-variation figure. Retain contrast tables and participant summaries for audit; a contrast forest figure is not part of the current figure set.
- **Boundary:** pooled values must not conceal condition-specific results. Participant proportions describe this study's four eligible events and must not be treated as stable individual ability scores or participant rankings. A trigger is an overt report of perceived change; it does not establish comprehension, absence of direct inspection, causality, or safety.

- **Current pooled comparison:** form one onset and one completion detection rate per participant across their two animated trials, then compare the 24 paired averages with a two-sided paired t-test. Retain all misses. Reuse this test within the [22-test family](inference_ch4.md); do not add it to the within-animation family.
- **Current within-animation comparison:** use exact two-sided conditional McNemar separately for the 16 exposed participants in each animation, with Holm across three tests. Report paired binary counts and onset-minus-completion gaps. See current RQ1 results and the validated rerun.
- **Supersession:** Bayesian between-animation models, participant-direction/profile tests and inferential bootstrap contrasts are historical only. Detection counts between animations remain descriptive. Unequal event windows, incomplete exposure and order/carryover prevent causal or isolated-salience claims.
Output hit `head -75` cap (75 lines, 22 unique files). The `tail` stage may have had more matches that never reached stdout. For existence checks across many files, prefer `grep -rl PATTERN <dir>` (list files only, no head). For enumeration, drop the `| head` or widen the cap.

==> analysis/contract_RQ1.md <==

### 2. Reaction time

- **Question:** Among detected events, how long elapsed between the scheduled change and the matched press? This is termed **reaction time** throughout RQ1.
- **Evidence and data:** matched onset and completion press times and latency fields in the trial-level trigger table.
- **Unit and denominator:** seconds; matched detections only, reported separately for condition and event.
- **Measures:** onset latency is `matched press time − 30 s`; completion latency is `matched press time − 90 s`. Report the median, first quartile, third quartile, IQR, and pairwise median differences.
- **Operation and comparison:** compare V1, V2, and V3 in one condition-by-event summary figure using each cell's median and IQR. Join onset medians across conditions and completion medians across conditions only as visual guides for their event-specific summaries; they do not represent within-person trajectories or pair individual observations. Never replace a miss with an artificial reaction time.
- **Uncertainty and diagnostics:** report detected-event counts, median, Q1, Q3 and IQR descriptively; retain ties, skew, sparse completion samples and undefined miss latencies. No reaction-time significance test or inferential between-animation contrast is selected for current Results.
- **Output:** exact summary, contrast, and 3-, 5-, and 10-second threshold tables; one condition-by-event reaction-time summary figure with event-specific median markers, IQR bars, and direct median labels; and a supplemental three-panel animated response-interval timeline with 16 anonymous trial rows per condition, onset and completion anchor-to-press segments, and misses in a labelled non-time gutter. Keep the time-area shading but omit its labels from this timeline's legend. Do not produce an ECDF or a descriptive aggregate interval timeline.
- **Boundary:** reaction time describes speed only after detection and cannot represent all eligible events by itself.

### 2a. Paired onset–completion reaction-time inference

The earlier reaction-time sign-test package is historical, superseded for current inference. Report reaction times descriptively under subquestion 2; do not infer equal reaction times from an unselected or inconclusive test.

### 3. Animated early and extra presses

- **Question:** How often did animated trials contain early or extra presses, how did this vary across V1, V2, and V3, and how did these presses coexist with successful or missed reports?
- **Evidence and data:** trial-level trigger table plus press-level early and extra classifications; NT trials are excluded from this subquestion.
- **Unit and denominator:** use one animated participant-trial for prevalence, with 16 trials in each condition. Use one classified press for timing and response-window summaries. Keep trial prevalence and press totals separate.
- **Measures:** binary `any early` and `any extra` trial flags; exact early and extra press counts; exact press time; seconds before the 30-second onset for early presses; onset-response window `[30,90)` versus completion-response window `[90,120)` for extras; retained `trial_end` boundary presses at exactly 120 seconds are reported separately; and the mutually exclusive trial profile `neither`, `early only`, `extra only`, or `both`.
- **Operation and comparison:** report trials with at least one early press and trials with at least one extra press separately for each condition as exact `n/16` counts and proportions. Compare the four trial profiles across conditions. Split extra presses by response window and condition, reporting both prevalence among all 16 eligible condition trials and prevalence among trials with the corresponding event detected. Cross-tabulate the four early/extra profiles against the detection profiles `both detected`, `onset only`, `completion only`, and `neither`, separately by condition.
- **Uncertainty and diagnostics:** keep all comparisons descriptive, using exact counts and proportions without bootstrap intervals, pairwise contrasts, or significance tests. Reconcile press-level totals to trial flags; show sparse or zero cells; and report whether presses are distributed across participants or concentrated in a small number of anonymous participants.
- **Output:** exact source tables; a horizontal condition comparison of separate early and extra trial prevalence; a horizontal 100% stacked response-profile composition (`both detected`, `onset only`, `completion only`, `neither`); a classified animated-press timing-by-condition display spanning 0–120 seconds with early, onset, completion, extra, and separate `trial_end` boundary classes; and the early/extra-profile-by-detection-profile cross-tab as an exact count table rather than a primary graph. The timing display is descriptive raw classified-press evidence, not a within-person trajectory or a reaction-time estimate.
- **Boundary:** early presses occur before onset and cannot be assigned to onset or completion. An extra is an unmatched press within an animated trial; its response-window location does not establish why it occurred. The four-profile composition is a co-occurrence description, not a combined error score, and the cross-tab cannot show that early or extra presses caused detections or misses.

### 4. NT false alarms

- **Question:** How often was a change reported when no animation occurred, how many false-alarm presses occurred, and when did they occur?
- **Evidence and data:** the NT trial-level any-press and press-count fields plus every press-level NT false-alarm record; animated trials are excluded from this subquestion.
- **Unit and denominator:** use one NT participant-trial for prevalence, with 24 NT trials; use one false-alarm press for the timing distribution. First-false-alarm timing is conditional on affected NT trials and must show that smaller denominator.
- **Measures:** NT trials with at least one false alarm; exact total false-alarm presses; false-alarm count per NT trial; exact false-alarm time from 0 to 120 seconds; and first false-alarm time among affected trials.
- **Operation and comparison:** report exact `n/24` prevalence and its complement, the discrete per-trial count distribution including zero, all exact false-alarm times, and the first false-alarm time for every affected NT trial.
- **Uncertainty and diagnostics:** use exact descriptive counts and proportions without bootstrap intervals or significance tests. Reconcile affected-trial prevalence, per-trial counts, total presses, and press times; report whether repeated presses are widespread or concentrated in a few anonymous trials.
- **Output:** exact source tables and concise text stating NT affected-versus-unaffected prevalence, the discrete false-alarm-count distribution, and exact 0–120-second false-alarm timing. Include a count-distribution figure retaining all 24 trials and a false-alarm timing display coloured and shaped by at-press gaze state; keep the 17-press denominator distinct from trial counts.
- **Boundary:** NT remains separate from animated early and extra presses. The 30- and 90-second clock positions are not NT onset or completion events; do not create NT detection, miss, response-window, or latency variables.

### 6. Fixed-period ambient gaze comparison

- **Question:** How do recorded display-looking time and contact frequency vary by condition and fixed phase?
- **Evidence and data:** verified fixed-window gaze tables under the [shared rules](rules_preprocessing.md), including detected and missed trials and adequately covered zero-contact windows.
- **Unit and denominator:** one participant-trial-period; 16 eligible trials per animation per phase and 24 NT whole trials. Report evaluable and indeterminate denominators separately.
- **Measures:** total time is seconds on the display; primary frequency is labelled **contacts per minute**, meaning recorded contacts divided by the full analysis-window duration in minutes, with contacts per valid minute retained as a sensitivity measure on the same evaluable windows. Retain medians and Q1/Q3/IQR.
- **Operation and comparison:** descriptive summaries over fixed onset 30,90), completion [90,120) and NT whole-trial 0–120 s; fixed phases include post-press gaze. No current inferential gaze tests or inferred condition ranking.
- **Diagnostics:** coverage, valid allocated duration, sample gaps, zero-contact windows, contact fragmentation and influential sparse groups; do not impute missing gaze.
- **Output:** existing fixed-period/whole-trial tables and descriptive figures; [RQ1 results.
- **Boundary:** allocation and recorded contact segments do not establish noticing, intentional looks, comprehension, distraction, safety or causality.

### 6a. Participant-paired general ambient-share comparisons

The two-test gaze package is historical, superseded for current inferential reporting. Preserve its definitions and outputs for provenance without adding them to current Results.

### 6b. Exploratory rankings across three gaze measures

The gaze-ranking package and earlier Skillings–Mack/Wilcoxon/bootstrap comparisons are historical, superseded for current inference. Retain descriptive gaze evidence and its coverage limits; do not infer equivalence or a ranking.

### 7. NT gaze context

- **Question:** How much recorded time was spent looking at the ambient display during NT trials, how did full-trial looking time and contact frequency differ between trials with no false alarms and trials with at least one false alarm, and what AOI state was recorded at false-alarm presses?
- **Evidence and data:** NT trigger tables and canonical gaze logs classified using the [pre-processing rules](rules_preprocessing.md).
- **Unit and denominator:** one NT participant-trial for full-trial allocation and false-alarm grouping, with all 24 NT trials retained; one false-alarm press for its at-press state. A trial with no false-alarm presses is a correct-rejection trial; a trial with at least one false-alarm press is a false-alarm trial, while the exact press count remains a separate measure.
- **Measures:** full-trial total ambient duration and contacts per minute of the full two-minute trial; binary correct-rejection versus false-alarm trial group; false-alarm press count per trial; gaze-data availability; `off_display` proportion among recorded samples; and missing-sample count. For each false-alarm press, record whether valid ambient-AOI contact overlaps the press timestamp or the state is indeterminate.
- **Operation and comparison:** use the full 0–120-second NT trial for gaze descriptors. Compare full-trial total ambient duration and contacts per minute between correct-rejection trials and false-alarm trials using exact group sizes, medians, and IQRs; retain indeterminate gaze trials and report them separately rather than as zero. Preserve the exact false-alarm press count per trial and describe press states separately, without invented events, pseudo-latencies, or lookback windows. Do not label either NT group as successful or unsuccessful detection.
- **Uncertainty and diagnostics:** report all 24 NT trials, exact correct-rejection and false-alarm trial denominators, exact press denominators and per-trial press counts, availability, `off_display` proportion among recorded samples, missing-sample count, timestamp gaps, and indeterminate cases. Use descriptive summaries without significance tests.
- **Output:** NT display-looking-time/contact-frequency and false-alarm-at-press tables; a full-trial duration/frequency display comparing correct-rejection and false-alarm trials with exact group sizes, median, IQR, and indeterminate counts; and a false-alarm timing display with ambient-display, driver-axis and indeterminate press states.
- **Boundary:** NT allocation is descriptive context for a trial with no animation. A correct rejection is the absence of a false-alarm press, not a detected event. The NT comparison does not create onset or completion outcomes; its full-trial allocation is not directly comparable with the animated fixed onset and completion periods and does not show that gaze allocation explains or causes a false alarm.

### 7a. Whole-trial gaze in no-animation and animated response groups

- **Question:** How does whole-trial ambient gaze compare between no-animation and the three animations pooled, and between correct and incorrect response groups?
- **Evidence and data:** canonical cleaned gaze logs, included trial crosswalk and cleaned trigger classifications under [preprocessing rules](rules_preprocessing.md).
- **Unit and denominator:** one included participant-trial over `0,120)`; retain 24 NT and 48 animated eligible trials and report evaluable/excluded gaze counts. Each usable animated trial contributes equally to pooled summaries, rather than averaging condition or phase medians.
- **Measures:** whole-trial total ambient duration and **contacts per minute** (recorded contact count divided by the full two-minute trial duration), using the existing whole-window coverage criterion and positive valid-duration requirement. Retain valid-minute frequency only as a sensitivity measure.
- **Operation and comparison:** compare all NT with all animations pooled; separately compare NT no-press correct rejections with animated detections and NT at-least-one-press false alarms with animated misses. Classify animated outcomes separately for changes happening (onset) and changes already finished (completion); reuse each trial's same full-trial gaze measures in these two distinct groupings. Preserve condition-specific supporting summaries.
- **Uncertainty and diagnostics:** descriptive trial-level medians and quartiles only, with exact eligible/evaluable denominators, input identity checks, independent duration reconstruction and reconciliation against existing NT full-trial measures.
- **Output:** [current contact-frequency package, including whole-trial measures, response-group and condition summaries, and validation receipt; the original whole-trial package preserves prior valid-minute outputs and input provenance.
- **Boundary:** response correctness aligns the comparisons conceptually, but false alarms and misses remain different error types. These are pooled descriptive comparisons, not participant-paired tests or causal effects; participants can contribute two animated trials, condition composition and gaze availability can differ between groups, and whole-trial gaze includes time before and after event reports. Neither comparison replaces the separate fixed-phase results.

### 8. Ambient-contact duration and frequency

- **Question:** During the fixed onset-to-completion and completion-to-trial-end periods, how much ambient-display gaze was recorded, how long were individual contacts, and how frequently did contacts occur?
- **Evidence and data:** canonical gaze logs and the verified participant-trial-condition crosswalk, using the [pre-processing rules](rules_preprocessing.md).
- **Unit and denominator:** one participant-trial-period. Each fixed interval, `30,90)` for onset and `[90,120)` for completion, includes 16 eligible trials for each animated condition and 24 clock-matched no-animation trials. Include detected and missed animated trials; report eligible, evaluable, indeterminate, and zero-contact window counts. Do not treat contacts or samples as independent participants.
- **Measures:** total ambient contact duration (s), median individual contact duration (ms), longest contact duration (ms), contact count, and primary contact frequency, labelled **contacts per minute** (recorded contacts divided by the full analysis-window duration in minutes), with contacts per valid allocated gaze minute retained as a sensitivity measure. Within each window, total ambient duration is the sum of the clipped allocated durations of its contacts; typical contact is the median duration of the individual contacts; longest contact is their maximum; and primary frequency is contact count divided by scheduled window minutes. Compare the valid-minute sensitivity on the identical evaluable windows, retaining the existing coverage and positive-valid-duration requirements; report valid-time fractions separately. Use these duration, count and frequency measures as the current gaze descriptors; omit display share (%) from reports, tables, figures and interpretations.
- **Operation and comparison:** calculate duration, count and frequency on exactly the same window for each row. For fixed phases use `[30,90)` and `[90,120)` irrespective of onset or completion press timing; label no-animation as a clock-matched baseline, since it has no animation events. Do not derive outcome-defined event-to-trigger windows; fixed-period summaries include detected and missed trials. Summarise each window first, then report condition-specific medians and first/third quartiles across evaluable windows without pooling contacts or valid duration across participants. For median/longest individual-contact summaries report the smaller denominator of evaluable windows with at least one contact (`contact window n`); `zero contact n` counts evaluable windows with no contacts. Other metrics retain evaluable zero-contact windows, with zero total duration, count and frequency. Condition summaries are medians across evaluable windows; typical contact therefore summarises within-window medians, while its denominator is `contact window n`. Retain Q1/Q3 in source tables and reports; the requested canvas tables display medians only. Provide detected/missed breakdowns alongside combined animated fixed-period summaries. For descriptive cross-insights, compare fixed-phase summaries with exact evaluable denominators; report within-trial duration or contact-frequency differences only for trials evaluable in both fixed phases, preserving the paired denominator; existing paired-share summaries are historical only. Relate these summaries to existing detection counts and detected-event reaction times without a gaze–outcome model or cross-RQ join. No-animation fixed-period source rows remain available for separate clock-matched analyses. In the ambient-contact report and canvas, show NT gaze only once per whole 0–120 s trial, without onset or completion labels.
- **Uncertainty and diagnostics:** keep contact summaries descriptive. Apply the existing 80% valid-sample coverage criterion separately to each fixed period and require positive valid allocated gaze duration. Record valid duration, off-display and unassigned time, gaps over 25 ms, boundary-truncated contacts, isolated samples, zero contacts, undefined duration summaries, and contact fragmentation at missing coverage. Check contact-duration sums against ambient duration and both frequencies against contact count divided by their respective window or valid minutes; reconcile retained descriptors with existing validated outputs where applicable.
- **Output:** use the [current contacts-per-minute package for fixed-period and whole-trial contact-frequency tables, descriptive figure source, summaries and validation; preserve earlier packages as source/provenance. Save reproducible code, contact-level and fixed-period tables, condition summaries, validation findings, and a concise report within [RQ1 provisional](RQ1/provisional/). After validation, update the gaze frame on the user-specified tldraw board with separate `[30,90)` and `[90,120)` tables for the three animated conditions and one `[0,120)` table for no-animation trials; show total and median/longest contact duration, frequency, units, evaluable denominators, and missingness notes.
- **Boundary:** contacts describe recorded ambient-AOI overlap during fixed periods, not verified fixations, perception, comprehension, road gaze, distraction, safety, or a causal design effect. Contacts split by invalid samples or recording gaps are not necessarily separate intentional looks. Scheduled-window frequency describes the recorded count over elapsed time and cannot recover contacts during unobserved time; valid-minute frequency describes the observed usable portion and does not repair fragmentation. Fixed-period summaries include gaze before and after presses and cannot establish that gaze explains detection or reaction time.

### 10. Trigger-aligned lane position

- **Question:** What lane-midpoint deviation was recorded when a participant made a matched detection press or an NT false-alarm press?
- **Evidence and data:** end-aligned derived simulator logs joined through the trial map and matched detection or NT false-alarm press timestamps; the required reverse end-alignment, derived-file provenance, and sample eligibility come from the [pre-processing rules](rules_preprocessing.md). Raw simulator `SimTime` is not an analysis input.
- **Unit and denominator:** metres at one eligible simulator sample per press. Report matched detection presses and NT false-alarm presses separately, with their exact press-level denominators.
- **Measures:** absolute lane-midpoint deviation, calculated as abs((laneOffsetLeft + laneOffsetRight) / 2); the signed-clearance diagnostic; and the time gap between a press and its matched simulator sample.
- **Operation and comparison:** first verify that each derived simulator file was reverse-aligned from its final recorded `SimTime` to the shared 0–120-second trial scale. For press context, join each matched onset/completion detection and NT false-alarm press to the nearest eligible sample by `aligned_trial_time`, without interpolation; retained `trial_end` boundary presses are excluded from this event-press comparison. For the continuous animated-condition display, retain every eligible 0.01-second aligned sample and calculate the timestamp-wise median, first quartile, third quartile, and contributing-trial count separately for V1, V2, and V3. Keep the complete numerical summary, but omit the isolated V1 point at 21.55 seconds from the figure only; do not smooth or interpolate across it. The latest user-requested mean-based recalculation applies the absolute-value formula per eligible sample, calculates the mean per trial-window over inclusive 0–120 s, `30,90)` and `[90,120)` for every condition, and reports M, sample SD, Md and IQR across trial means, with linear-interpolated quartiles. The no-animation shorter windows are clock-matched descriptive periods, not animation phases. This recalculation remains provisional pending reporting approval; preserve the earlier median-of-trial-medians package and its historical outputs. Compare 48 animated versus 24 NT whole trials, V1–V3 separately by phase (16 trials each), and NT whole trials with versus without any retained press. Preserve original means and medians of trial means as supplementary audit values, sample eligibility counts, all pairwise animation differences between group medians by phase and within-animation completion-minus-onset differences between group medians (not medians of paired changes); no inferential tests or trial-order adjustment in the descriptive package. The [earlier lane-distance inferential extension is historical and superseded for current reporting; retain its original outputs without adding lane significance tests. These descriptive summaries remain provisional; see the lane-distance package. Do not calculate pre/post change scores, assign animation events to the clock-matched NT periods, or calculate detected-versus-missed lane comparisons.
- **Uncertainty and diagnostics:** verify source-to-derived hashes, raw final `SimTime`, the alignment offset, monotonic `aligned_trial_time`, and the retained 0–120-second span before calculating lane measures. Report unmatched presses, press-to-sample time gaps on the aligned scale, retained and excluded simulator samples, lane validity, offset signs, lane width, exact denominators, time-specific contributing-trial counts, and the residual possibility of manual-stop timing error or clock drift.
- **Output:** a descriptive press-aligned lane-position table; a distribution figure showing every eligible press with median and IQR by condition and event, with NT false alarms separate; and a provisional continuous three-panel animated-condition trajectory. The trajectory places V1–V3 in one horizontal row on the 0–120-second trial clock, uses 10-second labels with 5-second minor guides, a 0–2 m vertical scale, a timestamp-wise median with outlined IQR ribbon, no in-chart sample-size labels, and shaded pre-onset `[0,30)`, animation-active `[30,90)`, and post-completion `[90,120]` intervals. It does not include NT because those clock positions are not NT events.
- **Boundary:** reverse end-alignment removes the earlier simulator-start offset because simulator recording and the iPad-clock trial were operationally stopped at the shared 120-second endpoint; it does not prove zero manual-stop error or zero clock drift. Lower values describe closer recorded lane centring at a press. This descriptive press context does not establish that an animated phase caused a change, set a safety threshold, measure driver quality, or describe physical lane departure.

### 2a. Detection–timeliness composition

- **Question:** How are eligible animated events distributed across detection and fixed reaction-time intervals?
- **Evidence and data:** the trial-level trigger table, limited to V1, V2, and V3; no press rematching and no early or extra presses.
- **Unit and denominator:** one eligible onset or completion event; 16 events in each condition-event cell and 96 eligible events overall. A miss remains an event with no reaction time.
- **Measures:** one mutually exclusive outcome per eligible event: miss; detected <=3 s; detected >3–5 s; detected >5–10 s; or detected >10 s.
- **Operation and comparison:** use fixed descriptive intervals, separate onset and completion panels, and condition × event source tables. Reconstruct <=3, <=5, and <=10 cumulative counts from the detected bands and reconcile them with the validated threshold table. Participant counts across four eligible events remain audit-only and condition exposure varies.
- **Uncertainty and diagnostics:** exact counts and proportions only; verify each cell sums to 16 and 100%, misses have no reaction time, boundary values at 3, 5, and 10 seconds, and threshold reconciliation.
- **Output:** a provisional horizontal 100% stacked figure and source/audit tables. This reorganises existing detection-success and reaction-time information; it does not introduce a new statistical estimand or replace the raw reaction-time figure.
- **Boundary:** the labels are fixed communication thresholds: `<=3 s` indicates a rapid response, `>3–<=5 s` a short delay, `>5–<=10 s` a moderate delay, and `>10 s` a very delayed response. These unequal-width intervals are descriptive bins, not discovered clusters or validated psychological or driver-performance types; retain the raw reaction-time view as the primary timing representation, and do not treat a miss as a late response.

### 11. Spatial gaze-sample context

- **Question:** Where on the recorded display canvas did valid gaze samples fall across the full trials?
- **Evidence and data:** canonical gaze logs and the 72-trial condition map, using the existing valid in-canvas classification.
- **Unit and denominator:** one valid sample in the inclusive 0–120-second interval; pool samples separately for each condition and label valid-sample and trial totals. Each bin percentage divides its sample count by all retained valid samples in that condition, not participant count or contact duration.
- **Measures and operation:** first retain the unsmoothed two-dimensional histogram over the 3840 × 656 pixel canvas using 80 × 82 pixel source bins. For the reader-facing density map, apply a two-dimensional Gaussian kernel with standard deviation one bin, truncated at three bins, with zero density outside the canvas; then renormalise the smoothed weights within each condition to 100%. Render between bin centres continuously, use one common linear percentage scale, show V1–V3, and mark the existing driver-axis/ambient boundary at x=1280. The bins and smoothing bandwidth are display-resolution choices, not new AOIs or gaze classes.
- **Diagnostics and output:** source bin counts and percentages, smoothed bin weights and percentages, per-trial sample accounting, and one spatial density figure. Verify all valid samples contribute exactly once, reconcile independent raw bin counts, reproduce the Gaussian smoothing by an independent operation, and verify that raw and smoothed condition percentages each sum to 100%. Include all trials without applying an event coverage filter; show excluded sample counts and explain the resulting unequal trial weights. Keep the raw table as the audit surface because smoothing redistributes observed sample mass across neighbouring bins.
- **Boundary:** this full-trial map includes post-press gaze and cannot explain pre-outcome detection. It describes recorded sample location, not fixation density, duration, attention, road gaze, or a participant-weighted condition comparison. Use fixed-period duration and contact measures in subquestions 6 and 8 for current gaze reporting; existing display-share outputs are historical only.

### 12. Standardised post-animation spatial gaze context

- **Question:** Where did recorded valid gaze samples fall during standardised 30-second post-animation windows for onset and completion?
- **Evidence and data:** canonical gaze logs and the 72-trial condition map, restricted to V1, V2, and V3 with the existing valid in-canvas classification.
- **Unit and denominator:** one valid, classified, in-canvas gaze sample. For onset, retain `30 <= time < 60 s`; for completion, retain `90 <= time < 120 s`. Pool samples separately for every condition × event panel and divide each raw or smoothed bin by that panel's retained valid samples. Each panel therefore sums to 100%; early presses do not remove later samples.
- **Measures and operation:** use the same 48 × 8 raw 80 × 82 pixel bins, two-dimensional Gaussian smoothing with standard deviation one bin, radius three bins, and zero density beyond the 3840 × 656 canvas as the full-trial spatial map. Render a 2 × 3 grid with onset then completion rows and V1–V3 columns, with a common magma percentage scale and the existing x=1280 driver-axis/ambient-display boundary. This 30-second spatial-window rule applies only to this figure and its audit tables; it does not change the fixed-period duration/contact measures in subquestion 6, coverage classification, triggers, or lane analysis.
- **Rationale for the fixed windows:** use the first 30 seconds after each scheduled transition (`30 <= time < 60 s` for onset and `90 <= time < 120 s` for completion) so the two spatial snapshots have equal duration and the onset view does not combine the transition with the next scheduled change at 90 seconds. The `30–60 s` choice is therefore a standardisation decision for supplemental spatial context, not a claim that it captures the complete onset response opportunity; the full `30–90 s` interval would answer the different question of what occurred throughout the onset-to-completion phase.
- **Diagnostics and output:** retain downloadable condition × event raw-bin counts and percentages, smoothed weights and percentages, and per-trial recorded, valid, and excluded sample totals. Verify sample membership with a direct integer-bin reconstruction, independently reproduce Gaussian smoothing, reconcile every raw panel total, and verify every raw and smoothed panel sums to 100%.
- **Boundary:** call this recorded valid-sample location during a standardised 30-second post-animation window. It includes samples after an early press by design and is not pre-outcome gaze, fixation density, attention, or an explanation of detection. The fixed-period duration/contact analysis in subquestion 6 supplies current gaze descriptors, while the full-trial spatial map remains context.

## Analytical conventions

- Preserve repeated observations by resampling whole participants with all their observations.
- Bootstrap diagnostics preserve whole participant bundles and use the seed, draw count and missingness handling declared by the current adopted family; the cross-outcome diagnostic uses 200,000 draws and seed 20261014. Former 20,000-finite-draw and earlier seed defaults belong to historical runs and do not override the [current specification](inference_ch4.md).
- Prioritise raw observations, effect sizes, exact denominators and appropriate uncertainty; use only the adopted paired t-test and exact McNemar detection families for current inference. Gaze, reaction times and lane-position summaries remain descriptive.
- Keep onset and completion separate and report all predeclared contrasts rather than selecting favourable ones.
- Reader-facing figures must omit P## and trial identifiers; audit tables may retain P## where necessary.
- Every user-facing graph needs a source table plus visible “How to read this graph” and “Example from this study” text.
- Use **detection success** for the primary matched-event outcome. Use **reaction time** for matched press time minus the scheduled onset or completion, among detected events only; do not use “conditional response latency” in reader-facing RQ1 material.
