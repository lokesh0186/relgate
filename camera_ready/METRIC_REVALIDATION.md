# Metric Revalidation

## Frozen-evidence integrity

All camera-ready computations used the frozen 108 JSON responses in `results/raw_outputs/`. No model or API calls were made. The accepted baseline hashes are in `ACCEPTED_BASELINE_HASHES.txt`.

The preflight and tuple audit established:

- 108 raw files, 108 usable scored rows, and 108 parse successes;
- 36 observations per mode;
- 27 unsafe observations and 9 READY-control observations per mode;
- exactly 12 scenarios, each represented for every model and mode;
- exactly three models: `openai/gpt-5.5`, `x-ai/grok-4.3`, and `meta-llama/llama-4-maverick`;
- exactly three modes: `m0_freeform`, `m1_checklist`, and `m2_evidence_grounded`;
- zero duplicate, missing, or extra case/model/mode tuples; and
- no Claude, Sonnet, or Anthropic result rows.

## Accepted-number reproduction

Before changing the scorer, `src/score_results.py` reproduced the accepted table exactly from the frozen outputs:

| Metric | M0 | M1 | M2 |
|---|---:|---:|---:|
| Critical Gap Recall | 0.975 | 1.000 | 1.000 |
| False-Ready Rate | 0.000 | 0.000 | 0.000 |
| False-Block Rate | 1.000 | 0.111 | 0.000 |
| Unsupported Evidence Claims | 0.062 | 0.208 | 0.053 |
| Decision Accuracy | 0.750 | 0.972 | 1.000 |
| Actionability | 1.580 | 1.738 | 1.739 |

The reproduction snapshots are `results/accepted_repro_relgate_scored_results.csv` and `results/accepted_repro_summary_metrics.csv`.

## Exact-evidence sensitivity audit

The accepted matcher treated a quote as supported if the full normalized quote, its first 40 characters, or its last 40 characters occurred in a normalized serialization of the case JSON. The strict policy instead checks whether the complete normalized quoted span occurs contiguously in the exact labeled change-bundle text shown to the model. Normalization lowercases text and collapses whitespace only.

| Mode | Quoted claims | Old unsupported quotes | Strict unsupported quotes | Seeded-missing PASS claims | Total evidence claims under strict scoring |
|---|---:|---:|---:|---:|---:|
| M0 | 8 | 4 | 3 | 0 | 8 |
| M1 | 10 | 2 | 2 | 12 | 22 |
| M2 | 151 | 5 | 5 | 8 | 159 |

Five quote classifications changed. Every row, quote, and source-context excerpt is preserved in `exact_evidence_sensitivity.csv`:

1. M0 / Grok / case_001: `[not provided]` changed from unsupported to supported because that exact placeholder is visible in the supplied bundle.
2. M2 / Llama / case_004: `Rollback Plan: can downgrade` changed from unsupported to supported because the visible field label and value form a contiguous supplied span.
3. M2 / Llama / case_005: `nginx.ingress.kubernetes.io/canary-weight: '10'` changed from supported to unsupported because the source uses double quotes; case/whitespace normalization does not alter quotation marks.
4. M2 / Llama / case_008: `Deployment Plan: Update config and restart workers.` changed from unsupported to supported because the visible label and value are contiguous in the supplied bundle.
5. M2 / Llama / case_009: a flattened multi-line configuration quote changed from supported to unsupported because the full normalized model quote is not a contiguous span of the supplied diff.

The M2 unsupported-quote count remained five, but the changed classifications occur in different response rows. Because the published metric is the macro mean of 36 response-level unsupported/claim fractions, its rounded value changed.

`unsupported_gate_passes()` contributes one total evidence claim and one unsupported claim whenever the response marks a benchmark-seeded missing gate as PASS. It contributed 0, 12, and 8 unsupported claims for M0, M1, and M2 respectively. This is separate from literal quote matching and prevents an unsupported positive gate decision from escaping the metric merely because no quote was extracted.

## Final strict table

| Metric | M0 | M1 | M2 |
|---|---:|---:|---:|
| Critical Gap Recall | 0.975 | 1.000 | 1.000 |
| False-Ready Rate (`n=27` unsafe/mode) | 0.000 | 0.000 | 0.000 |
| False-Block Rate (`n=9` READY/mode) | 1.000 | 0.111 | 0.000 |
| Unsupported Evidence Claims | 0.035 | 0.208 | 0.056 |
| Decision Accuracy (`n=36`/mode) | 0.750 | 0.972 | 1.000 |

Actionability remains 1.580, 1.738, and 1.739 in the artifact. It was omitted from the paper table for two-page space and reviewer-priority reasons, not recomputed away.

The unsupported-evidence headline is a macro average: for each response, unsupported claims are divided by all evidence claims, with zero assigned when no claim exists; the 36 response fractions are then averaged. Claim-pooled estimates are separately labeled in the Wilson CSV and must not be substituted for the headline statistic.

## Uncertainty and model-level outputs

`results/camera_ready_model_level_metrics.csv` reports each model/mode combination. `results/camera_ready_wilson_intervals.csv` reports 95% Wilson intervals for decision accuracy, false-ready rate, false-block rate, pooled claim validity, and pooled critical-gap recall.

For the principal zero-observed-error results:

- M2 false-ready: 0/27, 95% Wilson interval [0.000000, 0.124555];
- M2 false-block: 0/9, 95% Wilson interval [0.000000, 0.299145]; and
- M2 decision accuracy: 36/36, 95% Wilson interval [0.903581, 1.000000].

These are intervals for observed binomial proportions under the reported sampling abstraction. They do not turn the synthetic cases into a population sample and do not imply zero production risk.

## Reproduction commands

`./reproduce.sh` runs preflight, strict-matcher unit tests, the frozen-output sensitivity/coverage audit, final strict scoring, and table generation. It makes no model or API calls.
