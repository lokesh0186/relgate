# Camera-Ready Scoring Changelog

## Accepted scorer behavior

The accepted version of `exact_quote_support()` normalized the quote and a JSON serialization of the benchmark case, then returned supported when any of these conditions held:

1. the full normalized quote occurred;
2. the quote's first 40 characters occurred; or
3. the quote's last 40 characters occurred.

Conditions 2 and 3 were inconsistent with the prompt's exact-evidence semantics. The JSON serialization also differed from the labeled, placeholder-filled bundle actually supplied by `src/run_experiment.py`.

## Camera-ready behavior

`src/score_results.py` now reconstructs the exact visible bundle fields and labels used by the experiment runner. A quote is supported only when its complete normalized text is a contiguous substring of that supplied bundle. Normalization is limited to lowercasing and collapsing whitespace. No prefix, suffix, fuzzy, token-overlap, paraphrase, or semantic-equivalence acceptance remains.

Five unit tests in `tests/test_score_results.py` cover contiguous matching, harmless normalization, prefix rejection, suffix rejection, and visible field labels.

PASS on a gate intentionally seeded as missing continues to count as one evidence claim and one unsupported claim, independent of quote extraction. This behavior is documented in the paper and metric report.

## Sensitivity result

The old and strict matchers disagreed on five of 169 extracted quotes. Full details are in `exact_evidence_sensitivity.csv` and `METRIC_REVALIDATION.md`.

Only the Unsupported Evidence Claims row changed:

| Mode | Accepted value | Strict camera-ready value | Change |
|---|---:|---:|---:|
| M0 | 0.062 | 0.035 | corrected |
| M1 | 0.208 | 0.208 | unchanged |
| M2 | 0.053 | 0.056 | corrected |

Critical Gap Recall, False-Ready Rate, False-Block Rate, Decision Accuracy, Actionability, and every underlying model response are unchanged. The central evidence-grounding comparison M2 < M1 is preserved. The paper, generated table, README, full scored/summary CSVs, and metric documentation now use the strict values.

The historical accepted-reproduction CSVs and this changelog are intentionally retained so the repository does not imply that the permissive implementation never existed.
