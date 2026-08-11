# Frozen Accepted Experiment

This file records the experiment represented by the 108 frozen raw outputs. Camera-ready reproduction must not make new API calls.

## Design

- 12 synthetic scenarios: 9 unsafe cases with at least one critical seeded gap and 3 fully specified READY controls.
- 3 review modes: M0 Freeform, M1 Checklist, and M2 Evidence-Grounded RelGate.
- 3 exact model identifiers: `openai/gpt-5.5`, `x-ai/grok-4.3`, and `meta-llama/llama-4-maverick`.
- One call per case/model/mode at temperature 0, top-p 1, maximum 1800 output tokens.
- 12 x 3 x 3 = 108 calls, each saved under `results/raw_outputs/`.

The cases are database migration, cache configuration, Kubernetes resource change, infrastructure change, routing change, OAuth configuration, observability/logging, background queue workers, feature-flag rollout, Kubernetes HPA scaling, staged feature-flag rollout, and CDN/DNS routing.

## Modes

- **M0:** unstructured production-readiness review.
- **M1:** the seven gates with per-gate PASS/FAIL and a final decision; no quote requirement.
- **M2:** the seven gates plus the frozen prompt's evidence-grounding rule and parseable output format.

## Gate Policy

G1 Observability, G2 Alerting, G3 Rollout Safety, and G4 Rollback are critical/blocking. G5 Ownership, G6 Reliability Impact, and G7 Validation are major; the M2 prompt allows READY only when all critical gates have evidence and no major gate has a severe unresolved concern.

The gate set is a pilot operationalization rather than a universal taxonomy.

## Reproduction Without Model Calls

```bash
python3 scripts/preflight.py
python3 -m unittest discover -s tests -v
python3 scripts/camera_ready_audit.py
python3 src/score_results.py --input-dir results/raw_outputs --output-prefix full
python3 src/make_tables.py
```

The camera-ready audit checks 108 usable rows, the complete Cartesian product, exact final model/mode sets, no duplicates, parse success, strict evidence sensitivity, model-level outcomes, and Wilson intervals.

## Frozen Inputs

Hashes for cases, prompts, raw outputs, accepted metric CSVs, and accepted manuscript/PDF files are recorded in `camera_ready/ACCEPTED_BASELINE_HASHES.txt`. Raw outputs, prompts, and benchmark cases are not modified by camera-ready scoring.
