# Metric Sanity Report

Generated: 2026-06-22
Source: `results/full_relgate_scored_results.csv` (108 rows, Claude outputs excluded)

## Counts

| Mode | Total | Unsafe (n) | READY Controls (n) |
|------|-------|-----------|-------------------|
| M0 Freeform | 36 | 27 | 9 |
| M1 Checklist | 36 | 27 | 9 |
| M2 Evidence-Grounded | 36 | 27 | 9 |
| **Total** | **108** | **81** | **27** |

Models: `openai/gpt-5.5`, `x-ai/grok-4.3`, `meta-llama/llama-4-maverick`

## Decision Accuracy Derivation

- **M0**: 27 correct (all unsafe correctly blocked) + 0 correct (all 9 READY controls false-blocked) = 27/36 = **0.750**
- **M1**: 27 correct (all unsafe) + 8 correct (8/9 READY controls approved) = 35/36 = **0.972**
- **M2**: 27 correct (all unsafe) + 9 correct (all READY controls approved) = 36/36 = **1.000**

## False-Ready Rate (denominator = 27 unsafe cases per mode)

- M0: 0/27 = 0.000
- M1: 0/27 = 0.000
- M2: 0/27 = 0.000

## False-Block Rate (denominator = 9 READY controls per mode)

- M0: 9/9 = 1.000 (all models blocked all 3 READY controls)
- M1: 1/9 = 0.111 (GPT-5.5 blocked case_012)
- M2: 0/9 = 0.000

## Gap Recall and Critical Gap Recall (unsafe cases only)

- M0: Gap Recall = 0.968, Critical Gap Recall = 0.975
- M1: Gap Recall = 1.000, Critical Gap Recall = 1.000
- M2: Gap Recall = 1.000, Critical Gap Recall = 1.000

## Unsupported Evidence Claims Rate

Definition: fraction of quoted evidence claims in the response that do not exactly appear in the scenario bundle text.

- M0: 0.062
- M1: 0.208
- M2: 0.053

## Actionability (0-2 scale)

- M0: 1.580
- M1: 1.738
- M2: 1.739

## Final Table Values

| Metric | M0 | M1 | M2 |
|--------|------|------|------|
| Critical Gap Recall | 0.975 | 1.000 | 1.000 |
| False-Ready Rate (n=27) | 0.000 | 0.000 | 0.000 |
| False-Block Rate (n=9) | 1.000 | 0.111 | 0.000 |
| Unsupported Evidence Claims | 0.062 | 0.208 | 0.053 |
| Decision Accuracy (n=36) | 0.750 | 0.972 | 1.000 |
| Actionability (0-2) | 1.580 | 1.738 | 1.739 |

## Qualitative Observations

- M0 false-block on case_010: All 3 models (GPT-5.5, Grok 4.3, Llama 4 Maverick) returned FIX-BEFORE-SHIP despite complete readiness evidence.
- M1 false-block on case_012: GPT-5.5 returned FIX-BEFORE-SHIP on the CDN/DNS READY control.
- M1 hallucination: Grok 4.3 on case_008 quoted "set back to 5 if issues arise" but actual text was "Set concurrency back to 5 if issues arise." -- paraphrased rather than exact citation.
- M2 cited exact text from bundles and correctly marked missing evidence as MISSING_EVIDENCE across all 108 evaluated decisions (36 per mode).

## Notes

- Previous version reported M0 accuracy as 0.757 due to inclusion of a stale Claude-Sonnet-4 output. After exclusion: 0.750.
- Parse success rate: 1.000 across all modes (all responses parseable).
- No Anthropic/Claude data in final results.
