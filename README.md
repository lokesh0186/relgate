# RelGate

### Evidence-Grounded Readiness Gates for LLM-Reviewed Cloud Changes

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Benchmark: 12 scenarios](https://img.shields.io/badge/Benchmark-12_scenarios-green.svg)](benchmark/cases/)
[![Experiments: 108 calls](https://img.shields.io/badge/Experiments-108_calls-orange.svg)](results/raw_outputs/)

**Paper**: Submitted to the [37th IEEE International Symposium on Software Reliability Engineering (ISSRE 2026)](https://cyprusconferences.org/issre2026/), Fast Abstracts / Project Highlights track. Conference: October 20-23, 2026, Limassol, Cyprus. Accepted papers appear in IEEE Xplore.

**Author**: [Lokesh Chauhan](https://orcid.org/0009-0004-1544-6424), Independent Researcher

> This work was conducted independently and does not relate to the author's employment. No employer resources, data, or confidential information were used.

---

## Overview

LLM-assisted production-readiness review can be poorly calibrated: free-form review may block safe changes, while checklist review may approve changes with fabricated evidence. RelGate addresses this with an **evidence-grounded gate framework** that requires every readiness decision to cite exact text from the change bundle or explicitly mark evidence as missing.

### The Seven Readiness Gates

| Gate | Category | Question |
|------|----------|----------|
| **G1: Observability** | Critical | Dashboard/metric/log evidence to detect impact? |
| **G2: Alerting** | Critical | Alert coverage for failure modes? |
| **G3: Rollout Safety** | Critical | Staged rollout or blast-radius control? |
| **G4: Rollback** | Critical | Specific revert plan with trigger condition? |
| **G5: Ownership** | Major | On-call and escalation path identified? |
| **G6: Reliability Impact** | Major | SLO or error-budget analysis? |
| **G7: Validation** | Major | Test/staging/dry-run evidence? |

A change is **READY** only if all critical gates have cited evidence. Any critical gate with missing evidence produces **FIX-BEFORE-SHIP**.

---

## Key Findings

From **108 evaluation calls** across 3 models, 3 review modes, and 12 scenarios (9 unsafe + 3 READY controls):

1. **Free-form review is safe but over-conservative.** All models blocked every change including safe controls (false-block = 1.000), yielding only 0.750 decision accuracy.

2. **Checklist structure improves specificity but increases unsupported claims.** M1 reached 0.972 accuracy but produced 4x more unsupported evidence claims than evidence-grounded review (0.208 vs. 0.053).

3. **Evidence grounding improves calibration.** M2 achieved 1.000 decision accuracy with zero false-ready, zero false-block, and the lowest unsupported-claim rate, by requiring models to cite real bundle text or honestly report missing evidence.

**Main lesson**: Production-readiness review should be evaluated as an evidence-auditing task, not only as a pass/fail classification task.

---

## Results

### Decision Accuracy by Review Mode

| Metric | M0 Freeform | M1 Checklist | M2 RelGate |
|:-------|:-----------:|:------------:|:----------:|
| Critical Gap Recall | 0.975 | 1.000 | **1.000** |
| False-Ready Rate (n=27) | 0.000 | 0.000 | **0.000** |
| False-Block Rate (n=9) | 1.000 | 0.111 | **0.000** |
| Unsupported Evid. Claims | 0.062 | 0.208 | **0.053** |
| Decision Accuracy (n=36) | 0.750 | 0.972 | **1.000** |
| Actionability (0-2) | 1.58 | 1.74 | **1.74** |

Full scored results: [`results/full_relgate_scored_results.csv`](results/full_relgate_scored_results.csv)

Summary metrics: [`results/full_summary_metrics.csv`](results/full_summary_metrics.csv)

Metric derivation: [`results/metric_sanity_report.md`](results/metric_sanity_report.md)

---

## Benchmark

12 synthetic cloud-change scenarios spanning common infrastructure change types:

| Case | Type | Expected Decision |
|:-----|:-----|:-----------------|
| C01 | Database migration (PostgreSQL) | FIX-BEFORE-SHIP |
| C02 | Cache TTL change (Redis) | FIX-BEFORE-SHIP |
| C03 | K8s resource limit change | FIX-BEFORE-SHIP |
| C04 | Terraform RDS upgrade | FIX-BEFORE-SHIP |
| C05 | Load balancer routing | FIX-BEFORE-SHIP |
| C06 | Auth config change (OAuth) | FIX-BEFORE-SHIP |
| C07 | Observability/logging change | FIX-BEFORE-SHIP |
| C08 | Queue worker concurrency | FIX-BEFORE-SHIP |
| C09 | Feature flag rollout (100%) | FIX-BEFORE-SHIP |
| C10 | K8s HPA scaling | **READY** (control) |
| C11 | Feature flag staged rollout | **READY** (control) |
| C12 | CDN/DNS routing | **READY** (control) |

Each unsafe case has 2-6 seeded gaps with ground-truth severity labels (critical/major). READY controls have complete evidence for all seven gates.

- Scenario files: [`benchmark/cases/`](benchmark/cases/)
- JSON schema: [`benchmark/schema.json`](benchmark/schema.json)

---

## Models

| Model | Family | Type | Access |
|:------|:-------|:-----|:-------|
| GPT-5.5 | OpenAI | Commercial | [OpenRouter](https://openrouter.ai/) |
| Grok 4.3 | xAI | Commercial | [OpenRouter](https://openrouter.ai/) |
| Llama 4 Maverick | Meta | Open-weight | [OpenRouter](https://openrouter.ai/) |

All calls use temperature 0 for deterministic outputs. Total experiment cost: ~$1.30.

---

## Reproducing Results

### Requirements

- Python 3.10+
- `OPENROUTER_API_KEY` environment variable

```bash
pip install -r requirements.txt
```

### Running Experiments

```bash
# Step 1: Validate setup (no API calls)
python3 scripts/preflight.py

# Step 2: Run smoke test (18 calls, ~$0.23)
python3 src/run_experiment.py --profile smoke

# Step 3: Score smoke results
python3 src/score_results.py --input-dir results/raw_outputs_smoke --output-prefix smoke

# Step 4: Run full experiment (108 calls, ~$1.30)
python3 src/run_experiment.py --profile full

# Step 5: Score full results
python3 src/score_results.py --input-dir results/raw_outputs --output-prefix full

# Step 6: Generate paper table and figure
python3 src/make_tables.py
python3 src/make_figures.py
```

### Using Pre-Computed Results

All 108 raw outputs are included. To verify scoring without re-running API calls:

```bash
python3 src/score_results.py --input-dir results/raw_outputs --output-prefix full
python3 src/make_tables.py
```

Output: [`results/full_summary_metrics.csv`](results/full_summary_metrics.csv)

---

## Repository Structure

```
relgate/
├── paper/
│   ├── main.tex                          # Paper source (LaTeX, IEEE format)
│   ├── main.pdf                          # Compiled paper (2 pages)
│   └── references.bib                    # BibTeX references
│
├── benchmark/
│   ├── cases/                            # 12 change scenarios (JSON)
│   │   ├── case_001.json ... case_009.json  # 9 unsafe cases
│   │   └── case_010.json ... case_012.json  # 3 READY controls
│   └── schema.json                       # JSON schema for bundles
│
├── prompts/
│   ├── m0_freeform.txt                   # M0: Unstructured review
│   ├── m1_checklist.txt                  # M1: G1-G7 checklist
│   └── m2_evidence_grounded.txt          # M2: Evidence-grounding rule
│
├── src/
│   ├── run_experiment.py                 # Experiment runner (OpenRouter)
│   ├── score_results.py                  # Automated scoring
│   ├── make_tables.py                    # LaTeX table generation
│   └── make_figures.py                   # Architecture figure
│
├── scripts/
│   └── preflight.py                      # Pre-run validation
│
├── configs/
│   └── experiment_config.json            # Model/mode/budget config
│
├── results/
│   ├── raw_outputs/                      # 108 raw JSON responses
│   ├── full_relgate_scored_results.csv   # Scored results (108 rows)
│   ├── full_summary_metrics.csv          # Summary by mode
│   └── metric_sanity_report.md           # Metric derivation audit
│
├── research/
│   ├── venue_fit.md                      # ISSRE 2026 venue analysis
│   ├── related_work_matrix.md            # Prior work gap analysis
│   └── novelty_claim.md                  # Contribution positioning
│
├── docs/
│   └── relgate_design.md                 # Framework design document
│
├── experiments/
│   ├── experiment_plan.md                # Pilot design rationale
│   └── metrics.md                        # Metric definitions
│
├── CITATION.cff                          # Citation metadata
├── LICENSE                               # MIT License
├── README.md                             # This file
├── requirements.txt                      # Python dependencies
├── reproduce.sh                          # Reproduction script
└── .gitignore                            # Git ignore rules
```

---

## Limitations

- Small pilot: 12 synthetic scenarios, not production change records
- READY controls are fully specified; real evidence is often ambiguous or stale
- Evidence presence does not guarantee production safety; it only enables auditability
- Model versions evolve; results may not generalize to future releases
- No developer trust, latency, or deployment integration measurement yet

---

## Citation

If you use RelGate in your research, please cite:

```bibtex
@inproceedings{chauhan2026relgate,
  title={{RelGate}: Evidence-Grounded Readiness Gates for {LLM}-Reviewed Cloud Changes},
  author={Chauhan, Lokesh},
  booktitle={Proc. IEEE Int. Symp. Software Reliability Engineering (ISSRE), Fast Abstracts / Project Highlights},
  year={2026}
}
```

---

## License

This project is licensed under the [MIT License](LICENSE).
