# Metrics Definition

## Primary Metrics

### 1. Gap Recall
Of the seeded readiness gaps, what fraction did the model identify?

Formula: identified_seeded_gaps / total_seeded_gaps

Scoring: A gap is 'identified' if the model explicitly mentions the absence or deficiency corresponding to that gap. Partial matches (mentioning the topic but not the gap) count as 0.5.

### 2. Critical Gap Recall  
Of critical seeded gaps (severity=critical), what fraction did the model identify?

Formula: identified_critical_gaps / total_critical_gaps

This is the most important recall metric. Missing a critical gap means the system could approve a dangerous change.

### 3. False-Ready Rate
How often did the model say READY when at least one critical gate lacked evidence?

Formula: false_READY_decisions / cases_with_critical_missing_evidence

Since all 12 cases have at least one critical gap, the denominator is 12 per model-mode combination.

Ideal: 0.0 (never says READY when critical evidence is missing)

### 4. Evidence Hallucination Rate
How often did the model claim evidence exists (cite something) when that evidence is NOT in the bundle?

Formula: unsupported_evidence_claims / total_evidence_claims

Scoring: An 'evidence claim' is any statement that cites or references specific text from the bundle as proof. 'Unsupported' means the cited text does not exist in the bundle or is materially different.

For M0 (freeform), count any confidence statement about readiness as an implicit evidence claim if it asserts something is covered.

### 5. Actionability Score
Score each recommendation/finding on 0/1/2:
- 0 = vague or not useful ('consider monitoring')
- 1 = partially actionable ('add rollback plan')
- 2 = specific fix-before-ship action tied to missing evidence ('Add rollback trigger: if error_rate > 2% for 3min, revert via kubectl rollback')

Per-case actionability = mean of recommendation scores
Overall actionability = mean across all cases

### 6. Decision Accuracy
Whether the final READY/FIX-BEFORE-SHIP matches ground truth.

Formula: correct_decisions / total_decisions

Ground truth: all 12 cases should be FIX-BEFORE-SHIP (by design, all have critical gaps).

## Secondary Metrics

- **Verbosity**: total tokens in response
- **Latency**: seconds from request to response completion
- **Cost**: USD per call (from OpenRouter usage data)
- **Gate Consistency**: for M1/M2, whether individual gate verdicts are internally consistent with the final decision
- **Unsupported Assumptions**: count of claims not grounded in bundle text (broader than hallucination)

## Scoring Procedure

1. **Automated scoring** (score_results.py):
   - Parse M1/M2 structured outputs for gate verdicts
   - Check decision accuracy against ground truth
   - Count evidence claims and verify against bundle text
   - Compute token counts and latency from API response

2. **Semi-automated scoring** (requires human review):
   - Actionability scores (apply rubric)
   - M0 freeform gap identification (map free text to seeded gaps)
   - Evidence hallucination verification for edge cases

3. **All scoring decisions saved in CSV** with justification notes

## Output CSV Schema

Columns:
```
case_id, case_type, model, mode, seeded_gap_count, critical_gap_count, identified_gap_count, identified_critical_gap_count, gap_recall, critical_gap_recall, false_ready, evidence_claim_count, unsupported_evidence_claim_count, evidence_hallucination_rate, actionability_score_mean, decision_accuracy, latency_seconds, tokens_in, tokens_out, cost_usd, notes
```

## Aggregation

Results table in paper aggregates by mode (across all models and cases):

| Mode | Gap Recall | Crit. Gap Recall | False-Ready | Evid. Halluc. | Action. | Decision Acc. |
|------|-----------|-----------------|-------------|--------------|---------|---------------|
| M0   |           |                 |             |              |         |               |
| M1   |           |                 |             |              |         |               |
| M2   |           |                 |             |              |         |               |

Secondary breakdown by model shown if space permits or discussed in text.

## Threats to Metric Validity

- Gap identification from freeform text requires interpretation (mitigated by rubric)
- Seeded gaps have binary ground truth but real readiness is nuanced
- Hallucination detection requires careful bundle-text matching
- Actionability scoring involves subjective judgment (mitigated by 0/1/2 rubric)
- All 12 cases designed to be FIX-BEFORE-SHIP limits evaluation of true-positive READY decisions
