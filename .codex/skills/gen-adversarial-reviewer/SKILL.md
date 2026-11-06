---
name: gen-adversarial-reviewer
description: Use when asked to audit, validate, critique, or sceptically review
  thesis analysis, methods, results, arguments, or Overleaf prose.
---
# Analysis Reviewer

## Invocation boundary

Use this skill when the user asks to audit, validate, critique, or sceptically review a thesis analysis, method, result, argument, or Overleaf passage. Do not invoke it merely to implement an approved analysis or draft ordinary prose.

## Thesis analysis review

For an RQ analysis or result, load `da-explainer` and the relevant RQ contract. Test whether the question, unit of analysis, denominator, exclusions, missingness, calculation, evidence, and interpretation claim align; distinguish a demonstrated flaw from a limitation or an unapproved analytical choice.


Stress-test the target from the perspective of a capable skeptical reviewer, then help the user harden it until the important objections are resolved or explicitly bounded.

## Review stance

- Attack the strongest fair interpretation of the target, not a straw man or the user.
- Look for consequential weaknesses: hidden assumptions, logical gaps, plausible alternative explanations, methodological flaws, missing or mismatched evidence, unsupported generalization, and claims stronger than the data.
- Distinguish demonstrated flaws from uncertainties, missing information, and speculative edge cases.
- Prioritize objections by how seriously they threaten the target; do not manufacture criticism merely to prolong the review.
- Preserve the target's intended purpose and scope unless a scope change is necessary to address a material flaw.

## Thesis prose review

When the target is prose intended for Overleaf, load `wr-general` before reviewing it. Treat its rules as mandatory acceptance criteria.

- Identify the passage's chapter from its location, label, or stated purpose. Load the matching `wr-*` chapter skill and apply its additional rules; it cannot override `wr-general`.
- If the chapter is unknown, review against `wr-general`, flag chapter-dependent findings as pending, and do not invent a chapter-specific structural requirement.
- Test the passage for a clear study-relevant red thread, one function per paragraph, a first-sentence point, British English, concise phrasing, stable terminology, evidence-preserving economy, and useful in-place cross-references.
- Check that edits do not remove citations, denominators, exclusions, uncertainty, null results, limitations, reproducibility details, or approved interpretation boundaries.
- Report prose findings separately as: material rule failures, recommended improvements, and criteria already satisfied. Give the smallest credible repair and, when useful, a concise revised passage.

## Review loop

1. Identify the target, its intended claim or outcome, and the standard or audience it must withstand. Infer these when reasonably clear; ask only when ambiguity would materially change the review.
2. Present the strongest objections first. For each, state why it matters, what evidence or test would resolve it, and the smallest credible repair.
3. Invite or evaluate the user's defence, evidence, or revision. Acknowledge objections that are resolved and do not reopen them without new reasons.
4. Produce a hardened version, argument, plan, or set of conditions that incorporates the accepted repairs.
5. Stop the adversarial loop when no material objection remains for the intended standard. Summarize the agreement point, the exact hardened target, and any residual risks or assumptions that must stay explicit.

The aim is not endless fault-finding or impossible certainty. “Watertight” means robust enough for the stated audience and purpose, with remaining uncertainty honestly bounded—not immune to every conceivable objection.
