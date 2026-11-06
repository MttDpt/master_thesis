---
name: da-code-rules
description: Use when writing Python code for a data-analysis run
---
# Python Rules

Use this skill whenever a thesis data-analysis run executes Python code or creates a figure with Python. It supplements the matching RQ contract; it does not define analysis rules, exclusions, denominators, or statistical choices.

## Python execution

- Use Python packages suited to the task: `pandas` and `numpy` for tabular and numerical work; `scipy` only for required numerical or statistical routines; `matplotlib` with `seaborn` for static analytical figures. Do not silently fall back to standard-library-only plotting or calculations when these packages are required; report an unavailable dependency instead.
- Keep inputs, transformations, calculations, and figure generation in reproducible Python code. Do not alter raw data or invent a data-processing rule to make a figure easier to draw.

## Figure conventions

- Always use Matplotlib's default `DejaVu Sans` as the main figure font unless the user explicitly requests a different font. If the font is not available, use another sans-serif font. Never, ever use a serif font for any figure.
- Do not place a title inside a figure. Put the figure's context in its caption, filename, and report text.
- Label both axes. Labels state the measured variable or category and include units where applicable.
- For every categorical comparison, use a legend with the displayed category names.
- Place the legend above the figure and keep it on a single line whenever the available width allows; use a compact multi-line arrangement only when a single line would harm readability or cause clipping.
- Encode distinct categories with both colour and marker or symbol; do not rely on colour alone. Use a sufficiently distinct, colourblind-safe palette and preserve the same mapping across every figure in the run.
- Start from this run-wide mapping unless the RQ contract establishes a different approved semantic mapping:

  | Category | Colour | Marker |
  | --- | --- | --- |
  | Onset | `#0072B2` | circle (`o`) |
  | Offset | `#D55E00` | square (`s`) |
  | Early | `#009E73` | triangle (`^`) |
  | Extra | `#CC79A7` | diamond (`D`) |

  RQ2 questionnaire figure variants `rq2-prov-I`, `rq2-prov-II`, and `rq2-prov-III` use Q1 bright blue `#4569FF` with a diamond (`D`) and Q2 bright rose `#FF3B78` with a downward triangle (`v`). In Figure 9, NT retains `#4D4D4D` with a cross (`X`); V1 `#1B9E77`, V2 `#7570B3`, and V3 `#D95F02` all use a circle (`o`). For legends that identify Q1/Q2 or NT/V1/V2/V3, show marker-only proxy handles in the mapped colour; never show connecting lines, axes, or uncertainty whiskers. Use subtle horizontal grid lines at the labelled y-axis values in RQ2 figures 3, 4, 6, 8, and 9. In `rq2-prov-III`, remove the report-level external image frame, place the legends for Figures 4, 6, and 9 closer to the plotting area while retaining clear separation, and position Figure 4's confidence-score label close beneath the x-axis labels without overlap.

  For the revised RQ1 displays, retain event colours and shapes while using filled markers for detected events and hollow markers for misses; place undefined gaze values in a separate labelled indeterminate position. The exact-count stacked displays use these fixed secondary mappings (counts appear inside segments, so no hatching is used):

  | Display | Category colours, in left-to-right order | Redundant encoding |
  | --- | --- | --- |
  | Trial detection profile | Both detected `#009E73`; onset only `#0072B2`; completion only `#D55E00`; neither `#777777` | Fixed segment order, labelled legend, exact counts |
  | Detection–timeliness | Detected <=3 s `#009E73`; >3–5 s `#56B4E9`; >5–10 s `#E69F00`; >10 s `#CC79A7`; miss `#777777` | Fixed interval order, labelled legend, exact counts |

  The revised RQ1 companion figures use ambient-display press state `#7B3294` with diamond (`D`), driver-axis state `#008837` with circle (`o`), and indeterminate state `#777777` with cross (`X`). NT trial-share and lane false-alarm observations use `#555555` with filled plus (`P`); median overlays use black ticks and lines; IQR ribbons use `#56B4E9` at 0.52 opacity with a `#0072B2` outline. Paired-share heatmaps use a continuous viridis scale, D/M text for detected/missed, and grey `#DDDDDD` with a dash for indeterminate values; spatial sample maps use a continuous magma scale and the existing AOI boundary. All figures use Matplotlib's DejaVu Sans font.

  When only onset and offset, or only early and extra, are shown, retain their assigned colour and marker. For other categories, assign additional distinct colour-marker pairs once and reuse them consistently throughout the run. Whenever a new category, colour, or marker is introduced, or an encoding rule changes, update this mapping table in the same skill revision so the documented mapping remains authoritative.
- Use hatch patterns, stripes, dots, crosses, diagonal lines, internal symbols, or other textures in coloured areas only when no text is displayed inside the area. If text is displayed inside a coloured area, remove all such patterns and use colour alone, with sufficient contrast for the text to remain readable.
- For figures intended for a PDF, prefer a horizontal composition when it improves readability or makes better use of the available page frame. Prefer rows, horizontally arranged small multiples, or a widened single panel over stacking compatible views vertically. Use a vertical layout when it clearly better preserves the data's natural ordering, comparison, or legibility.
- Export the publication figure in a vector format where appropriate and a PNG review copy. Visually inspect the exported figure for readable labels, a visible legend, distinguishable category encodings, and clipping before reporting it as validated.

## Boundary

These conventions govern Python implementation and figure presentation. The matching RQ contract remains authoritative for what the figure may show and how it may be interpreted.
