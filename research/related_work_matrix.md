# Related Work Matrix — RelGate (ISSRE 2026 FA/PH)

**Paper:** RelGate: A Lightweight LLM-Assisted Production-Readiness Gate for Cloud Changes  
**Last updated:** 2026-06-22

---

## 1. Production Readiness Reviews and Release Readiness

| Paper/Source | Venue/Year | Problem | Method | Handles prod-readiness evidence? | Measures false-ready? | Requires evidence citations? | Evaluates LLM readiness? | Gap relative to RelGate |
|---|---|---|---|---|---|---|---|---|
| Beyer et al., "Evolving SRE Engagement Model" (Ch. 32, *Site Reliability Engineering*) | O'Reilly / Google, 2016 | Scaling SRE engagement beyond per-service onboarding | Production Readiness Reviews (PRRs) as structured human-led assessments of service maturity | ✅ Yes — defines PRR checklist areas | ❌ No | ❌ No — human judgment, no citation mechanism | ❌ No | PRRs are manual, unscalable, and lack automation; no measurement of false-approval rates |
| Murphy et al., "Production Readiness Reviews: A Surprisingly Versatile Practice" | USENIX ;login:, 2019 [verify year] | Generalizing PRRs beyond Google's original scope | Defines PRR dimensions: observability, reliability, scalability, security, DR, alerting, deployments | ✅ Yes — structured checklist areas | ❌ No | ❌ No | ❌ No | Provides taxonomy of readiness dimensions but no automation, no LLM involvement, no false-ready measurement |
| Beyer et al., "Engagement Model" (*The Site Reliability Workbook*) | O'Reilly / Google, 2018 | Operationalizing SRE engagement patterns | Tiered engagement model with PRR as a gate | ✅ Yes | ❌ No | ❌ No | ❌ No | Describes organizational process but not automated evidence validation |

**Source URLs:**
- https://sre.google/sre-book/evolving-sre-engagement-model/
- https://www.usenix.org/publications/loginonline/production-readiness-reviews-surprisingly-versatile-practice
- https://sre.google/workbook/engagement-model/

---

## 2. SRE Checklists, Launch Reviews, Operational Readiness

| Paper/Source | Venue/Year | Problem | Method | Handles prod-readiness evidence? | Measures false-ready? | Requires evidence citations? | Evaluates LLM readiness? | Gap relative to RelGate |
|---|---|---|---|---|---|---|---|---|
| Google Launch Checklist (referenced in *Site Reliability Engineering*, Ch. 27) | O'Reilly / Google, 2016 | Ensuring services meet minimum reliability bar before launch | Manual checklist covering capacity, monitoring, rollback, etc. | ✅ Yes — checklist-based | ❌ No | ❌ No — binary check, no evidence trail | ❌ No | Static checklist; no adaptive reasoning about evidence completeness |
| AWS Well-Architected Framework — Operational Excellence Pillar | AWS, 2015–present | Guiding cloud architecture decisions for operational readiness | Five-pillar framework with review questions and best practices | ✅ Partially — advisory, not gating | ❌ No | ❌ No | ❌ No | Advisory framework, not an automated gate; no empirical evaluation of decision accuracy |
| Azure DevOps Operational Readiness Checklist patterns | Microsoft Azure, various | Pre-production validation for Azure workloads | Checklist templates for monitoring, alerting, DR, security | ✅ Partially — template-driven | ❌ No | ❌ No | ❌ No | Templates require manual completion; no LLM-driven assessment or hallucination measurement |

---

## 3. LLMs for Code Review / PR Review

| Paper/Source | Venue/Year | Problem | Method | Handles prod-readiness evidence? | Measures false-ready? | Requires evidence citations? | Evaluates LLM readiness? | Gap relative to RelGate |
|---|---|---|---|---|---|---|---|---|
| Li et al., "Automating Code Review Activities by Large-Scale Pre-Training" | FSE, 2022 | Automating code review comment generation and code refinement | CodeReviewer: pre-trained model on code review data for review comment generation and code revision | ❌ No — code-level review only | ❌ No | ❌ No | ❌ No — evaluates code quality, not deployment readiness | Operates at code diff level; does not assess operational/reliability evidence for production readiness |
| Tang et al., "Breaking Task Isolation: Enhancing Code Review Automation with MoE LLMs" | ISSRE, 2025 | Improving code review by breaking task isolation between review sub-tasks | Mixture-of-Experts LLM architecture for multi-task code review | ❌ No — code review focus | ❌ No | ❌ No | ❌ No | MoE architecture for code quality; no production-readiness dimension or evidence grounding |
| Fan et al., "Large Language Models for Software Engineering: A Systematic Literature Review" [verify exact title] | Various, 2023–2024 | Surveying LLM applications in SE including code review | Systematic review of ChatGPT/GPT-4 for code review tasks | ❌ No | ❌ No | ❌ No | Partially — evaluates LLM effectiveness for code tasks | Reviews LLM capability for code tasks but not for operational readiness gating |

---

## 4. LLMs for Incident Response / AIOps

| Paper/Source | Venue/Year | Problem | Method | Handles prod-readiness evidence? | Measures false-ready? | Requires evidence citations? | Evaluates LLM readiness? | Gap relative to RelGate |
|---|---|---|---|---|---|---|---|---|
| Ahmed et al., "Recommending Root-Cause and Mitigation Steps for Cloud Incidents using Large Language Models" | ICSE, 2023 | Automating root-cause analysis and mitigation recommendation for cloud incidents | Fine-tuned GPT-3/3.5 on historical incident data from Microsoft | ❌ No — post-incident, not pre-deployment | ❌ No | ❌ No — generates recommendations without evidence citations | Partially — evaluates LLM for incident tasks | Post-incident focus; does not address pre-deployment readiness or false-ready detection |
| Cui et al., "AetherLog: Log-based Root Cause Analysis by Integrating LLMs with Knowledge Graphs" | ISSRE, 2025 | Root cause analysis from logs using LLMs + KGs | Combines LLM reasoning with structured knowledge graphs for log-based RCA | ❌ No — post-incident RCA | ❌ No | Partially — KG provides grounding | Partially — evaluates LLM+KG for RCA accuracy | Knowledge graph grounding is related to evidence grounding, but applied to incident analysis not readiness review |
| Yan et al., "An Empirical Study of Production Incidents in Generative AI Cloud Services" | ISSRE, 2025 | Understanding failure patterns in GenAI cloud services | Empirical study of incident taxonomies and root causes | ❌ No — incident characterization | ❌ No | ❌ No | ❌ No — studies incidents in AI services, not LLM-as-reviewer | Characterizes incidents but does not propose prevention via pre-deployment gating |
| Chen et al., "Outage Mitigation in Microsoft Azure" [verify exact title] | ICSE-SEIP / FSE Industry, 2022–2023 [verify] | Reducing time-to-mitigate for cloud outages | LLM-recommended mitigation actions from incident history | ❌ No — post-incident | ❌ No | ❌ No | Partially | Post-incident mitigation; no pre-deployment readiness assessment |

---

## 5. LLM Hallucination and Evidence Grounding in SE

| Paper/Source | Venue/Year | Problem | Method | Handles prod-readiness evidence? | Measures false-ready? | Requires evidence citations? | Evaluates LLM readiness? | Gap relative to RelGate |
|---|---|---|---|---|---|---|---|---|
| Ji et al., "Survey of Hallucination in Natural Language Generation" | ACM Computing Surveys, 2023 | Taxonomizing hallucination in NLG systems | Comprehensive survey: intrinsic vs. extrinsic hallucination, detection methods, mitigation strategies | ❌ No — general NLG focus | ❌ No | ❌ No — surveys the problem, does not enforce citations | ❌ No | Provides theoretical framework for hallucination but does not study hallucination in SE/readiness contexts |
| Nogueira et al., "Beyond Functional Correctness: Empirical Evaluation of LLMs for Text-to-Code" [verify exact title] | ISSRE, 2025 | Evaluating LLM-generated code beyond pass/fail correctness | Empirical study measuring reliability, robustness, and non-functional properties of LLM code | ❌ No | ❌ No — measures code quality, not approval decisions | ❌ No | Partially — evaluates LLM output reliability | Evaluates LLM reliability for code generation, not for readiness decision-making |
| Liu et al., "Enhancing Reliability Assurance for DNN against Numerical Defect with LLMs" [verify exact title] | ISSRE, 2025 | Detecting numerical defects in DNNs using LLMs | LLM-assisted defect detection for deep learning reliability | ❌ No | ❌ No | ❌ No | Partially — LLM as reliability tool | Applies LLMs to DNN testing, not to production-readiness review of cloud changes |

---

## 6. Reliability Gates, Quality Gates, CI/CD Gates

| Paper/Source | Venue/Year | Problem | Method | Handles prod-readiness evidence? | Measures false-ready? | Requires evidence citations? | Evaluates LLM readiness? | Gap relative to RelGate |
|---|---|---|---|---|---|---|---|---|
| Fitzgerald & Stol, "Continuous Software Engineering: A Roadmap and Agenda" | JSS, 2017 | Defining continuous practices (CI/CD/CD) and research gaps | Roadmap covering continuous integration, delivery, deployment, and quality assurance | Partially — discusses quality gates in CI/CD | ❌ No | ❌ No | ❌ No | Defines quality gates conceptually but pre-dates LLM era; no automated readiness assessment |
| Humble & Farley, *Continuous Delivery* | Addison-Wesley, 2010 | Reliable, repeatable software delivery | Deployment pipelines with automated gates (test, staging, production) | Partially — gate concept | ❌ No | ❌ No — gates are binary pass/fail on tests | ❌ No | Gates are test-based; no semantic readiness reasoning or evidence validation |
| Schermann et al., "Continuous Experimentation and Progressive Delivery" [verify exact title] | ICSE-SEIP / ESE, 2018 [verify] | Reducing deployment risk through progressive rollout | Feature flags, canary deployments, progressive delivery patterns | Partially — risk reduction | ❌ No | ❌ No | ❌ No | Progressive delivery reduces blast radius but does not assess readiness evidence completeness |

---

## 7. Safety/Reliability of AI-Powered Software Systems

| Paper/Source | Venue/Year | Problem | Method | Handles prod-readiness evidence? | Measures false-ready? | Requires evidence citations? | Evaluates LLM readiness? | Gap relative to RelGate |
|---|---|---|---|---|---|---|---|---|
| Pei et al., various AIOps works (root cause analysis, microservice reliability) | ICSE/FSE/ASE, 2020–2024 [verify specific papers] | Automated operations for cloud-native systems | ML/DL-based anomaly detection, root cause localization, microservice dependency analysis | ❌ No — runtime operations | ❌ No | ❌ No | ❌ No | AIOps for runtime; does not address pre-deployment readiness gating |
| Poenaru-Olaru et al., "Prepared for the Unknown: Adapting AIOps Capacity Forecasting Models" | ISSRE, 2025 | Adapting capacity forecasting models to unseen workload patterns | Transfer learning / adaptation techniques for AIOps capacity models | ❌ No — capacity forecasting | ❌ No | ❌ No | ❌ No | Capacity forecasting is one input to readiness but not a holistic readiness gate |

---

## 8. Cloud Reliability / DevOps / Deployment Risk

| Paper/Source | Venue/Year | Problem | Method | Handles prod-readiness evidence? | Measures false-ready? | Requires evidence citations? | Evaluates LLM readiness? | Gap relative to RelGate |
|---|---|---|---|---|---|---|---|---|
| Nie et al., "DeST: Unsupervised Decoupled Spatio-Temporal Framework for Microservice Incident Management" | ISSRE, 2025 | Detecting and localizing incidents in microservice architectures | Unsupervised spatio-temporal decoupling for incident detection | ❌ No — incident detection at runtime | ❌ No | ❌ No | ❌ No | Runtime incident detection; does not prevent incidents via pre-deployment review |
| Zhang et al., "Integrating GraphSAGE and Mamba for Fault Detection in Microservice Systems" | ISSRE, 2025 | Fault detection in microservice dependency graphs | Graph neural networks (GraphSAGE) + Mamba architecture for fault detection | ❌ No — runtime fault detection | ❌ No | ❌ No | ❌ No | Detects faults post-deployment; does not assess whether a change should have been deployed |

---

## Summary Gap Analysis

### Key Observations

1. **Production Readiness Reviews exist but are manual and unscalable.** Google's PRR (SRE Book, 2016; USENIX ;login:) and launch checklists define *what* to check but rely entirely on human reviewers. No automation, no LLM assistance, no measurement of decision accuracy.

2. **LLM-based code review is advancing but stays at the code level.** CodeReviewer (Li et al., FSE 2022) and MoE approaches (Tang et al., ISSRE 2025) automate code-level feedback but do not reason about operational readiness evidence (monitoring dashboards, load test results, rollback plans, capacity analysis).

3. **AIOps/LLM research focuses on post-incident, not pre-deployment.** ICSE 2023 (Ahmed et al.), ISSRE 2025 (Cui et al.; Nie et al.; Zhang et al.) all address incident detection, root cause analysis, or mitigation *after* failures occur. The pre-deployment prevention gap remains unstudied.

4. **Hallucination research is general-purpose.** Ji et al. (ACM CS 2023) survey hallucination broadly. Nogueira et al. (ISSRE 2025) evaluate LLM code reliability. Neither studies hallucinated *readiness evidence* — i.e., an LLM fabricating claims about monitoring coverage or load test results.

5. **No existing work measures false-ready rates.** None of the surveyed papers define or measure the rate at which automated systems incorrectly approve changes that lack mandatory production-readiness evidence.

---

## Gap Paragraph

Existing LLM-based review tools can produce useful natural-language feedback (Tang et al., ISSRE 2025; Li et al., FSE 2022), and SRE checklists can guide production readiness (Google SRE Book; USENIX PRR). However, there is limited empirical evidence on whether LLMs hallucinate readiness evidence or falsely approve cloud changes when mandatory reliability evidence is absent. AIOps research at ISSRE 2025 addresses incident detection and root cause analysis (Cui et al.; Zhang et al.; Nie et al.) but not pre-deployment readiness review. RelGate studies this specific failure mode — false-ready decisions caused by missing or hallucinated evidence — and proposes evidence-grounded readiness gates as a measurable mitigation.

---

## Positioning Statement

RelGate occupies a unique intersection:
- **Unlike PRRs:** Automated, LLM-assisted, measurable
- **Unlike LLM code review:** Operates on operational readiness evidence, not code diffs
- **Unlike AIOps:** Pre-deployment prevention, not post-incident detection
- **Unlike general hallucination studies:** Domain-specific (production readiness), task-specific (gate decisions), metric-specific (false-ready rate)

---

*[verify] markers indicate citation details that should be confirmed against original sources before submission.*
