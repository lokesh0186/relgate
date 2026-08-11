# Camera-Ready Metric Sanity Report

Generated from the 108 frozen raw outputs using the corrected strict scorer.

## Integrity Checks

- Usable rows: 108
- Parse successes: 108
- Modes: 36 rows each
- Per mode: 27 unsafe observations and 9 READY controls
- Models: `openai/gpt-5.5`, `x-ai/grok-4.3`, `meta-llama/llama-4-maverick`
- Duplicate case/model/mode tuples: 0
- Missing or extra tuples: 0
- Other model identifiers: 0

## Decision Derivation

- M0: 27/36 correct = **0.750**; false-ready 0/27 = **0.000**; false-block 9/9 = **1.000**
- M1: 35/36 correct = **0.972**; false-ready 0/27 = **0.000**; false-block 1/9 = **0.111**
- M2: 36/36 correct = **1.000**; false-ready 0/27 = **0.000**; false-block 0/9 = **0.000**

All rates are observed sample statistics. For M2, the 95% Wilson interval is [0, 0.124555] for 0/27 false-ready observations and [0, 0.299145] for 0/9 false-block observations.

## Gap Recall

Unsafe outputs only, macro-averaged per response:

- M0: gap recall 0.968; critical gap recall **0.975**
- M1: gap recall 1.000; critical gap recall **1.000**
- M2: gap recall 1.000; critical gap recall **1.000**

## Unsupported Evidence Claims

The paper reports the mean of response-level unsupported/total-claim fractions, with zero assigned when no evidence claims are extracted. A claim is either an extracted quote or a PASS on a seeded-missing gate. The strict quote rule requires the entire quoted span to occur contiguously in the supplied bundle after case/whitespace normalization.

| Mode | All evidence claims | Quoted claims | Seeded-missing PASS claims | Old unsupported quote classifications | Strict unsupported quote classifications | Final macro rate |
|---|---:|---:|---:|---:|---:|---:|
| M0 | 8 | 8 | 0 | 4 | 3 | **0.035** |
| M1 | 22 | 10 | 12 | 2 | 2 | **0.208** |
| M2 | 159 | 151 | 8 | 5 | 5 | **0.056** |

Although M2 has the same total number of unsupported quote classifications under both policies, two classifications changed in each direction and their response-level locations changed the macro mean from 0.053 to 0.056. M0 changed from 0.062 to 0.035 because the exact visible `[not provided]` placeholder is part of the supplied bundle. Details for all quotes and all five changes are in `camera_ready/exact_evidence_sensitivity.csv`.

A PASS on a seeded-missing gate contributes one unsupported claim. This captures a positive gate assertion that contradicts the seeded absence even when the response's final decision remains FIX-BEFORE-SHIP.

The criterion is deterministic. No manual rating or inter-rater adjudication was used. Semantic relevance and actual operational adequacy are not measured.

## Final Paper Table

| Metric | M0 | M1 | M2 |
|---|---:|---:|---:|
| Critical Gap Recall | 0.975 | 1.000 | 1.000 |
| False-Ready Rate (n=27) | 0.000 | 0.000 | 0.000 |
| False-Block Rate (n=9) | 1.000 | 0.111 | 0.000 |
| Unsupported Evidence Claims | 0.035 | 0.208 | 0.056 |
| Decision Accuracy (n=36) | 0.750 | 0.972 | 1.000 |

Actionability remains in the CSVs (M0 1.580, M1 1.738, M2 1.739) but was omitted from the two-page paper for space and focus. It is an automated lexical heuristic, not a human rating.
