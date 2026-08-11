# RelGate

### Evidence-Grounded Readiness Gates for LLM-Reviewed Cloud Changes

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Benchmark: 12 scenarios](https://img.shields.io/badge/Benchmark-12_scenarios-green.svg)](benchmark/cases/)
[![Experiments: 108 calls](https://img.shields.io/badge/Experiments-108_calls-orange.svg)](results/raw_outputs/)

**Paper status**: Accepted to the [ISSRE 2026](https://cyprusconferences.org/issre2026/) Fast Abstracts / Project Highlights track (Submission 357). The work is not yet published; no DOI has been assigned.

**Author**: [Lokesh Chauhan](https://orcid.org/0009-0004-1544-6424), Independent Researcher

> This work was conducted independently and does not relate to the author's employment. No employer resources, data, or confidential information were used.

---

## Overview

Freeform LLM review may block adequately documented changes, while checklist review may mark gates satisfied without source support. RelGate instead requires each PASS to cite a bundle span or explicitly mark evidence missing.

For the camera-ready analysis, a citation is supported only when the complete quoted span occurs verbatim and contiguously in the supplied bundle after case normalization and whitespace collapsing. A quote may be shorter than its source sentence. Paraphrases, semantic equivalents, fuzzy matches, and prefix/suffix-only matches are unsupported. A literal match can still be irrelevant or insufficient; this metric does not assess either question.

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

1. **Freeform review was over-conservative in this sample.** All models blocked every change, including the READY controls (false-block = 1.000), yielding 0.750 decision accuracy.

2. **Checklist structure reduced false blocking but had more unsupported claims than RelGate.** M1 reached 0.972 accuracy; its mean per-response unsupported-claim fraction was 0.208 versus 0.056 for M2.

3. **RelGate produced no observed false-ready or false-block decisions in this pilot.** M2 had 1.000 observed decision accuracy. These are feasibility results, not production accuracy or zero-risk estimates.

The experiment treats production-readiness review as evidence auditing as well as pass/fail classification.

---

## Results

### Decision Accuracy by Review Mode

| Metric | M0 Freeform | M1 Checklist | M2 RelGate |
|:-------|:-----------:|:------------:|:----------:|
| Critical Gap Recall | 0.975 | 1.000 | **1.000** |
| False-Ready Rate (n=27) | 0.000 | 0.000 | **0.000** |
| False-Block Rate (n=9) | 1.000 | 0.111 | **0.000** |
| Unsupported Evid. Claims | 0.035 | 0.208 | **0.056** |
| Decision Accuracy (n=36) | 0.750 | 0.972 | **1.000** |
| Actionability (0-2) | 1.58 | 1.74 | **1.74** |

Full scored results: [`results/full_relgate_scored_results.csv`](results/full_relgate_scored_results.csv)

Summary metrics: [`results/full_summary_metrics.csv`](results/full_summary_metrics.csv)

Metric derivation: [`results/metric_sanity_report.md`](results/metric_sanity_report.md)

Model-level metrics: [`results/camera_ready_model_level_metrics.csv`](results/camera_ready_model_level_metrics.csv)

95% Wilson intervals: [`results/camera_ready_wilson_intervals.csv`](results/camera_ready_wilson_intervals.csv)

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

Each case/model/mode tuple was called once at temperature 0. Repeated-run or stochastic robustness was not measured. Total experiment cost: ~$1.30.

---

## Reproducing Results

### Requirements

- Python 3.10+
- `OPENROUTER_API_KEY` only for new experiments; it is not needed for frozen-output reproduction

```bash
pip install -r requirements.txt
```

### Reproducing the Camera-Ready Results (No API Calls)

All 108 frozen raw outputs are included. These commands perform only local validation and scoring:

```bash
python3 scripts/preflight.py
python3 -m unittest discover -s tests -v
python3 scripts/camera_ready_audit.py
python3 src/score_results.py --input-dir results/raw_outputs --output-prefix full
python3 src/make_tables.py
```

### Running New Experiments (Not Part of Camera-Ready Reproduction)

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

- Small, gate-aligned synthetic pilot; it may favor instruction compliance and does not establish production calibration.
- READY controls are fully specified; real evidence may be ambiguous, stale, conflicting, incomplete, or organization-specific.
- One temperature-0 observation per case/model/mode; repeated-run robustness is unknown.
- Literal quotation validity is not semantic relevance or operational adequacy.
- Deterministic checks can cover some literal readiness conditions; a deterministic baseline is future work.
- Larger real/anonymized records and expert/developer evaluation are needed.

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
