# Experiment Plan

## Overview
- 12 cloud-change cases × 3 review modes × 3 models = 108 API calls
- All calls via OpenRouter API
- Temperature = 0 for determinism
- All raw outputs saved

## Case Design

12 cases across these types:
1. case_001: Database migration / schema change (PostgreSQL column addition with no downtime strategy)
2. case_002: Cache TTL change (Redis TTL reduction from 1hr to 5min for user sessions)
3. case_003: Kubernetes deployment resource-limit change (memory limit increase for order-service)
4. case_004: Terraform infrastructure change (RDS instance class upgrade in production)
5. case_005: Load balancer / routing change (ingress rule update shifting traffic to new API version)
6. case_006: Authentication config change (OAuth token expiry reduction from 24h to 1h)
7. case_007: Observability/logging change (adding structured logging with sampling rate change)
8. case_008: Background worker / queue change (increasing SQS consumer concurrency from 5 to 20)
9. case_009: Feature flag rollout (enabling new payment flow for 100% of users)
10. case_010: Dependency/library upgrade (upgrading gRPC client library major version)
11. case_011: Alert threshold change (relaxing CPU alert from 80% to 95%)
12. case_012: Regional/failover config change (adding new region to service mesh with failover)

Each case has:
- Realistic change description
- Pseudo diff or config snippet
- Service context
- Seeded missing evidence labels (ground truth)
- Expected gaps and their severity (critical/major/minor)
- Expected correct decision (READY or FIX-BEFORE-SHIP)

## Seeded Gaps

Distribute gaps so that:
- Every case has 2-5 seeded gaps
- At least 1 critical gap per case (ensuring FIX-BEFORE-SHIP is correct answer for all 12)
- Gap types cover: missing rollback plan, vague rollback, no alert, no dashboard/metric, missing owner/on-call, no SLO/customer impact, unsafe all-at-once deploy, no blast-radius limit, missing validation/staging test, ambiguous dependency risk, missing data migration recovery, weak post-deploy monitoring
- Total seeded gaps across 12 cases: ~36-40
- Critical gaps: ~18-20

## Review Modes

M0 Freeform:
- System prompt: 'You are a senior SRE reviewing a cloud change for production readiness.'
- User prompt: 'Review this change for production readiness. Identify any concerns.' + change bundle text
- No explicit gates, no evidence requirement

M1 Checklist:
- System prompt: 'You are a senior SRE. Evaluate this change against the following production-readiness checklist.'
- User prompt: Includes the 7-gate checklist (G1-G7) + change bundle + 'For each gate, state PASS or FAIL with a brief explanation. Then give final decision: READY or FIX-BEFORE-SHIP.'
- No strict evidence-citation requirement

M2 Evidence-Grounded RelGate:
- System prompt: 'You are a production-readiness gate. You must evaluate each gate and cite exact evidence from the change bundle. If evidence is not present, you MUST say MISSING_EVIDENCE. You must NOT infer or assume evidence.'
- User prompt: Includes 7-gate checklist + evidence-grounding rules + output format + change bundle + 'For each gate, cite the exact text from the bundle that supports PASS. If no evidence exists, mark MISSING_EVIDENCE. Final decision cannot be READY if any critical gate (G1-G4) is MISSING_EVIDENCE.'

## Models

Use OpenRouter API (OPENROUTER_API_KEY from env):
1. anthropic/claude-sonnet-4 (strong frontier)
2. anthropic/claude-haiku-3.5 (cost-effective)
3. meta-llama/llama-4-maverick (open-weight)

If any model is unavailable, substitute with nearest equivalent and document.

## Settings
- temperature: 0
- max_tokens: 2048
- top_p: 1
- No system-level randomness
- Each call is independent (no conversation history)

## Execution Order
- Run all 12 cases × 3 modes for each model sequentially
- Save: raw JSON response, parsed output, timing, token counts, cost
- Total: 108 calls
- Estimated time: ~15-30 min depending on rate limits
- Estimated cost: <$5 total

## Output Files
- results/raw_outputs/{model}_{mode}_{case_id}.json
- results/relgate_pilot_results.csv (one row per call)
- results/summary_metrics.csv (aggregated by mode)

## Reproducibility
- All prompts versioned in prompts/ directory
- Exact model identifiers recorded
- Timestamp of each call recorded
- reproduce.sh script provided
- requirements.txt with pinned versions
