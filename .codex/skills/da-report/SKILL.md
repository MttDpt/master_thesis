---
name: da-report
description: Use to assemble or revise a standalone report from a validated
  analysis package, including a rendered HTML report when requested.
---
# Analysis Report

Use to create or revise a standalone report from a validated analysis package. For thesis prose, use `wr-general` and the matching chapter skill directly with the approved evidence.

- Follow the current reporting brief. Read the package manifest or receipt, relevant tables, and displayed figures; consult only necessary contract clauses.
- Do not read raw datasets or full analysis history unless a requested value cannot otherwise be verified.
- Report the exact conflict if validation is incomplete or artifacts disagree; `da-code` owns changes to analytical logic.
- Assemble the requested report under the run's `report/` directory unless another destination is specified.
- Lead with the questions the report is meant to answer and direct, plain-language results. Follow any question order, terminology, and status labels in the brief; label findings from the evidence rather than assuming a desired conclusion.
- Make the population, unit, denominator, comparison, and uncertainty clear where they affect interpretation. Explain what pairing, multiplicity correction, or other design choices contribute, and state relevant limits such as order effects or different participant subsets when they apply.
- Distinguish observed counts, calculated estimates, statistical evidence, and interpretation. Describe likely descriptive leaders separately from tested conclusions; nonsignificance does not show equivalence. Keep claims within the study design and requested analytical scope.
- For HTML reports, use a readable responsive layout and informative tables or figures. Use captions or compact reading notes to identify axes, units, encodings, denominators, uncertainty, and meaningful boundaries. Keep technical detail secondary (for example, in an expandable section) when the brief asks for a plain-language report.
- Link the exact source tables, figures, settings, code, provenance, and validation artifacts that support reported values when available. State computational validation, statistical conclusion, and approval for thesis adoption as distinct statuses when relevant.
- Add a worked example only when useful or requested; use `da-explainer` for substantive explanation. Verify report values against generated artifacts and inspect the rendered output with appropriate local browser or document tooling; fix numerical, link, readability, or clipping issues found.
- Update an existing RQ index/log once when a report is added or its recorded status changes. Preserve provisional status until explicit approval.

Return the report and source-package paths, validation result, and any material unresolved issue.
