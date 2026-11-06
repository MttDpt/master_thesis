---
name: thesis-conventions
description: Apply this thesis project's presentation conventions to results
  figures, tables, captions, condition and outcome labels, significance markers,
  and approved detection-score explanations.
---
# Thesis results presentation

Apply the author's project-specific rules when creating or editing thesis results figures, tables, captions, and outcome labels. Presentation edits do not authorize changing approved scores, tests, or numerical results.

For number formatting and statistical reporting, also apply [da-numbers-apa](../da-numbers-apa/SKILL.md); the rules below add thesis-specific conventions.

## Layout and statistical notation

- Keep thesis pages portrait; resize, crop, or redraw figures to fit while preserving readability.
- Use abbreviated statistic labels: M, SD, Md, IQR. Italicize Latin statistic labels in TeX with \textit{} or appropriate math typesetting; keep Greek symbols upright using the document's supported typesetting.
- Report IQR as a single value (Q3 minus Q1), not an interval. Do not relabel an interval as an IQR without the necessary source values.
- Write sample sizes as $n = 24$ or the appropriate value; retain the distinction between N and n when applicable. Keep numerical values and percentages out of \textit{}.
- Replace “Mean-score gap” with δ and “Holm-adjusted p” with pHolm, using appropriate mathematical typesetting: upright δ, italic p, and an upright Holm label. Center headings within their columns.

## p-values and significance markers

- Use decimal notation in tables rather than scientific notation, retaining enough precision to avoid misleading rounding; apply the exact-p-value rules in the APA skill.
- Replace NS labels with exact p-values whenever available, including nonsignificant results. If only a threshold such as p > .05 is available from the approved source, preserve its limited precision rather than inventing a value. Report an exact boundary value accurately.
- Place significance asterisks alongside figure p-values, for example p = .015*. Use the highest applicable level: * for p < .05, ** for p < .01, *** for p < .001.
- Determine stars from the unrounded p-value. Where a comparison uses Holm correction, use its adjusted p-value for both the label and stars.
- Define the star thresholds and any correction in a concise caption or legend. Stars highlight statistical significance, not effect size or practical importance.

## Condition and outcome labels

- Replace V1, V2, V3, and NT with sun-to-moon, buildings, red-sphere, and no-animation; add “animation” to animated condition names when useful.
- Call compound detection “detection (onset + completion)”.
- Call detection in non-animated trials “detection (no press)”; “detection (no trigger press)” is also acceptable.
- Use “recognition” and “interpretation” consistently, including non-animated trials. Avoid expanded labels such as “unchanged-condition recognition” and “correct meaning interpretation”.

## Figure styling and readability

- Use distinct colours for conditions, especially sun-to-moon and buildings.
- Use pale, low-opacity fills with coloured outlines for bars and markers.
- Keep markers small enough to reveal interval endpoints and surrounding elements; draw markers above interval lines.
- Separate numerical labels from bars, markers, and connecting lines so they do not overlap.
- When a cross-shaped no-animation marker overlaps an interval line, rotate the marker so the interval line passes between its arms.

## Captions and detection-score explanations

- Keep captions concise; remove redundant commentary while retaining essential score definitions and trial-set information.
- When showing the approved combined detection score, explain that animated-trial detection averages onset and completion, giving scores of 0, 0.5, or 1.
- Explain that detection success in non-animated trials means no trigger press.
- Combining separate onset/completion measures is a task-specific analytical change, not a default formatting operation; use an existing approved combined score or follow explicit authorization.

These rules do not prescribe visual selection, table borders, table structure, or chart composition.
