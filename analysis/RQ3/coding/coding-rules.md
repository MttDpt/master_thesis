---
title: RQ3 Transcript Coding Rules
description: Provisional two-layer coding structure for immediate post-trial interpretation transcripts.
type: rq3_coding_rules
status: provisional
tags:
  - analysis
  - rq3
  - coding
---

# RQ3 Transcript Coding Rules

These rules separate the overall success of an interpretation from the details that explain what participants noticed and how they understood it. One participant-trial transcript is one Layer 1 record; Layer 2 permits multiple details from the same transcript.

## Layer 1: Meaning success

Layer 1 determines whether the response matches the intended meaning of an animated condition or correctly identifies the NT state. NT success includes either reporting no meaningful animation or correctly describing the continuous baseline landscape colour shift without inventing a separate visual metaphor. For V1--V3, naming a visible object, colour, movement, or transition is not sufficient by itself: the participant must explicitly, or through a direct answer to the meaning prompt, link what was shown to the intended information.

| Code | When used | Values | Example |
|---|---|---|---|
| `success` | Every included transcript | `yes`, `no` | V1 “it represents time passing” → `yes`; V1 “the sun moved and the moon appeared” without a meaning → `no`; V3 “warning” → `no`; NT “nothing changed” → `yes` |
| `specificity` | Only when `success = yes` | `full`, `partial` | V3 “distance and time to destination” → `full`; “approaching the destination” → `partial` |
| `failure` | Only when `success = no` | `alternative`, `unknown`, `false-change` | V3 “warning” → `alternative`; V3 “I have no idea” → `unknown`; NT “the mountains moved” → `false-change` |

Use `NA` for the inactive branch: `failure = NA` when `success = yes`, and `specificity = NA` when `success = no`.

For `specificity`, use `full` when the intended information is clearly identified. Use `partial` when the answer reaches the correct meaning domain but only states a broad or visually literal state, such as “get dark” or “day-to-night landscape,” without clearly explaining the information conveyed. A tentative intended meaning that the participant says may have been suggested by the questionnaire is also `partial`. Keep meaning specificity separate from accuracy of visual details.

Every assigned Layer 1 code must carry:

| Support field | Value | Example |
|---|---|---|
| `evidence` | Exact transcript wording supporting the code | “It was like an animation from day to night.” |
| `locator` | Participant-trial key and timestamp | `P22_t3 00:07–00:35` |

### Intended reference

| Condition | Success criterion |
|---|---|
| V1: Sun and moon | Time of day, day–night transition, or passage of time |
| V2: Buildings | Current location, surroundings, terrain, or urban/environmental context |
| V3: Red sphere | Destination progress, remaining distance or time, estimated arrival time, or approaching arrival |
| NT: No intended animation | Reporting no meaningful animation or correctly describing the continuous baseline landscape colour shift; this is a condition-consistent NT outcome, not decoding a visual metaphor |

## Layer 2: Response details

Layer 2 explains the path from seeing the visual content to interpreting it. Codes are multi-label where the transcript supports more than one value.

| Code | Values | Example |
|---|---|---|
| `object` | `sun`, `moon`, `stars`, `sky`, `hills`, `buildings`, `city`, `sphere`, `landscape`, `other`, `none` | `object: sphere [accuracy: full]` |
| `transformation` | `movement`, `appearance`, `disappearance`, `growth`, `zoom`, `colour`, `transition`, `none` | `transformation: zoom [accuracy: partial]` when scale change was noticed but not fully described |
| `stage` | `start`, `process`, `end`, `unclear` | `end` when the participant noticed only the final red sphere |
| `interpretation` | `time`, `location`, `destination`, `warning`, `weather`, `fatigue`, `entertainment`, `notification`, `assistant`, `other`, `none` | `warning` when the red sphere was understood as caution or danger |
| `reason` | A link from mentioned visual cues to an `interpretation` code; retain alternatives and whether a cue was inferred or rejected | `object:sphere + transformation:colour → interpretation:warning` |
| `certainty` | `sure`, `unsure`, `unknown`; confidence in the interpreted meaning, not in whether a visual event occurred | `unsure` for “Maybe it means we are entering a city”; `unknown` when no meaning is offered |
| `reaction` | `distracting`, `calming`, `decorative`, `confusing`, `glitch`, `useful` | `glitch` when a visual transition was described as looking unintended; leave this code unassigned when no reaction is explicitly stated |
| `evidence` | Exact transcript wording supporting the detail | “Probably some kind of warning because it was orange.” |
| `locator` | Participant-trial key and timestamp | `P13_t2 00:47` |

### Accuracy qualifier

`accuracy` is not a standalone code. Attach it to each coded `object` or `transformation` value except `none`; `none` has no accuracy qualifier:

| Qualifier | Meaning | Example |
|---|---|---|
| `full` | The reported detail matches the displayed object or transformation | `object: buildings [accuracy: full]` |
| `partial` | The participant recognised part of the detail but omitted or blurred an important component | `transformation: zoom [accuracy: partial]` |
| `incorrect` | The participant named a different object or transformation | V3 `object: sun [accuracy: incorrect]` |

When multiple objects or transformations are reported, assign `accuracy` separately to each value.

### Calibration clarifications

- **Condition reference:** Use the canonical crosswalk condition as the intended reference. A participant who names another visual element or meaning may have misinterpreted the trial; do not infer a transcript-source mismatch from the response alone.
- **Stage:** Leave `stage` unassigned when no change was noticed. Use `unclear` only when a change was noticed but its phase cannot be identified. When several phases are explicitly described, code each supported phase rather than selecting only one dominant phase.
- **Objects and colour:** When a participant says “sun or moon” without distinguishing them, retain the alternatives and mark each object `partial`; the uncertainty does not turn either into a fully identified object. A generic shape such as “ball” is also `partial` recognition of a displayed round object, not an incorrect `other` object. Code `city` or `landscape` as an object when the participant describes that scene as seen; do not add it as a seen object when it is offered only as a questionnaire-influenced explanation. Treat a reported glare as colour information, not an `other` object.
- **Transformations:** NT retains a subtle background terrain-colour animation: the colour may change slightly and can look as though colour is moving. An explicit NT background-colour change is therefore `colour` with `full` accuracy, not a false V1–V3 transition; keep an imprecise colour-motion account partial and do not infer colour from a generic unspecified change. The participant-viewed V2 buildings included grey and orange forms; reports of that colour change or of orange buildings becoming more intense support `colour` with `full` accuracy. An orange-to-red glare supports `colour`. An uncertain report of rising or sharpening light supports `appearance` with `partial` accuracy, even if the participant may have missed the full visual change. “Buildings emerge from underground” supports `appearance` with `full` accuracy. A generic mention of an “animation” supports `appearance` and `movement`; if no onset or motion details are given, mark those transformation details `partial` and do not invent a direction. A correctly reported movement together with a time-of-day change supports a `full` `transition` even when the participant is unsure whether the meaning is sunset or sunrise. If the transition is only inferred and the participant says they may have missed the visual change, mark `transition` `partial`.
- **Reasons:** Preserve “or” when the participant offers alternatives; do not turn them into simultaneous observations. A mentioned sun cue may support a time interpretation even when the participant calls it an imperfect metaphor or infers it rather than claiming to have seen it. Record that limitation with exact evidence. For a sunset-or-sunrise account, the reason for `interpretation:time` is the stated time change; record uncertain object names separately rather than adding them as simultaneous reason links.
- **Reactions:** Use `confusing` when the animation itself is difficult to follow, including difficulty noticing when it stops. Difficulty finding a meaning alone is not a `confusing` reaction. Use `glitch` for a visual effect judged to be a malfunction; an ordinary trial ending is not a glitch even when the participant wonders whether it was intentional. Leave `reaction` unassigned when the participant states no reaction; absence is not coded as neutrality.
