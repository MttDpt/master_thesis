# Study-results wording

Use when drafting, revising, or discussing the thesis's empirical findings in any chapter, including Results and Discussion. These are the author's wording preferences from RQ1 draft annotations and follow-up clarification; they do not select analyses or approve new results.

## Evidence remains authoritative

Read the requested passage and its approved result source. Resolve a concrete definition or interval gap through the relevant analysis contract; for RQ1, use the [RQ1 contract](../../../../analysis/contract_RQ1.md) and [pre-processing rules](../../../../analysis/rules_preprocessing.md). Do not recalculate data just to improve prose. Examples below illustrate wording, not a new source of study values.

Copy verified event windows, denominators, units, and aggregation levels from those sources. Do not turn a mistaken time label in an annotation into a scientific definition. For a wording-only edit containing a factual conflict, identify the smallest conflict briefly and preserve the source-supported fact; change no unrelated prose. If the user explicitly wants a verbatim transcription, provide it as their proposed wording without presenting conflicting labels or values as validated results.

## Participant actions and windows

- Prefer "Participants detected changes in the sun-to-moon animation during the onset window" to "Sun-to-moon onset was detected". Use active language about participants reporting or responding to a change.
- Place the verified interval before its event label: "[verified interval] onset window" or "[verified interval] completion window". Include the interval when naming an event window, rather than using "detected onsets", "completion-period samples", or vague "later" wording.
- Describe scheduled changes and matched reports; avoid wording implying that participants understood a change's meaning.
- For outcome comparisons, write "In trials where participants missed the change..." rather than treating trial outcomes as separate participant populations.
- Use "reaction time" for the delay from the scheduled change to the matched trigger press. "Participants responded faster" is appropriate when supported. Never say "responded sooner after detecting it": the detection time is not a separate measured starting point.

## Label values and counts

- Prefer "Mdn=" for medians. Name the measure and include its unit; an isolated "Mdn=18.7" is unreadable. For example, "time looking at the display: Mdn=18.7 s" identifies the quantity.
- Add "(n=)" when the relevant sample count is otherwise missing. State whether it counts trials, evaluable gaze windows, detected events, or presses. A nearby unambiguous numerator/denominator need not be repeated. Follow an explicit request to remove a redundant count from a sentence.
- A gaze sample count does not replace the eligible detection denominator. A lane-position press count does not count unique trials or participants.
- When combining measures, label them separately: "time looking at the display: Mdn=... s; contact frequency: Mdn=... contacts per valid minute". Do not leave a seconds value and a frequency value in one unexplained parenthesis.
- Distinguish affected trials from the overall press count: "Additional presses occurred in ... trials, with ... presses overall". "Overall" should identify the stated condition or group, not imply a study-wide total.
- Preserve the summary operation. A median of trial averages must remain distinguishable from a median across samples, a mean across trials, or a value at a press. Use "median of the trial averages" rather than the ambiguous "median average distance".

## Plain wording for gaze

Use concrete verbs and familiar nouns instead of "ambient gaze allocation" or "display-looking time".

| Reported measure | Plain wording | Keep clear |
| --- | --- | --- |
| Total ambient time, seconds | "time participants spent looking at the display" | This is seconds, not a percentage. |
| Ambient share, percent | "the proportion of valid looking time spent on the display" | Its denominator includes valid display and driver-axis gaze, not every recorded gaze sample. Explain this once where needed. |
| Contact frequency | "how often the gaze record showed looking at the display" | Label values as recorded contacts per valid minute; define the valid-time denominator at first use. Contacts can be split by tracking gaps and are not confirmed intentional glances. |

"Participants looked at the display more and for longer" needs separately labelled share and seconds values so "more" is not mistaken for contact frequency. When the contrast is frequency, "participants looked at the display less often" can follow the recorded-contact explanation, with the frequency label attached to its value.

Support "similar amounts of time looking" with total ambient seconds. Similar share percentages alone do not establish similar seconds. Do not silently replace a contact run with a verified look or fixation. Explain the measurement once; avoid repeating a long technical definition in every sentence.

## Plain wording for lane position and presses

- Replace "lower median lane-midpoint deviation" with "cars were typically closer to the lane centre", retaining the distance in metres and the statistic.
- For a press measurement, specify "when participants pressed the trigger". A value at a press does not describe lane position across the whole trial.
- For a trial summary, name the actual whole-trial measure and aggregation. Do not invent a no-press comparison from press-only results or silently substitute a whole-trial statistic.
- Define extra presses at first use: "additional trigger presses that could not be matched to a scheduled change". They are not necessarily "presses before the official ones".
- Define early presses as presses before the scheduled onset began, and no-animation false alarms as presses despite no scheduled visual change. Keep these categories distinct.
- Say which verified window contains additional presses and separate the number of affected trials from the total number of presses.

## Comparisons and cross-insights

- Lead with the comparison, then the supporting values: most versus fewest detections, shorter versus longer reaction time, or higher versus lower gaze values. Do not merely list each condition's row.
- Cross-reference outcomes honestly. A condition with the fewest onset reports can have the most completion reports; avoid declaring a complete reversal or ranking if one condition is tied or the inference is inconclusive.
- Make the logical connection visible: "Although participants spent similar amounts of time looking at the display, reaction times differed across animations." Report the verified medians and sample counts supporting each part.
- Connect detection, reaction time, gaze, and lane position when relevant to the requested question, without treating coincident condition summaries as an individual-level association or causal explanation.
- Keep Results observations separate from Discussion explanations. In Discussion, the same participant-focused and measurement wording applies; qualify a proposed mechanism as an interpretation.
- Avoid repeatedly inserting "descriptively" into findings. Establish descriptive or exploratory status at the appropriate section or analysis introduction; place essential limitations once where they constrain interpretation. Preserve consequential uncertainty, missingness, and null results without a disclaimer after every sentence.
- Use "although", "while", "despite", or "therefore" only when the connection is clear. A lower gaze frequency and higher detection count can be contrasted; they do not explain each other.

## Targeted revisions and direct questions

- Replace only the highlighted text when that is the request. Keep surrounding wording, data, structure, and ordering. Do not add a broader polish, restore an explicitly deleted sentence elsewhere, or repeat a finding merely to introduce the next one.
- Apply the user's replacement wording rather than generating a fresh alternative. Change grammar only as necessary to join it to the surrounding sentence; flag a substantive factual conflict separately.
- Return the requested revised sentence or paragraph, without unsolicited outlines or review checklists. Include annotation directives and change formatting when the current request requires them.
- If asked "which value is this?", answer with the measure's name and unit immediately. If asked for its dataset label, give the exact verified column name. Do not answer either question solely by rewriting the sentence.
