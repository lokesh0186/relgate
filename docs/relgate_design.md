# RelGate: Framework Design

**RelGate** is a lightweight LLM-assisted production-readiness gate for cloud changes. It evaluates a structured **change bundle** against a set of **gates**, using evidence-grounded reasoning to produce a deployment decision.

---

## Change Bundle Schema

A change bundle is a JSON document representing a cloud/software change submitted for production-readiness review.

| Field | Description |
|-------|-------------|
| `change_id` | Unique identifier |
| `change_type` | Category (e.g., `database_migration`, `k8s_deployment`, `terraform_infra`, `cache_config`) |
| `change_summary` | 1–3 sentence description of what the change does |
| `diff_or_config` | The actual diff, config snippet, or manifest change |
| `service_context` | What service/system this affects, dependencies, traffic |
| `deployment_plan` | How it will be deployed (canary, blue-green, all-at-once, feature flag) |
| `rollback_plan` | How to revert if something goes wrong |
| `observability_evidence` | Dashboards, metrics, logs, traces available to detect impact |
| `alerting_evidence` | Alert rules covering this change's failure modes |
| `owner_oncall_evidence` | Who owns the change, on-call contact, escalation path |
| `slo_reliability_impact` | SLO/error-budget impact, customer-facing risk |
| `blast_radius` | Scope of impact (one pod, one service, one region, all regions) |
| `validation_evidence` | Tests, dry-runs, staging results, integration tests run |

---

## Gates

### G1: Observability Evidence

**Question:** Does the bundle include concrete dashboard/metric/log/trace evidence needed to detect the impact of this change?

- **PASS criteria:** Specific dashboard URL, metric name, log query, or trace identifier cited from the bundle.
- **FAIL criteria:** No observability evidence provided, or only vague claims like "we have monitoring."

### G2: Alerting Evidence

**Question:** Does the bundle include alert coverage for this change's failure modes, or explain why existing alerts are sufficient?

- **PASS criteria:** Alert rule name, threshold, or explicit statement that existing alerts cover the new failure modes with rationale.
- **FAIL criteria:** No alerting evidence, or generic "our alerts will catch issues."

### G3: Rollout Safety

**Question:** Does the bundle include staged rollout, canary, feature flag, or blast-radius control?

- **PASS criteria:** Specific deployment strategy with stages, percentages, or feature flag configuration cited.
- **FAIL criteria:** All-at-once deployment with no staged approach, or no deployment strategy mentioned.

### G4: Rollback Evidence

**Question:** Does the bundle include a specific rollback plan and trigger condition?

- **PASS criteria:** Concrete rollback steps with trigger condition (e.g., "if error rate > 1% for 5min, revert to previous version via …").
- **FAIL criteria:** No rollback plan, or vague "we can revert if needed."

### G5: Ownership

**Question:** Does the bundle identify owner, on-call, and escalation path?

- **PASS criteria:** Named owner, on-call rotation or contact, escalation procedure.
- **FAIL criteria:** No ownership info, or "the team will handle it."

### G6: Reliability Objective / Customer Impact

**Question:** Does the bundle state SLO/error-budget/customer-impact risk?

- **PASS criteria:** References specific SLO, error budget consumption estimate, or customer-facing impact assessment.
- **FAIL criteria:** No SLO/reliability mention, or "low risk" without justification.

### G7: Validation Evidence

**Question:** Does the bundle include test, dry-run, staging, or verification results?

- **PASS criteria:** Test results, staging deployment outcome, dry-run output, or integration test pass cited.
- **FAIL criteria:** No validation evidence, or "tests pass" without specifics.

---

## Gate Criticality

| Tier | Gates | Behavior |
|------|-------|----------|
| **Critical** (must pass for READY) | G1, G2, G3, G4 | Any failure → FIX-BEFORE-SHIP |
| **Major** (should pass) | G5, G6, G7 | Missing → FIX-BEFORE-SHIP |

> **Note:** Organizations may configure criticality differently. This is the default for our pilot.

---

## Decision Logic

```
if all critical gates PASS and all major gates PASS:
  decision = READY
elif any critical gate has MISSING_EVIDENCE:
  decision = FIX-BEFORE-SHIP
elif any gate is AMBIGUOUS:
  decision = UNKNOWN (requires human review)
else:
  decision = FIX-BEFORE-SHIP
```

---

## Evidence-Grounding Rule

Every PASS claim must cite the exact text/span from the change bundle that supports it.

**PASS format:**

```
Gate: G1 Observability Evidence
Verdict: PASS
Evidence: "Dashboard: grafana.internal/d/svc-orders-latency, Alert: orders_p99_latency > 500ms" (from field: observability_evidence)
```

**MISSING_EVIDENCE format:**

```
Gate: G1 Observability Evidence
Verdict: MISSING_EVIDENCE
Evidence: No observability evidence found in the bundle.
Recommendation: Add dashboard/metric references before deployment.
```

**Core constraint:** The model must NOT infer, assume, or fabricate evidence.

---

## Review Modes

### M0: Freeform

- Prompt asks: "Review this change for production readiness."
- No explicit gate list. No evidence-citation requirement.
- LLM responds in natural language.

### M1: Checklist

- Prompt gives the 7-gate checklist and asks for pass/fail per gate.
- LLM should assess each gate but is not required to cite exact evidence spans.
- Final decision required.

### M2: Evidence-Grounded RelGate

- Prompt gives gates AND requires every PASS to cite exact evidence from the bundle.
- If evidence is absent, model must mark MISSING_EVIDENCE.
- Final decision cannot be READY if any critical gate is MISSING_EVIDENCE.
- This is the full RelGate protocol.

---

## Architecture

```
Change Bundle (JSON)
       |
       v
[Review Mode Selection: M0 / M1 / M2]
       |
       v
[LLM Review (via OpenRouter API)]
       |
       v
[Gate Scoring: G1-G7 verdicts]
       |
       v
[Evidence Verification: check cited evidence exists in bundle]
       |
       v
[Decision: READY / FIX-BEFORE-SHIP / UNKNOWN]
       |
       v
[Scoring Script: compare to ground truth]
```
