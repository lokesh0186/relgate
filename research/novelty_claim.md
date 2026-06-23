# RelGate — Novelty Claim

**Target venue:** ISSRE 2026 (Fast Abstracts / PhD Forum)  
**Paper:** RelGate: A Lightweight LLM-Assisted Production-Readiness Gate for Cloud Changes

---

## Core Claim

RelGate contributes an early experimental framework for studying **false-ready decisions** in LLM-based production-readiness review. It introduces **evidence-grounded reliability gates** requiring exact support from the change bundle for readiness claims, and a small seeded benchmark for measuring gap recall, false-ready rate, evidence hallucination, and actionable remediation guidance.

---

## What We Do NOT Claim

- First-ever LLM readiness review system.
- First-ever cloud reliability gate.
- A fully validated production solution.
- A benchmark representative of all production cloud changes.
- Human-equivalent reliability assessment.

---

## Contributions

1. **Problem framing.** False-ready decisions and hallucinated readiness evidence in LLM-assisted production-readiness review.
2. **RelGate method.** Evidence-grounded reliability gates for observability, alerting, rollout, rollback, ownership, and reliability-impact evidence.
3. **Pilot benchmark.** 12 seeded cloud-change bundles with known missing readiness evidence across diverse change types.
4. **Preliminary empirical result.** Evidence-grounded prompting reduces false-ready and hallucinated-evidence behavior compared with free-form review.
5. **Artifact.** Prompts, benchmark cases, scoring scripts, raw results, and paper released on GitHub.

---

## Distinction from QRS Paper (IaC-Guard-V)

| Dimension | QRS / IaC-Guard-V | ISSRE / RelGate |
|-----------|-------------------|-----------------|
| Problem | Verifying LLM-generated IaC repair patches | Pre-deployment production-readiness review of arbitrary cloud changes |
| Domain | Terraform / Kubernetes IaC patches | Cloud-change bundles (code, config, IaC, pipeline artifacts) |
| Methodology | Verification gates V1–V4 | Evidence-grounded readiness gates G1–G7 |
| Metrics | Patch correctness, verification accuracy | Gap recall, false-ready rate, evidence hallucination, remediation actionability |

The two papers address orthogonal concerns: IaC-Guard-V asks "is this generated repair correct?" while RelGate asks "is this change ready for production?"

---

## Why This Is Not Obvious

1. **Production readiness ≠ code correctness.** LLMs are increasingly used for code review, but production readiness spans observability, alerting, rollout safety, rollback plans, and ownership — dimensions not captured by code-level analysis.
2. **SRE checklists are human-facing.** Existing production-readiness checklists (e.g., Google SRE PRR) are designed for human reviewers and are not structured for LLM interaction or automated evidence extraction.
3. **Hallucinated readiness evidence is unstudied.** The failure mode where an LLM fabricates evidence that a readiness criterion is satisfied (citing nonexistent configs, inventing metric names) has not been empirically characterized.
4. **Evidence grounding as mitigation is novel.** Requiring the LLM to cite exact artifacts from the change bundle as support for each readiness claim — and scoring the result for hallucination — is a new application of grounding techniques to the false-ready problem.

---

## ISSRE Positioning

RelGate directly addresses two topics from the ISSRE 2026 Call for Papers:

- **Reliability of AI-powered software systems.** We study the reliability failure modes of LLM-based review (false-ready, hallucinated evidence) and propose a mitigation (evidence grounding).
- **Metrics, measurement, assessment.** We define and operationalize metrics (gap recall, false-ready rate, evidence hallucination rate, remediation actionability) for evaluating LLM-based readiness review on a controlled benchmark.

---

## Scope Boundaries

This is an early-stage experimental study. Results are preliminary, the benchmark is small (12 cases), and the findings indicate directions rather than production-validated conclusions. The contribution is the framework, metrics, and initial evidence — not a deployable system.
