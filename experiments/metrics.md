# Camera-Ready Metric Definitions

These definitions describe the deterministic implementation in `src/score_results.py` used for the final camera-ready results.

## Decision Metrics

- **Decision accuracy:** fraction of final `READY` / `FIX-BEFORE-SHIP` decisions equal to scenario ground truth. Denominator: 36 outputs per mode.
- **False-ready rate:** unsafe scenarios incorrectly decided `READY`. Denominator: 27 unsafe observations per mode (9 cases x 3 models).
- **False-block rate:** READY controls incorrectly decided `FIX-BEFORE-SHIP`. Denominator: 9 READY observations per mode (3 cases x 3 models).
- **Parse success:** fraction of outputs from which one of the two final decisions was extracted.

## Gap Metrics

A seeded gap is identified when deterministic keyword and local absence-marker rules in `gap_identified()` detect the missing or deficient gate concept. There is no half credit.

- **Gap recall:** response-level identified seeded gaps / seeded gaps, macro-averaged over unsafe outputs.
- **Critical gap recall:** response-level identified critical seeded gaps / critical seeded gaps, macro-averaged over unsafe outputs.

## Unsupported Evidence Claims

A response's evidence claims are:

1. quoted spans of at least eight characters, excluding quoted output labels; plus
2. each PASS parsed for a gate that ground truth marks as seeded-missing.

A quote is supported only when its complete normalized text is a contiguous substring of the exact visible change bundle. Normalization consists only of Unicode-independent case folding and whitespace collapsing. A quote may be shorter than its source sentence. Paraphrase, semantic equivalence, fuzzy matching, and prefix/suffix-only matching are unsupported.

A PASS on a seeded-missing gate contributes one evidence claim and one unsupported claim, even if the response also includes a quote. This preserves the accepted metric's treatment of an unsupported positive gate judgment.

Per-response unsupported rate is `unsupported claims / evidence claims`, or zero when no claims were extracted. The paper reports the macro mean across 36 responses per mode. Claim-pooled counts and Wilson intervals are also supplied in `results/camera_ready_wilson_intervals.csv`.

The criterion is deterministic; no human rating or inter-rater adjudication was used. It evaluates literal quotation validity, not semantic relevance or operational adequacy.

## Actionability

`actionability_score()` is an automated 0--2 lexical specificity heuristic over recommendation-like response chunks. It remains in the artifact for continuity with the accepted experiment but is omitted from the camera-ready paper table for space and focus. It is not a human rating.

## Output Schema

The scored CSV includes identifiers, ground truth, parsed decision, gap counts/recall, false-ready/false-block indicators, evidence-claim counts, `unsupported_evidence_rate`, the backward-compatible `evidence_hallucination_rate` alias, actionability, decision accuracy, usage, cost, and raw filename.

## Validity Limits

- The scenarios and M2 prompt share the seven-gate ontology.
- The quote test does not judge relevance or adequacy.
- Gap identification and actionability are deterministic lexical heuristics.
- Per-response macro means weight responses equally, including responses with no extracted evidence claims.
- The pilot has one temperature-0 observation per case/model/mode.
