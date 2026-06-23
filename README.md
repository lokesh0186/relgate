# RelGate: Evidence-Grounded Readiness Gates for LLM-Reviewed Cloud Changes

**Paper**: Submitted to IEEE ISSRE 2026 Fast Abstracts / Project Highlights Track

## Overview

RelGate is a project prototype and experimental framework that evaluates whether LLM-assisted production-readiness review can be made auditable through evidence-grounded gates. Instead of accepting free-form LLM approval or rejection, RelGate requires every readiness decision to cite exact evidence from the change bundle or explicitly mark evidence as missing.

**Key findings** from a 108-call pilot across 3 models and 3 review modes:
- Free-form review (M0) is safe but over-conservative: it blocked all READY controls (false-block = 1.000, accuracy = 0.750)
- Checklist review (M1) improved specificity but increased unsupported evidence claims (0.208 vs. 0.053)
- Evidence-grounded review (M2) achieved the best calibration: zero false-ready, zero false-block, 1.000 decision accuracy, and the lowest unsupported-claim rate (0.053)

**Main lesson**: Production-readiness review should be evaluated as an evidence-auditing task, not only as a pass/fail classification task.

## Repository Structure

```
relgate/
├── paper/
│   ├── main.tex                 # Paper source (LaTeX, IEEE format)
│   ├── main.pdf                 # Compiled paper (2 pages)
│   └── references.bib           # BibTeX references
├── benchmark/
│   ├── cases/                   # 12 change scenarios (JSON)
│   │   ├── case_001.json        # Database migration (unsafe)
│   │   ├── case_002.json        # Cache TTL change (unsafe)
│   │   ├── case_003.json        # K8s resource limit (unsafe)
│   │   ├── case_004.json        # Terraform RDS upgrade (unsafe)
│   │   ├── case_005.json        # Load balancer routing (unsafe)
│   │   ├── case_006.json        # Auth config change (unsafe)
│   │   ├── case_007.json        # Observability/logging (unsafe)
│   │   ├── case_008.json        # Queue worker concurrency (unsafe)
│   │   ├── case_009.json        # Feature flag rollout (unsafe)
│   │   ├── case_010.json        # K8s HPA scaling (READY control)
│   │   ├── case_011.json        # Feature flag staged (READY control)
│   │   └── case_012.json        # CDN/DNS routing (READY control)
│   └── schema.json              # JSON schema for change bundles
├── prompts/
│   ├── m0_freeform.txt          # M0: Unstructured review prompt
│   ├── m1_checklist.txt         # M1: G1-G7 checklist prompt
│   └── m2_evidence_grounded.txt # M2: Evidence-grounding prompt
├── src/
│   ├── run_experiment.py        # Experiment runner (OpenRouter API)
│   ├── score_results.py         # Automated scoring script
│   ├── make_tables.py           # LaTeX table generation
│   └── make_figures.py          # Architecture figure generation
├── scripts/
│   └── preflight.py             # Pre-run validation checks
├── configs/
│   └── experiment_config.json   # Model/mode/budget configuration
├── results/
│   ├── raw_outputs/             # 108 raw JSON responses
│   ├── full_relgate_scored_results.csv  # Scored results (108 rows)
│   ├── full_summary_metrics.csv         # Summary by mode
│   └── metric_sanity_report.md          # Metric derivation audit
├── research/
│   ├── venue_fit.md             # ISSRE 2026 venue analysis
│   ├── related_work_matrix.md   # Prior work gap analysis
│   └── novelty_claim.md         # Contribution positioning
├── docs/
│   └── relgate_design.md        # Framework design document
├── experiments/
│   ├── experiment_plan.md       # Pilot design rationale
│   └── metrics.md               # Metric definitions
├── README.md                    # This file
├── LICENSE                      # MIT License
├── CITATION.cff                 # Citation metadata
├── requirements.txt             # Python dependencies
└── reproduce.sh                 # Reproduction script
```

## Experiment Design

| Parameter | Value |
|-----------|-------|
| Scenarios | 12 (9 unsafe + 3 READY controls) |
| Models | GPT-5.5, Grok 4.3, Llama 4 Maverick |
| Modes | M0 Freeform, M1 Checklist, M2 Evidence-Grounded |
| Total calls | 108 |
| Temperature | 0 |
| API | OpenRouter |
| Cost | ~$1.30 total |

## Results Summary

| Metric | M0 Freeform | M1 Checklist | M2 RelGate |
|--------|:-----------:|:------------:|:----------:|
| Critical Gap Recall | 0.975 | 1.000 | 1.000 |
| False-Ready Rate (n=27) | 0.000 | 0.000 | 0.000 |
| False-Block Rate (n=9) | 1.000 | 0.111 | 0.000 |
| Unsupported Evid. Claims | 0.062 | 0.208 | 0.053 |
| Decision Accuracy (n=36) | 0.750 | 0.972 | 1.000 |
| Actionability (0-2) | 1.58 | 1.74 | 1.74 |

## Seven Readiness Gates

| Gate | Category | Question |
|------|----------|----------|
| G1 Observability | Critical | Dashboard/metric/log evidence to detect impact? |
| G2 Alerting | Critical | Alert coverage for failure modes? |
| G3 Rollout Safety | Critical | Staged rollout or blast-radius control? |
| G4 Rollback | Critical | Specific revert plan with trigger? |
| G5 Ownership | Major | On-call and escalation path identified? |
| G6 Reliability Impact | Major | SLO or error-budget analysis? |
| G7 Validation | Major | Test/staging/dry-run evidence? |

## Reproduction

```bash
# Prerequisites: Python 3.10+, OPENROUTER_API_KEY environment variable
pip install -r requirements.txt

# Validate setup
python3 scripts/preflight.py

# Run experiment (108 API calls, ~$1.30)
python3 src/run_experiment.py --profile full

# Score results
python3 src/score_results.py --input-dir results/raw_outputs --output-prefix full

# Generate table and figure
python3 src/make_tables.py
python3 src/make_figures.py
```

## Limitations

- Small pilot: 12 synthetic scenarios, not production change records
- READY controls are fully specified; real evidence is often ambiguous
- Evidence presence does not guarantee production safety
- Model versions evolve; results may not generalize to future releases
- No developer trust or latency measurement yet

## Citation

```bibtex
@inproceedings{chauhan2026relgate,
  title     = {RelGate: Evidence-Grounded Readiness Gates for LLM-Reviewed Cloud Changes},
  author    = {Chauhan, Lokesh},
  booktitle = {Proc. IEEE Int. Symp. Software Reliability Engineering (ISSRE), Fast Abstracts / Project Highlights},
  year      = {2026},
  note      = {Submitted}
}
```

## License

MIT License. See [LICENSE](LICENSE).
