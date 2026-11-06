---
title: RQ3 Provisional Coding Report
description: Quick-reference Layer 1 and Layer 2 results from the current 72-trial provisional coding package.
type: rq3_provisional_report
status: provisional
tags: [analysis, rq3, coding]
---

# RQ3 Provisional Coding Report

The latest [validated package](full-corpus-validation.json) covers 72 immediate post-trial responses: NT (24), V1 (16), V2 (16), and V3 (16). These are provisional single-coder results.

## Layer 1 — meaning outcome

| Condition | Trials | Full success | Partial success | All success | Alternative meaning | Unknown meaning | False change |
|---|---:|---:|---:|---:|---:|---:|---:|
| NT | 24 | 18 | 0 | 18/24 (75%) | — | — | 6 |
| V1 | 16 | 7 | 3 | 10/16 (62.5%) | 6 | 0 | — |
| V2 | 16 | 13 | 1 | 14/16 (87.5%) | 1 | 1 | — |
| V3 | 16 | 0 | 0 | 0/16 (0%) | 10 | 6 | — |

For V1–V3, success requires a statement of the intended meaning; visual description alone does not count. NT success means a condition-consistent account of no meaningful animation or the continuous baseline colour shift. The NT false-change category records reported changes beyond that baseline.

## Layer 2 — response codes

Each cell is the number of distinct participant-trials assigned that code. Codes can co-occur, so columns do not sum to the condition totals. Object and transformation counts include all accuracy levels; see the [evidence file](full-corpus-code-evidence.csv) for full, partial, and incorrect assignments.

| Family | Code | NT (n=24) | V1 (n=16) | V2 (n=16) | V3 (n=16) |
|---|---|---:|---:|---:|---:|
| object | buildings | 0 | 0 | 15 | 0 |
| object | city | 0 | 0 | 4 | 0 |
| object | hills | 2 | 0 | 1 | 1 |
| object | landscape | 4 | 0 | 3 | 1 |
| object | moon | 0 | 11 | 0 | 0 |
| object | none | 18 | 0 | 0 | 1 |
| object | other | 2 | 0 | 0 | 0 |
| object | sphere | 0 | 2 | 1 | 13 |
| object | stars | 0 | 13 | 0 | 0 |
| object | sun | 0 | 14 | 1 | 4 |
| transformation | appearance | 1 | 12 | 10 | 6 |
| transformation | colour | 5 | 5 | 9 | 5 |
| transformation | disappearance | 0 | 3 | 0 | 2 |
| transformation | growth | 0 | 0 | 8 | 3 |
| transformation | movement | 2 | 14 | 2 | 5 |
| transformation | none | 15 | 0 | 0 | 2 |
| transformation | transition | 0 | 8 | 5 | 1 |
| transformation | zoom | 1 | 0 | 3 | 1 |
| stage | end | 2 | 12 | 4 | 6 |
| stage | process | 3 | 16 | 13 | 11 |
| stage | start | 2 | 10 | 6 | 2 |
| stage | unclear | 5 | 0 | 1 | 1 |
| interpretation | assistant | 1 | 1 | 0 | 0 |
| interpretation | entertainment | 1 | 1 | 0 | 0 |
| interpretation | fatigue | 0 | 2 | 0 | 0 |
| interpretation | location | 0 | 0 | 14 | 0 |
| interpretation | none | 21 | 0 | 1 | 5 |
| interpretation | notification | 0 | 0 | 0 | 1 |
| interpretation | other | 1 | 1 | 0 | 2 |
| interpretation | time | 0 | 10 | 1 | 4 |
| interpretation | warning | 1 | 0 | 2 | 4 |
| interpretation | weather | 0 | 2 | 0 | 1 |
| certainty | sure | 15 | 5 | 3 | 0 |
| certainty | unknown | 5 | 0 | 1 | 5 |
| certainty | unsure | 4 | 11 | 12 | 11 |
| reaction | confusing | 0 | 2 | 1 | 0 |
| reaction | distracting | 0 | 1 | 0 | 2 |
| reaction | glitch | 0 | 1 | 0 | 0 |
| reason | any explicit cue-to-meaning link | 3 | 14 | 15 | 11 |

A blank reaction in the trial codes means no explicit reaction was coded; it does not mean a neutral reaction.

## Source and interpretation boundary

The [coding rules](coding-rules.md), [trial codes](full-corpus-trial-codes.csv), [evidence file](full-corpus-code-evidence.csv), [report values](full-corpus-report-values.json), [source manifest](full-corpus-source-manifest.csv), and [build script](build_full_corpus.py) support these tables. Results describe immediate answers; they do not establish perception during driving or causal effectiveness.
