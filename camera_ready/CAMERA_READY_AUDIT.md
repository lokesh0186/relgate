# ISSRE 2026 Camera-Ready Audit

Paper: *RelGate: Evidence-Grounded Readiness Gates for LLM-Reviewed Cloud Changes*
Submission: 357, Fast Abstracts / Project Highlights
Decision: Accepted

## Disposition

Scientific, artifact, publication-policy, and PDF checks pass for camera-ready submission review. The author-requested IEEE AI-use acknowledgment is present in the final PDF.

## Repository and baseline

- Initial branch: `main`
- Initial HEAD: `0009fc374eb47644c24f199b42e0b4560f838a93`
- Initial dirty state preserved: modified `paper/main.tex`, modified `paper/main.pdf`, and untracked `paper/ISSRE_2027_paper_357_submitted.pdf`
- Camera-ready branch: `camera-ready/issre2026-357`
- Frozen hashes: `camera_ready/ACCEPTED_BASELINE_HASHES.txt`
- Rechecked frozen inputs: 123 benchmark, prompt, and raw-output files; zero hash mismatches
- No benchmark case, prompt, or raw response was modified
- No tag, release, or new model/API call was performed

## Official constraints checked

The official ISSRE Fast Abstract / Project Highlights call describes these papers as two-page technical articles, requires English, IEEE Computer Society formatting, a single PDF with embedded fonts, and lists August 19, 2026 AoE as the camera-ready deadline: <https://cyprusconferences.org/issre2026/fast-abstract-track/>.

The final file uses IEEEtran conference mode at its normal 10-point US Letter settings. It has two pages including references. No manual copyright footer, ISBN, DOI, PDF eXpress identifier, geometry override, font reduction, negative vertical-space hack, or line-spacing compression was introduced. Later author-specific camera-ready instructions remain authoritative if they conflict.

## Data reproduction and scoring correction

The accepted scorer reproduced the accepted table exactly from the frozen 108 outputs before any scoring change. Integrity checks found 108 usable/parsed rows, 36 per mode, 27 unsafe and 9 READY observations per mode, three final model identifiers, complete 12-by-3-by-3 coverage, and no duplicate, missing, extra, Claude, Sonnet, or Anthropic result rows.

The accepted exact-quote matcher could accept only a quote prefix or suffix and compared against a JSON serialization rather than the exact labeled bundle shown to the model. The corrected scorer requires the complete case/whitespace-normalized quote to occur contiguously in that visible bundle. Five quote classifications changed. Only the macro Unsupported Evidence Claims row changed: M0 0.062 to 0.035; M1 remained 0.208; M2 0.053 to 0.056. M2 remains below M1. All decision, recall, and actionability results are unchanged.

Full evidence is in `METRIC_REVALIDATION.md`, `SCORING_CHANGELOG.md`, and `exact_evidence_sensitivity.csv`. Historical accepted-reproduction CSVs are retained rather than rewriting the audit trail.

## Paper changes

- Rewrote the abstract to report observed controlled-pilot results and explicitly reject a production-accuracy interpretation.
- Added compact primary-source positioning against RAG, Chain-of-Verification, and format-constrained generation.
- Added a rationale for the seven gates and made the gate taxonomy explicitly configurable and non-universal.
- Reconciled Fig. 1 with the deterministic gate policy: only missing critical-gate evidence blocks; missing major-gate evidence raises a warning.
- Defined exact evidence as a verbatim contiguous source span after case/whitespace normalization only.
- Documented deterministic unsupported-claim scoring, seeded-missing PASS treatment, macro averaging, and absence of human adjudication.
- Added model-level outcomes and 95% Wilson intervals without adding another paper table.
- Added all requested limitations: synthetic/controlled scope, shared-ontology instruction-compliance risk, clean controls, ambiguous/stale/conflicting/incomplete/organization-specific evidence, one temperature-0 observation, deterministic checks, and separate future assessment of correctness, quote validity, semantic relevance, and adequacy.
- Removed general calibration/perfect-performance language while retaining the observed 1.000 statistic.
- Explained that M0's lower unsupported-claim fraction coincided with blocking every READY control.
- Added an IEEE acknowledgment identifying OpenAI Codex, Sections I--V, scoring/test code, and the author's independent verification.
- Retained Fig. 1 and Table I. Actionability remains in the artifact but is omitted from Table I to prioritize decision/evidence metrics and uncertainty.

## Reference audit

Existing bibliography records were checked and corrected using publisher or venue sources. The camera-ready paper cites six directly relevant sources. Reviewer-requested records use official NeurIPS or ACL Anthology metadata:

- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020;
- Dhuliawala et al., *Chain-of-Verification Reduces Hallucination in Large Language Models*, Findings of ACL 2024, DOI `10.18653/v1/2024.findings-acl.212`; and
- Tam et al., *Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models*, EMNLP 2024 Industry Track, DOI `10.18653/v1/2024.emnlp-industry.91`.

No secondary blog was used to construct bibliography metadata. No DOI was invented for this paper, and neither the paper nor artifact claims that it is already in IEEE Xplore.

## Artifact alignment

Updated `README.md`, `CITATION.cff`, `docs/relgate_design.md`, `experiments/experiment_plan.md`, `experiments/metrics.md`, `results/metric_sanity_report.md`, final scored/summary CSVs, scoring code, tests, table generator, and the no-API reproduction script.

The README status is “Accepted to the ISSRE 2026 Fast Abstracts / Project Highlights track (Submission 357)” and explicitly says not yet published/no DOI. Paper, README, table source, summary CSV, and metric report agree on final values. `CITATION.cff` carries acceptance status but no DOI.

## Reproducibility checks

`./reproduce.sh` passed and made no model/API calls. It ran:

- repository preflight;
- five strict exact-span regression tests;
- frozen-output integrity and sensitivity audit;
- strict rescoring of all 108 outputs;
- summary regeneration; and
- LaTeX table regeneration from `results/full_summary_metrics.csv`.

Python compilation checks passed for `src/*.py` and `scripts/*.py`. The generated `paper/tables/results_table.tex` matches the final summary CSV.

## PDF preflight

- Pages: 2
- Page size: 612 x 792 pt, US Letter
- Encrypted: no
- PDF version: 1.7
- Fonts: ten Type 1 subsets; every font embedded; no Type 3 fonts
- Final LaTeX log: no overfull boxes, missing citations, unresolved references, or errors
- Text extraction: title, author, email, Table I values, and artifact URL present
- Forbidden-status scan: no TODO, FIXME, DRAFT, PLACEHOLDER, TBD, anonymous, redacted, sample, lorem, Claude, Sonnet, calibration, perfect, or submitted text in the final PDF
- `qpdf`: unavailable in the environment, so the conditional `qpdf --check` was not run; `pdfinfo`, `pdffonts`, `pdftotext`, successful Poppler page rendering, and per-page extraction were used instead

Raw outputs are stored in `PDFINFO_FINAL.txt` and `PDFFONTS_FINAL.txt`. Visual findings are in `RENDERED_PAGE_INSPECTION.md`.

## AI-content policy compliance

IEEE's current conference policy says AI-generated article content, including text and code, must be disclosed in the Acknowledgment with the system, affected sections, and level of use; editing/grammar-only use is generally outside the mandatory policy: <https://conferences.ieeeauthorcenter.ieee.org/author-ethics/guidelines-and-policies/submission-policies/>.

Camera-ready work in this repository included substantive AI-assisted manuscript revision and deterministic scoring/test code. After author direction, the final PDF now contains this acknowledgment immediately before References:

Draft for author approval and adaptation:

> OpenAI Codex was used during camera-ready preparation to assist with language revision in Sections I--V and with implementation/review of deterministic scoring and test code used to verify the unsupported-evidence metric. The author independently verified all outputs, analyses, results, and conclusions.

The rebuilt PDF remains exactly two pages with normal IEEE typography, embedded Type 1 fonts, and a visible lower-margin safety reserve.

## Remaining scientific limitations

The study remains a 12-case synthetic feasibility pilot. It does not measure production effectiveness, stochastic robustness, semantic relevance, operational adequacy, developer trust, or causal superiority over deterministic baselines. The shared M2/benchmark ontology may favor instruction compliance. Wilson intervals remain wide, especially for 0/9 false blocks. These limitations are stated in the paper rather than resolved by unsupported new claims.
