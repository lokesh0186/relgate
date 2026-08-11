# Humanization Diff Audit

## Scope and baseline

- Starting branch: `main`
- Starting HEAD: `bdfa34e94a5ce0cdd86e2dbce0e73afa37f7953a`
- Working branch: `camera-ready/issre2026-357-human-prose`
- Scope: prose and punctuation only. No experiment, scoring, table, figure architecture, citation metadata, or disclosure changes.
- Pre-existing untracked file preserved: `paper/ISSRE_2027_paper_357_submitted.pdf`

## Paragraph-level audit

| Section | Old wording summary | New wording summary | Scientific meaning changed? | Metrics changed? | Citation support changed? | Reviewer-response content preserved? |
|---|---|---|---|---|---|---|
| Abstract | Dense compound sentences described the problem, method, experiment, results, and limits. | Recast as short direct sentences; removed prose em dashes and stacked qualifications. | NO | NO | NO | YES |
| Motivation, opening paragraph | Used a semicolon, `source-traceability concern`, and an abstract contrast with hallucination taxonomies. | Split the control result into two sentences and directly described unsupported PASS judgments. | NO | NO | NO | YES |
| Motivation, prior-work paragraph | Positioned RelGate as `complementary to` three methods in two balanced sentences. | Described RAG, Chain-of-Verification, and structured generation separately, then stated RelGate's narrower task. | NO | NO | NO | YES |
| Figure 1 caption | Joined the evidence rule and decision rule with a semicolon. | Used two sentences; the critical/major behavior is unchanged. | NO | NO | NO | YES |
| RelGate Design, gate rationale | Used a compressed taxonomy sentence and `pilot operationalization`. | Explained the same detection, containment/recovery, accountability, service-impact, and validation roles in direct sentences; retained configurability. | NO | NO | NO | YES |
| RelGate Design, evidence rule | Used a long contrast and the abstract phrase `evaluation dimensions`. | Kept verbatim-contiguous matching and normalization rules explicit; stated directly that literal support alone does not establish relevance or sufficiency. | NO | NO | NO | YES |
| Pilot Study, setup | Used passive procedural wording (`Each was reviewed`). | Used active first-person wording and retained every scenario, mode, model, access, temperature, and call-count detail. | NO | NO | NO | YES |
| Pilot Study, metrics and scoring | Used `The latter`, a colon, and a semicolon to compress definitions. | Named Unsupported Evidence Claims directly and separated deterministic scoring, seeded-missing PASS handling, and lack of human adjudication. | NO | NO | NO | YES |
| Preliminary Results, aggregate results | Ended with a formulaic `Thus` sentence. | Reported M2's observed errors, accuracy, and unsupported-claim fraction directly. | NO | NO | NO | YES |
| Preliminary Results, model/example paragraph | Used one balanced model sentence and a rhetorical `illustrating why` clause. | Split model results from the example and stated plainly that the decision was correct but its quoted support was not. | NO | NO | NO | YES |
| Preliminary Results, uncertainty | Began with the abstract phrase `Uncertainty is substantial`. | Began with the concrete reason: the sample is small. Wilson intervals and zero-risk warning are unchanged. | NO | NO | NO | YES |
| Discussion and Limitations, feasibility and validity | Used `production effectiveness`, `seven-gate ontology`, and `bound these findings`. | Used direct language about the synthetic pilot, shared gates, instruction compliance, realistic evidence, repeat runs, and model versions. | NO | NO | NO | YES |
| Discussion and Limitations, deterministic checks and future study | Used `complementary evidence-to-decision problem` and a long future-work list. | Explained simple deterministic checks directly and separated the future design, four evaluation aspects, and evidence-quality requirements. | NO | NO | NO | YES |
| Acknowledgment | Disclosed Codex language and scoring/test-code assistance and independent author verification. | Unchanged byte-for-byte from the starting manuscript. | NO | NO | NO | YES |

## Repository prose

README edits were limited to four passages: the overview no longer says `addresses this with a framework`; the exact-span paragraph uses direct sentences; the M2 finding reports the observed outcomes without `best observed decision behavior`; and the canned `Main lesson` label was removed. Accepted status, strict scoring semantics, corrected metrics, limitations, commands, and artifact paths are unchanged.

## Numeric and scientific guard

- The sorted counts of every numeric token in `paper/main.tex` are identical before and after the rewrite (`diff` produced no output).
- `paper/tables/results_table.tex` was not edited.
- Required values remain present: 12, 9, 3, 108, 27, 36, 0.975, 1.000, 0.000, 0.111, 0.035, 0.208, 0.056, 0.750, 0.972, 0.138, 0.031, 0.333, 0.083, 0.125, 0.299, and 95\%.
- The citation-command sequence in `paper/main.tex` is identical before and after.
- `paper/references.bib`, all result files, prompts, benchmark cases, scorer code, and Table I were not edited.
- Section headings and order are unchanged.
- The AI acknowledgment is identical before and after.

## Reviewer-response preservation

- Reviewer 1: RAG, Chain-of-Verification, and structured-generation positioning remain; gate rationale/configurability and strict exact-span semantics remain; the synthetic-study limitation remains.
- Reviewer 2: deterministic quote scoring, seeded-missing PASS handling, no human adjudication, real-evidence ambiguity categories, and the deterministic-baseline limitation remain.
- Reviewer 3: benchmark/policy alignment, instruction-compliance interpretation, non-production interpretation of 1.000, model-level results, Wilson intervals, single-run limitation, and the four separate future evaluation questions remain.

## Punctuation audit

- Authored prose `---` count: 2 before, 0 after.
- Full-file semicolon count: 23 before, 11 after.
- The 11 remaining semicolons are TikZ command terminators plus the separator in the Figure 1 gate-label node. No prose sentence retains a semicolon.

## Final manual prose audit

The following sentences or phrases were reviewed and intentionally kept:

- `RelGate treats this as evidence auditing rather than open-ended advice.` **KEEP**: concise statement of the task distinction.
- `The Unsupported Evidence Claims metric is the mean ...` **KEEP**: exact metric definition; simplifying it further risks changing the denominator semantics.
- `M0's lower unsupported-claim fraction coincided with blocking all READY controls.` **KEEP**: necessary explanation of the M0/M2 tradeoff visible in Table I.
- `Its 1.000 decision accuracy may therefore reflect compliance ...` **KEEP**: `therefore` states the direct reason for the reviewer-requested benchmark-alignment caveat.
- `A deterministic baseline remains future work.` **KEEP**: compact and explicitly requested by the reviewers.
- `These are zero observed errors, not zero risk.` **KEEP**: necessary qualification of the Wilson intervals and zero observed rates.

No remaining sentence was marked **REWRITE** after the final pass. Repeated uses of `evidence`, `decision`, and `accuracy` were retained where they name the mechanism or reported metrics.

## Build and visual result

- Clean IEEEtran build: PASS.
- Page count: 2.
- Page size: US Letter (612 x 792 pt).
- Fonts: embedded Type 1 only; no Type 3 fonts.
- LaTeX log: no overfull boxes, unresolved citations, or broken references.
- 200-DPI inspection: no clipping, overlap, unreadable figure/table text, or reference crowding; acknowledgment and independence footnote are present.
- `qpdf`: not available in the environment; PDF is unencrypted and parsed successfully by Poppler.
