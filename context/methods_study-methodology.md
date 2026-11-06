---
type: methodology_study_record
status: active
updated: 2026-10-01
provenance: user-confirmed and study-artifact-derived project context
---

# Methodology Study Record

This is the detailed, evolving record of the realised methodology, prototype, apparatus, study procedure, collected measures, and known limitations. It is project context, not literature evidence or thesis prose. Use it when the current task needs those study facts.

Scope: Sections 3.1–3.5. Data preparation, analysis, validity, reliability, and scope are maintained separately in [Methods: Data Preparation, Analysis, Validity and Scope](methods_data-preparation.md). Figures and diagrams are intentionally out of scope for this interview. No numerical results, statistical tests, effect sizes, or qualitative findings are asserted unless separately confirmed as computed or used.

## Related records

These links are optional routes, not required reading. Open only the record needed for information that is not defined here.

- [Methods: Data Preparation, Analysis, Validity and Scope](methods_data-preparation.md): methodology-facing preparation, analysis boundaries, and validity.
- [Pre-processing rules](../analysis/rules_preprocessing.md): current cleaning, exclusion, source-selection, alignment, and classification rules.
- [RQ1 analysis contract](../analysis/contract_RQ1.md): detection, trigger, gaze, and lane-positioning subquestions and operations.
- [RQ2 analysis contract](../analysis/contract_RQ2.md): discrimination, correctness, confidence, and comparison subquestions.
- [RQ3 analysis contract](../analysis/contract_RQ3.md): immediate interpretation, interview, coding, and integration subquestions.
- [Thesis Backbone](thesis_backbone.md): thesis-level research-question wording and framing.

## Quick navigation

| Need | Go to |
|---|---|
| Study-wide constraints and exclusions | [Global confirmed constraints](#global-confirmed-constraints) |
| Canonical materials and source roles | [Study materials and agent use](#31-study-materials-and-agent-use) |
| RQ-to-method alignment | [Research process and RQ-to-method alignment](#32-research-process-and-rq-to-method-alignment) |
| Workshop | [Exploratory workshop](#33-exploratory-workshop) |
| Display, prototype, stimuli, and implementation | [Prototype and experimental stimuli](#34-prototype-and-experimental-stimuli) |
| Study design, apparatus, participants, procedure, and measures | [Simulator study](#35-simulator-study) |
| Preparation and analysis | [Methods: Data Preparation, Analysis, Validity and Scope](methods_data-preparation.md#36-data-preparation-and-analysis) |
| Pre-processing definitions | [Pre-processing rules](../analysis/rules_preprocessing.md) |
| Validity and scope | [Methods: Data Preparation, Analysis, Validity and Scope](methods_data-preparation.md#37-validity-reliability-and-scope) |
| Unresolved methodology and analysis work | [Open questions](#open-questions) |
| RQ-specific subquestions, metrics, and operations | Matching [RQ1](../analysis/contract_RQ1.md), [RQ2](../analysis/contract_RQ2.md), or [RQ3](../analysis/contract_RQ3.md) analysis contract |
| Thesis-level RQ framing | [Thesis Backbone](thesis_backbone.md) |

## Global confirmed constraints

- P00 was a pilot session and is excluded from the reported study.
- Twenty-six formal sessions were conducted. P06 and P07 exceeded the five-trigger recording capacity and are excluded from all analyses and modalities. P25 and P26 replaced them across all measures. Final analysed n = 24.
- The realised protocol consisted of three trials per participant. Six three-trial sequences were deliberately selected before data collection to balance condition exposure and baseline position. The stale six-block, 24-trial wording in the Google explanation sheet is a spreadsheet typo and is out of scope.
- `VI` for P17 and P23 means `V1`.
- Participants were BMW employees with valid driving licences. No compensation was provided. Final sample: 17 interns, thesis students, or working students; 5 PhD students; 2 full-time employees.
- Vision and colour-vision information was descriptive only and was not used as an eligibility criterion.
- Participants gave verbal informed consent. No written consent form was used. The exact practical NDA process remains unresolved.
- Figures are deliberately deferred and must not generate interview questions in this task.
- The canonical local study-data mirror is `analysis/dataset/`, with item-level Drive provenance and participant/trial mapping in `analysis/dataset/manifest.csv`. `P07_t3` is unavailable: the Drive source contains only a missing-file placeholder, and the user confirmed on 2026-08-20 that the transcript cannot be retrieved.

Source of confirmation for the global constraints: user interview, 2026-07-14.

## 3.1 Study Materials and Agent Use (Deprecated)

This section is deprecated. Use the Dataset Registry for the current, update-in-place index of study-material locations and its routing rules.

## 3.2 Research Process and RQ-to-Method Alignment

### Confirmed facts

- The chapter presents a design-oriented HCI process followed by an empirical simulator evaluation.
- The process has five operational stages: exploratory workshop; feature narrowing and metaphor development; implementation of three animated mappings; controlled simulator study; and organisation of evidence for detection, discrimination, interpretation, and cross-cutting validity analysis.
- RQ1 asks how effectively drivers detect changes in a peripheral ambient display and how much visual attention the display receives. Participant trigger occurrence and timestamps are the primary behavioural evidence; raw gaze coordinates and timestamps provide the related display-allocation evidence.
- RQ2 concerns discrimination. The study collected two post-trial items, one about the visible element and one about the type of change, with binary correctness fields and confidence ratings from 1, guessing, to 4, very sure.
- RQ3 concerns interpretation. Immediate oral responses were recorded after the discrimination items. Trial transcripts use `P##_t1`, `P##_t2`, and `P##_t3`; final interviews use `P##_z`.
- Trial-level oral responses and final interviews were transcribed automatically. The researcher alone conducted and recorded the sessions. No separate confidence rating was collected for interpretation beyond the discrimination-task confidence ratings. Quotations and reporting use P## pseudonyms only.
- The current immediate-response analysis uses a post hoc hybrid deductive–inductive two-layer codebook: one meaning-success outcome per participant-trial plus zero or more transcript-supported response details with exact evidence and locators. The 72-trial assignments remain provisional and single-coder.
- Current binary interpretation comparisons combine full and partial success and use exact paired McNemar tests between animations, with eight shared participants per contrast and Holm across three. The [adopted Chapter 4 specification](../analysis/inference_ch4.md) supersedes earlier Bayesian/sign-test reporting approvals; NT baseline recognition remains distinct from animated metaphor decoding. Original coding and historical model outputs remain preserved.
- The periphery-detection task is linked to RQ1, the discrimination task to RQ2, and the interpretation task to RQ3.
- NASA-TLX, original UEQ, and driving-offset data remain complementary rather than substitutes for the primary RQ outcomes. Final interviews remain separate contextual interpretation evidence because their coding and integration with immediate responses have not been completed.
- Current scoring and analytical decisions are maintained in the [pre-processing rules](../analysis/rules_preprocessing.md) and RQ contracts; unresolved integration decisions remain explicitly deferred.

Output hit `head -75` cap (75 lines, 43 unique files). The `tail` stage may have had more matches that never reached stdout. For existence checks across many files, prefer `grep -rl PATTERN <dir>` (list files only, no head). For enumeration, drop the `| head` or widen the cap.

==> context/methods_study-methodology.md <==
Source of confirmation: user interview, 2026-07-14 and 2026-07-15; existing Chapter 3 handoff inspected 2026-07-14.

## 3.3 Exploratory Workshop

### Confirmed facts

- The workshop lasted one hour and involved 13 internal BMW employees.
- Participants were divided into four groups: three groups of three and one group of four. Each group included at least one senior profile; the wider pool was predominantly junior employees, interns, and working students.
- Task 1 was an eight-minute individual Crazy 8s-style exercise. Each participant was asked to brainstorm eight possible types of information or features for the PHUD, with no predefined categories or limitations.
- Task 2 lasted 12 minutes. Groups reviewed the eight ideas from each member, selected ideas to include, and were explicitly allowed to combine, adapt, or improve them.
- Task 3 lasted 10 minutes. Groups selected features for LOW and HIGH driving scenarios and ranked them by proximity to the driver axis, where 1 meant closest and higher numbers meant further away. LOW was defined as easy, relaxed driving with light traffic and simple roads, where the car might assist with tasks such as lane keeping. HIGH was defined as demanding driving with busy roads and challenging conditions, where eyes remain on the road and hands remain on the wheel.
- Task 4 lasted 20 minutes. Groups transformed the prioritised features into 3D visual concepts that conveyed the same meaning without letters or numbers, using shapes, artefacts, symbolism, sketches, or descriptions on the provided scenario canvas and avoiding the driver-axis section.
- The numbered workshop sequence ended with Task 4. A separate 10-minute group presentation and discussion activity completed the one-hour session; it was not numbered as Task 5 in the participant-facing material.
- Workshop materials or retained documentation included sketches, photographs, and notes.
- The workshop was formative, not an evaluation of the final prototype. It narrowed the candidate space to three features and informed early metaphor development.
- The retained materials documented a map of the groups' candidate feature ideas.
- A four-person review panel voted on the mapped ideas: the researcher, two BMW supervisors, and one KTH supervisor. In thesis prose, report this only as a four-person expert review panel and do not identify affiliations or roles. The reported consensus rule was high consensus for at least three of four votes, mid consensus for two votes, and low consensus for zero votes. The candidate count was corrected in Round 2: the full idea set under discussion contained nine ideas, not six. All nine ideas met the high-consensus threshold.
- The nine ideas reported in the interview were: weather at the destination; music; navigation to the destination, potentially including estimated time of arrival, distance, or delays; general car status; car-status battery; elevation; engine status; an ambient background layer; and time of day.
- The final study used three mappings for feasibility and study manageability. The selected concepts were chosen after testing visual representations for the high-consensus feature candidates and judging their graphic/design quality and their position on a descending or ascending abstraction continuum.
- V1 represented time of day instead of a conventional clock or current-time display, using a sun traversing the scene followed by a moon, stars, and changing sky colour. V2 originated from BMW's altitude-and-terrain widget and was operationalised as geolocation and terrain context, with hills changing into a city setting. V3 originated from navigation and represented distance and time to destination, or estimated time of arrival, rather than a countdown; a progressive zoom ended at a red sphere used as the arrival point.
- The selection was also motivated by practical study burden: more than three animated mappings would have made it difficult for participants to experience the selected conditions within the available study schedule. This is a feasibility rationale, not a claim that every participant experienced every condition in the realised protocol.
- A qualitative, in-depth review with the supervisor considered which selected features would be easiest to express as visual metaphors, what could be adapted, and which features best fit BMW's existing feature set.

Source of confirmation: user interview, 2026-07-15; existing Chapter 3 handoff inspected 2026-07-14; online Overleaf review clarification, 2026-07-18.

## 3.4 Prototype and Experimental Stimuli

### 3.4.1 Display context and design requirements

#### Confirmed facts

- The prototype targeted BMW's panoramic display across the base of the windscreen: an approximately 1.5-metre-wide, 4-to-6-centimetre-high, pillar-to-pillar projection surface.
- The driver-axis region above the steering wheel was protected and not altered because it contains safety-critical driving information.
- The ambient layer occupied the remaining widget region. The broader platform can present speed, navigation, driver-assistance alerts, vehicle status, and entertainment information; the prototype instead used that peripheral area as an ambient communication surface.
- Widgets are selected and arranged on the BMW central display: a QuickSelect menu and long-press interactions support selection and ordering, while an upward swipe projects a selected app onto the panoramic banner. The banner can hold up to six active widgets, and layouts can be stored to the BMW ID.
- The stimuli used non-textual, non-semantic, metaphor-based visual changes in a 3D scene and were intended for peripheral availability without direct foveal inspection.

Source of confirmation: user interview, 2026-07-14; existing Chapter 3 handoff inspected 2026-07-14.

### 3.4.2 Conditions and visual mappings

#### Confirmed facts

- V1 represented time of day instead of a conventional clock or current-time display: a sun moved across a dune-like scene, the sky changed, and a moon and stars appeared.
- V2 represented geolocation and terrain context by adapting BMW's altitude-and-terrain widget: hills collapsed and cylindrical city-like forms rose. Its intended meaning was the landscape context through which the driver was currently travelling, although the experimental implementation was not connected to the simulator's live terrain or location.
- V3 represented distance and time to destination, or estimated time of arrival, rather than a countdown: the camera progressively zoomed towards a dune and revealed a glowing red sphere as the arrival point.
- NT was a static baseline: the shared idle scene remained visible and did not animate. NT was not an absent-display condition.
- The mappings were independent of simulated time, location, and destination. They did not report live vehicle state.
- The three animated conditions were intentionally different in information type, visual form, and abstraction. These factors were not independently manipulated, so condition comparisons cannot isolate a pure abstraction effect.

Source of confirmation: user interview, 2026-07-14; existing Chapter 3 handoff inspected 2026-07-14; online Overleaf review clarification, 2026-07-19.

### 3.4.3 Animation timing and abstraction

Output hit `head -75` cap (75 lines, 47 unique files). The `tail` stage may have had more matches that never reached stdout. For existence checks across many files, prefer `grep -rl PATTERN <dir>` (list files only, no head). For enumeration, drop the `| head` or widen the cap.

==> context/methods_study-methodology.md <==
#### Confirmed facts

- Animated stimuli followed a common 120-second schedule: 30 seconds idle, 60 seconds transition, 30 seconds final state, then blackout.
- The schedule supplied nominal transition onset at 30 seconds and nominal transition completion at 90 seconds for trigger matching.
- The initial 30-second idle period allowed the driver to focus on the driving task and made the onset less predictable; the display was intentionally unchanged immediately after trial start.
- The 60-second transition was selected to give drivers enough time to notice that something was changing while avoiding an overly short animation.
- The final 30-second stable period allowed time for a driver to notice that the animation had ended and press the end trigger despite continuing to drive.
- At the end of the 120-second trial, the PHUD blacked out and displayed no further visual content. The researcher then stopped the simulator and stopped the iPad clock, which also stopped gaze recording; no gaze data were collected after trial termination.
- P00 was a pilot and is excluded from the reported study; no pilot result is inferred from that fact.

Source of confirmation: user interview, 2026-07-15; existing Chapter 3 handoff inspected 2026-07-14.

### 3.4.4 Implementation and integration

#### Confirmed facts

- Separate ProtoPie projects handled the participant-facing PDT response surface on the iPhone and the researcher-facing timer and recording controls on the iPad.
- Only the green right-hand area of the participant iPhone interface was touch-sensitive for PDT responses; presses elsewhere on the screen did not register a response.
- The iPad received PDT signals, recorded timestamps, displayed the trial timer and controls, and could store at most five response timestamps per trial.
- A Python script using the Tobii SDK started and stopped gaze recording.
- The visual prototype was first developed in Unity 6, but the project shifted to Spline because Spline enabled faster iteration and implementation while making the desired aesthetic and visual-effects quality achievable within the project timeline.
- Spline did not have a numbered version applicable to the study because it was a cloud-based web editor updated through rolling feature releases.
- The researcher edited the 3D scene in Spline and played it directly rather than exporting a scene file. An OBS-like streaming bridge connected the computer setup and loaded the scene directly to the Driver Simulation PC and display; the exact bridge software and configuration remain unknown.
- The researcher manually started the relevant scene and transition for every trial.
- The scheduled visual condition was presented while the simulator route ran.
- Trial termination was operationally synchronized by the researcher: when the iPad clock reached two minutes, the gaze recording stopped with the clock and the researcher stopped the simulator, which stopped vehicle recording. The PHUD had blacked out at the planned trial end.
- Display resolution is not currently available and is explicitly flagged for later recovery.
- The researcher started the simulator first. After a short, unmeasured delay of a few seconds, the researcher started the iPad clock and visual-animation timeline together; starting the iPad clock also started gaze recording. Trigger timestamps and gaze timestamps therefore share the iPad timeline. Simulator recording began earlier and uses its own timeline. The manual offset between the simulator and iPad timelines was not measured or automatically verified.

Source of confirmation: user interview, 2026-07-15 and 2026-07-22; existing Chapter 3 handoff and backbone inspected 2026-07-14; online Overleaf review clarification and supplied interface images, 2026-07-21.

## 3.5 Simulator Study

### 3.5.1 Experimental design and conditions

#### Confirmed facts

- The realised protocol consisted of three trials per participant.
- Each included participant experienced NT once and two different animated conditions.
- Six three-trial sequences were selected before data collection and assigned to four included participants each:
  - `NT--V3--V2`
  - `V3--NT--V2`
  - `NT--V3--V1`
  - `V3--NT--V1`
  - `V1--V2--NT`
  - `V2--V1--NT`
- This yielded 24 NT exposures and 16 exposures each for V1, V2, and V3.
- The sequence plan balanced total condition exposure and the position of NT, but did not include every possible order and was not full counterbalancing. Full counterbalancing was infeasible because the project could not recruit the additional participants within the available study time; this was a recruitment and scheduling constraint, not a statistical-power rationale.
- `VI` in the first trial of P17 and P23 is a typographical label for V1.
- The stale six-block, 24-trial wording in the explanation sheet must not be used as a protocol, rationale, or analysis basis.

Source of confirmation: user interview, 2026-07-14; existing Chapter 3 handoff and backbone inspected 2026-07-14.

### 3.5.2 Apparatus and test environment

#### Confirmed facts

- The study used a driving-simulator cockpit with the panoramic display.
- The simulator environment was BMW's in-house SPIDER framework. The local BMW Simulation Centre presentation describes SPIDER as a modular in-house driving-simulation framework with intelligent-traffic, vehicle-dynamics, sound, and control modules, and with OpenDRIVE, OpenCRG, and Open Simulation Interface connections. These centre-wide descriptions are contextual and do not establish the exact thesis simulator hardware.
- A representative P23 SPIDER recording sidecar identifies the version as `2025.03.06-28567-g97027f92e9-R2025-1`, the configuration file as `Unreal.Dsx`, the road description as `Runtime/Project/UIUX2020/Course/Course.xodr`, and the motion configuration as `Runtime/Project/UIUX2020/Motion/MMI_Guiding_Unreal.Motion`. The metadata reports `MegaCity [2]` as the start position and a 0.01-second simulator cycle time.
Output hit `head -75` cap (75 lines, 60 unique files). The `tail` stage may have had more matches that never reached stdout. For existence checks across many files, prefer `grep -rl PATTERN <dir>` (list files only, no head). For enumeration, drop the `| head` or widen the cap.

==> context/methods_study-methodology.md <==
- The eye tracker was a Tobii Pro Spark mounted in front of the driver, to the right of the steering wheel from the driver's perspective, rather than directly facing the driver. Viewing distance and camera angle are unavailable. It recorded timestamped gaze coordinates during each trial.
- The Tobii Pro Spark was operated at 60 Hz. At the start of each session, every participant completed the device software's built-in calibration tutorial. Calibration was repeated if it did not pass.
- Tobii's official product documentation lists 60 Hz default or 33 Hz operation, binocular calibration, timestamped gaze outputs, and integrated tracker-to-client synchronisation. These product capabilities contextualise, but do not replace, the study-specific 60 Hz and built-in calibration procedure above.
- A phone mounted centrally on the steering wheel was the participant trigger.
- Each trigger press sent a signal to a ProtoPie project on the researcher's iPad, which displayed the countdown and stored up to five timestamps.
- A Python script using the Tobii SDK controlled gaze recording.
- Each continuously recorded gaze sample has `Timestamp_ms`, `X`, `Y`, `GazeSource`, and `Status`. `GazeSource` can identify `Merged`, `RightEye`, or `LeftEye` input. The configured display coordinate area is confirmed as 3840 by 656. Valid points inside that area retain their coordinates. The user confirmed that samples exported or derived as `Invalid`/`unclassified`, including out-of-canvas samples stored at `(0,0)`, mean that the participant was not looking at the configured display; this does not distinguish road gaze from another off-display target. A timestamp interval with no recorded sample remains missing coverage. The physical display dimensions, coordinate units, and coordinate reference remain unknown.
- The gaze fields support comparison of the driver-axis region above the steering wheel with the ambient two-thirds of the display, alongside broader gaze-pattern analysis for RQ1. Current gaze classifications are maintained in the [pre-processing rules](../analysis/rules_preprocessing.md), while measures and operations are maintained in the [RQ1 analysis contract](../analysis/contract_RQ1.md).
- Gaze timestamps were aligned with the researcher iPad clock. The Tobii SDK or software version is unavailable.
- Simulator logs contained `SimTime`, simulation-vehicle world `x`, `y`, and `z` coordinates in metres, `laneOffsetLeft`, `laneOffsetRight`, and `laneId`. Speed, steering angle, acceleration, and braking were not logged directly. The sidecar defines `laneOffsetLeft` as the offset to the left lane border, with left relative to object orientation and stored as a negative value; `laneOffsetRight` is the offset to the right lane border, with right relative to object orientation and stored as a positive value. `laneId` is the current lane identifier, with 0 meaning no valid lane, negative values right lanes, and positive values left lanes. The prior centreline interpretation is superseded and must not appear in Chapter 3.
- The route was a shared urban city setting with no simulated traffic and a plain daytime condition. It comprised four turns followed by roundabout entry and first-exit departure. Driving the full route at the intended stable 50 km/h pace took longer than two minutes, so each trial used the same route but stopped at the fixed two-minute boundary rather than completing it. The user-provided route image documents this common route; it is procedural evidence, not a requested thesis figure.

Source of confirmation: user interview, 2026-07-15; representative P23 SPIDER sidecar and CSV accessed from the driving-simulator Drive folder 2026-07-15; local SPIDER sidecar inspected 2026-07-15; official Tobii product page accessed 2026-07-15; BMW SPIDER clipping inspected 2026-07-15; existing Chapter 3 handoff and backbone inspected 2026-07-14; online Overleaf review clarification, 2026-07-18; user-confirmed `unclassified` semantics, 2026-08-29.

### 3.5.3 Participants and procedure

#### Confirmed facts

- P00 was a pilot and excluded.
- Twenty-six formal sessions were conducted.
- P06 and P07 exceeded the five-trigger recording capacity and were excluded from all analyses and modalities.
- P25 and P26 replaced P06 and P07 across all measures.
- Final analysed n = 24.
- All participants were BMW employees with valid driving licences. No compensation was provided.
- The final sample comprised 17 interns, thesis students, or working students; 5 PhD students; and 2 full-time employees.
- Formal-study participants were recruited through invitations on internal BMW communication channels and word of mouth.
- The design target was 24 analysable participants, a multiple of six matching the six planned condition sequences. The six-sequence cycle was repeated after the sixth participant assignment.
- The target was constrained by a seven-working-day collection window with approximately five hours per day and participant availability. This was a feasibility rationale, not a statistical power calculation.
- Twenty-six formal sessions were ultimately conducted. The relationship between the 24-person design target and the 26 sessions is accounted for operationally by the confirmed exclusion of P06 and P07 and replacement by P25 and P26; no separate power rationale is claimed.
- Vision and colour-vision information was descriptive only, not eligibility criteria.
- Participants received a study briefing, gave verbal informed consent, and completed a demographic questionnaire. No written consent form was used.
- No participant withdrawal process was used or recorded.
- All BMW employees were already covered by an NDA as part of their employment contract. No additional study-specific NDA process was applied.
- Participant names were removed and replaced with pseudonymous identifiers such as P01, P02, and so on. Whether a re-identification key was retained is not confirmed.
- Questionnaire answers were received in the researcher's Google account. Gaze and driving-behaviour metrics, audio, and transcripts were stored on the local PC.
- No retention or deletion policy is known or recoverable from the interview.
- No ethics, legal, privacy, or internal governance review or approval is known or recoverable.
- No re-identification key was retained.
- No separate withdrawal procedure existed beyond the offered but unused option to stop; no participant withdrew.
- No additional data-retention or deletion instruction was known or recoverable.
- Familiarisation lasted approximately three minutes.
- Familiarisation used the same urban scenario but a different route from the experimental trials. It introduced the ambient display, let participants practise the phone-trigger procedure, and allowed them to adjust to the fixed displayed speed and expected researcher speed prompts.
- Before driving, participants were instructed only to notice display changes and answer afterward. They were not told what any specific animation represented before or during the trials. The researcher used generic examples to explain the trigger task: press when a visual change begins, and press again when the scene stops changing and reaches a stable state. No feature-specific example, such as buildings meaning a city setting, was provided.
- At the beginning of each session, the researcher gave a short meet-and-greet presentation explaining the research goal and study instructions, without disclosing the animation meanings or intended effects. Participants could ask questions and clarify doubts before driving.
- The introductory briefing was substantially identical across participants.
- Each participant completed three two-minute trials on the same urban route, following researcher-delivered turn-by-turn directions.
- Each participant received the assigned three-trial sequence exactly as planned, with no known order deviations.
- Instructions were to keep eyes on the road and use peripheral vision for the display. The prototype speed was fixed at 50 km/h because no real-time connection between Spline and simulator data was implemented. The researcher monitored simulator telemetry and asked participants to slow down whenever they exceeded 50 km/h. Speed-up reminders were not part of the realised procedure.
- The researcher knew the scheduled condition and animation timing during each trial. Animated conditions followed the fixed 30-second idle, 60-second transition, and 30-second final-state timing; NT had no animation.
- During trials, the researcher gave safety and route-control reminders when needed, including staying in the correct lane, avoiding the opposite-direction lanes, and avoiding buildings or unintended streets. These were researcher interventions, not standardised experimental stimuli.
- Speed and safety interventions were not logged.
- Participants pressed the phone trigger at perceived animation onset and perceived animation end. No press was required when no change was perceived.
- At the end of each two-minute trial, the display blacked out and the simulator and iPad-controlled gaze recording stopped. NASA-TLX and the two discrimination items with confidence ratings were alternated in order across participants and trial tasks; the oral interpretation prompt followed both.
- The study's independent or controlled inputs were the scheduled visual condition and its fixed timing, the standardized route and turn-by-turn instructions, and the no-animation NT baseline. The dependent or collected outcomes were periphery-detection/trigger scores, raw gaze orientation, lane-offset and simulator traces, NASA-TLX scores, discrimination scores, interpretation answers, and original-UEQ responses. Current scoring rules are maintained in the [pre-processing rules](../analysis/rules_preprocessing.md) and matching RQ contracts; unresolved rules remain explicitly marked there.
- After trial 3, the researcher replayed the visual conditions without active driving. The participant completed the original UEQ and a recorded semi-structured interview.
- Participants were offered breaks and the option to stop, but neither was used in the formal sessions.
- A few participants reported mild simulator sickness, but no report warranted stopping the simulation.
- No manipulation checks, calibration-quality records beyond the device calibration procedure, or formal protocol-consistency checks were recorded.

Source of confirmation: user interview, 2026-07-14 and 2026-07-16; existing Chapter 3 handoff and backbone inspected 2026-07-14; online Overleaf review clarification, 2026-07-18.

### 3.5.4 Measures and data sources

#### Confirmed facts

- Trial-level sources included participant triggers, gaze coordinates and validity fields, simulator traces, NASA-TLX dimensions, discrimination responses and correctness, confidence ratings, and oral interpretation transcripts.
- Participant-level or post-study sources included demographics, original-UEQ responses, and final semi-structured interview transcripts.
- Discrimination correctness was stored as binary 0 or 1.
- Confidence was stored from 1 to 4, from guessing to very sure.

#### Analysis-derived confidence result (provisional; 2026-10-09)

- In 16 paired participants per animation, mean Q1 (element identification) and Q2 (change identification) confidence were respectively 3.69 and 3.31 for sun-to-moon (V1), 3.81 and 2.94 for buildings (V2), and 3.56 and 2.19 for red-sphere (V3), on the recorded 1–4 scale. Under paired t-tests with Holm correction across 15 tests considered in the exploratory chat, the Q1–Q2 differences were inconclusive for V1 and higher for Q1 for V2 and V3; the existing cumulative-logit mixed model produced the same outcomes for those three contrasts. See the within-animation confidence analysis and validation and its [expanded multiplicity family](../analysis/RQ2/provisional/statistical-tests/20261009-within-animation-confidence/expanded_family15.csv).
- These are analysis-derived, post hoc findings, not a change to the realised study procedure or selected RQ2 Results. They describe reported confidence in answers, including incorrect answers; they do not show that recognition was correct, imply causation, or establish equality for inconclusive comparisons. Numerical-score interpretation assumes conventional equal spacing; ordinal-model estimates remain conditional on their model assumptions.
- Six NASA-TLX dimensions were recorded on a 1–10 scale: mental demand, physical demand, temporal demand, performance, effort, and frustration. No NASA-TLX analysis or aggregation rule has yet been chosen; it is intentionally deferred pending later selection of an appropriate analysis approach.
- The post-study instrument was the original UEQ: 26 bipolar adjective pairs rated on a seven-point scale. It is neither UEQ-S nor UEQ+. Its six-scale scoring route, item recoding, aggregation, and benchmark use remain to be applied during analysis.
- Gaze was retained and used as raw coordinates plus timestamps, rather than through an already-defined area-of-interest or fixation-detection procedure. It was intended to assess display-versus-road orientation for RQ1; the later classification rule remains to be defined.
- The attached driving CSV `_20260311_160838.csv` has seven semicolon-separated columns: `SimTime`; vehicle world `x`, `y`, and `z` coordinates; `laneOffsetLeft`; `laneOffsetRight`; and `laneId`. Speed, steering angle, acceleration, and braking are not logged directly. Selection of a specific available variable or derived outcome for analysis is intentionally deferred.
- Measure roles are currently classified as follows: the periphery-detection task is primary for RQ1; the discrimination task is primary for RQ2; immediate post-trial interpretation is primary for RQ3; raw gaze is contextual for RQ1; NASA-TLX, original UEQ, and driving-offset data are complementary to the RQs. RQ3 immediate-response coding and exploratory condition modelling are specified; final-interview analysis and cross-source integration remain unresolved.
- Independent or controlled inputs were the scheduled visual condition and fixed timing, the standardized route and turn-by-turn instructions, and the NT no-animation baseline. Dependent or collected outcomes were periphery-detection/trigger scores, raw gaze orientation, lane-offset and simulator traces, NASA-TLX scores, discrimination scores, interpretation answers, and original-UEQ responses.

Source of confirmation: user interview, 2026-07-14 and 2026-07-15; existing Chapter 3 handoff and backbone inspected 2026-07-14; duplicate gaze CSV inspected 2026-07-15; online Overleaf review clarification, 2026-07-18; user-provided original-UEQ Google Form inspected 2026-07-22.

## Open questions

Use this checklist only for unresolved methodology facts. Current pre-processing definitions and RQ-specific analytical specifications live in the [pre-processing rules](../analysis/rules_preprocessing.md) and matching [RQ1](../analysis/contract_RQ1.md), [RQ2](../analysis/contract_RQ2.md), or [RQ3](../analysis/contract_RQ3.md) analysis contract.

### Analysis and data preparation

- [ ] Which still-unresolved scoring or evidence-integration rules remain after applying the current pre-processing and RQ contracts?
- [ ] What additional missingness, retake, outlier, extra-trigger, ambiguous-pair, or incomplete-trial rules are needed beyond the confirmed P00/P06/P07 exclusions?
- [ ] What cross-device alignment procedure, if any, is available for simulator, visual-animation, iPad, and gaze timelines?
- [ ] What gaze validity, interpolation, coordinate-reference, and area-of-interest rule is appropriate outside the validated RQ1 specification?
- [ ] Which simulator variables or derived lane-centering measure will be selected, and how will its diagnostics be documented?

### RQ2: discrimination

- [ ] Will Q1 and Q2 be analysed separately or combined; if combined, what is the exact rule?
- [ ] Which condition and trial-order comparisons will be made?
- [ ] How will confidence be analysed: by correctness, item, condition, or another grouping?
- [ ] What does reliability mean in this analysis, given that individual animated-condition test-retest cannot be estimated?
- [ ] What tests, effect sizes, uncertainty reporting, and missing-response treatment will be used?

### RQ3: interpretation

- [x] Immediate responses use the documented post hoc hybrid deductive–inductive two-layer coding frame.
- [ ] Will the provisional full-corpus assignments receive a second-coder or structured-review pass; if so, how will revisions be reconciled and versioned?
- [ ] What coding, dependability, stopping, and quotation-selection rules will govern the final interviews?
- [ ] How will immediate responses, final interviews, and any quantitative context be integrated?

### Secondary measures, integration, and validity

- [ ] How will NASA-TLX dimensions be scored, aggregated, grouped, and reported?
- [ ] How will original-UEQ items be recoded, scaled, aggregated, and benchmarked?
- [ ] What statistical analyses, if any, will be used for cross-cutting measures?
- [ ] What rule will determine whether quantitative and qualitative evidence agrees, conflicts, or only qualifies another modality?
- [ ] Which acknowledged validity threats are accepted limitations, which are mitigated, and what later documentation is needed for researcher interventions, gaze and simulator quality, demand or priming, and qualitative dependability?
- [ ] Are any manipulation checks, calibration-quality records, or protocol-consistency checks recoverable beyond the procedures already documented?
