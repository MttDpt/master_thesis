---
name: da-code
description: Use for implementing and validating an approved RQ analysis as reproducible code
---
# Data Analysis

Implement one approved thesis RQ analysis as reproducible code and produce a validated provisional output package.

## Context

- Scope the run to one RQ and modality.
- Read the matching `RQ1`, `RQ2`, or `RQ3` contract.
- Read shared preprocessing rules only when this run depends on preprocessing, exclusions, classifications, joins, missingness, or derived inputs.
- Use thread-named files directly. Consult indexes/manifests only when required information is missing or needs verification.
- If an analytical choice is unresolved, route it to `da-preprocessing` or `da-rq-contract`; do not invent it.
- Before Python work, load `da-code-rules`.

## Execution

1. Check repository state and preserve unrelated changes.
2. Write deterministic analysis code directly; encode inputs, grain, population/denominators, operations, outputs, checks, privacy constraints, and stop conditions in code/config/run metadata rather than a prose plan.
3. Keep all code, outputs, figures, tables, logs, manifests, and receipts under the matching `analysis/RQn/` tree.
4. Delegate only mechanical execution/packaging when useful. The worker must not reinterpret or change analytical definitions, denominators, transformations, tests, or figure meaning.
5. Validate the generated package directly: reconcile inputs and denominators, inspect outputs, verify checks, privacy, and labels. Worker success alone is insufficient.
6. Record the run once in the matching RQ index/log and mark it `provisional` until explicit user approval.

## Boundaries

Never edit raw data, overwrite unrelated changes, publish to Overleaf, expose identifying information, or make substantive thesis claims without separate authorisation and validation.

Use `da-report` for narrative reporting.

## Handoff

Return code/output paths, execution status, checks, validation status, and unresolved blockers.
