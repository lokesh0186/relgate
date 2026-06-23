# ISSRE 2026 Fast Abstracts / Project Highlights — Venue Fit Analysis

**Paper:** RelGate: A Lightweight LLM-Assisted Production-Readiness Gate for Cloud Changes  
**Target Track:** Fast Abstracts / Project Highlights (FA/PH)  
**Research Date:** 2026-06-22  
**Source:** https://cyprusconferences.org/issre2026/fast-abstract-track/

---

## 1. Conference Overview

| Field | Detail |
|-------|--------|
| Conference | 37th IEEE International Symposium on Software Reliability Engineering (ISSRE 2026) |
| Dates | October 20–23, 2026 |
| Location | St. Raphael Resort, Limassol, Cyprus |
| Track | Fast Abstracts / Project Highlights |
| Publication | Supplemental Proceedings of ISSRE 2026 via **IEEE Xplore** |

### Keynote Speakers (Relevance Indicators)
- **Don Syme (GitHub):** "The Agentic Repository Automation Revolution" — *directly relevant; RelGate is an agentic pre-deployment gate*
- **Paolo Tonella:** "AI Testing" — *relevant; RelGate evaluates LLM reliability in safety-critical decisions*
- **Laurie Williams:** "Software Supply Chain Security" — *tangentially relevant; pre-deployment gates are supply-chain safety mechanisms*

---

## 2. Submission Requirements

| Requirement | Specification |
|-------------|---------------|
| **Deadline** | **June 25, 2026 (AoE)** ← extended from June 15 |
| Notification | August 05, 2026 |
| Camera-Ready | August 19, 2026 |
| Format | IEEE Computer Society Format |
| Length | **2 pages** (strict) |
| Submission System | EasyChair — single PDF, all fonts embedded |
| Language | English |
| Anonymization | **Not required** — author names should be included |
| Originality | Must not be previously published or under submission elsewhere |
| Plagiarism Check | IEEE Cross Check |
| Presentation | Short talk or poster (assigned upon notification) |
| Contact | issre2026-fast-abstracts@easychair.org |

### Timeline Status (as of 2026-06-22)
⚠️ **3 days remaining** until submission deadline (June 25 AoE).

---

## 3. Track Scope & Aims

FA/PH papers are **two-page, lightly reviewed** technical articles. The track explicitly welcomes:

### Fast Abstracts
- Early original ideas
- Work-in-progress and ongoing experiences
- Challenges to the SRE status quo
- Critical analyses of prior work
- Lessons from real-world SRE applications
- New problems from industrial or academic experience
- Approaches to significant problems **without complete results**

### Project Highlights
- Overviews of funded research projects and objectives
- Project methodologies, architectures, and experimental frameworks
- Early or intermediate results, lessons learned, preliminary insights
- Datasets, benchmarks, tools, platforms released or in progress
- Collaboration experiences, challenges, emerging directions

---

## 4. Topics of Interest (Verbatim from CFP)

1. Reliability, safety, maintainability, security, survivability, resilience, robustness, and other dependability attributes
2. Faults (defects, bugs, etc.), errors, failures, and other dependability threats
3. Reliability of all systems, applications, networks, and software
4. Metrics, measurement, assessment, monitoring, modeling, estimation, prediction
5. **Reliability of AI-powered software systems, including LLMs, autonomous agents, AI-enabled applications**
6. Other contents about software reliability: normative/regulatory/ethical spaces, societal aspects

### RelGate Topic Mapping

| CFP Topic | RelGate Alignment |
|-----------|-------------------|
| Reliability, resilience, robustness | Pre-deployment gates prevent reliability regressions |
| Faults, errors, failures, dependability threats | False-ready decisions as dependability threats; evidence hallucination as a fault class |
| Metrics, measurement, assessment, prediction | Gate pass/fail metrics, evidence-grounding scores, hallucination rates |
| **Reliability of AI-powered systems, LLMs, agents** | **Primary fit** — evaluating LLM reliability as a production-readiness reviewer |
| Normative/regulatory/ethical spaces | Responsible AI deployment; human-in-the-loop gate design |

---

## 5. ISSRE 2025 Acceptance Patterns

### Research Sessions (Relevant Precedents)

| Session | Papers | Relevance to RelGate |
|---------|--------|---------------------|
| RS2: LLMs for Logs and Chatbots | CSLParser, AetherLog (LLM+KG root cause) | LLMs applied to operational reliability tasks |
| RS6: AI for Software Engineering | Code Review with MoE LLMs, Human vs AI code defects | **Direct precedent** — LLM-assisted code review |
| RS7: Large Language Models | AUVANA, Enhancing DNN Reliability with LLMs, ASASQL | LLM reliability and LLMs-for-reliability both accepted |
| RS8: Microservices and Cloud | GraphSAGE fault detection, DeST incident management, ClusterRCA, Production Incidents in Generative AI Cloud Services | Cloud production systems, AIOps |
| RS9: Performance and Reliability | AIOps Capacity Forecasting | Predictive reliability, production realism |

### Fast Abstracts 2025 (Accepted Examples)
- Bug Whispering: Towards Audio Bug Reporting
- Automated Extraction of Quality Concerns From Mobile App Reviews Using Deep Learning
- Impacts of RBB Topology on Blockchain Scalability
- Redundant Self-Adaptive Quantum Software Architecture towards Reliable Quantum Computing

**Observation:** FA/PH accepts diverse, early-stage ideas with modest empirical backing. RelGate's pilot (108 calls across 12 cases × 3 modes × 3 models) exceeds the empirical depth of most accepted fast abstracts.

---

## 6. What ISSRE Values (Derived from Program Analysis)

1. **Reliability/dependability as the central concern** — not a side benefit
2. **Empirical evidence and measurement** — numbers over narratives
3. **Production realism** — real systems, real incidents, real deployments
4. **Clear failure models and dependability threats** — named failure modes
5. **Tools/artifacts that enable reproduction** — open benchmarks, scripts
6. **Honest limitations and threats to validity** — not overselling
7. **Actionable insights for practitioners** — industry applicability
8. **Cloud/microservice/AIOps relevance** — strong in 2025 program
9. **LLM reliability and LLMs for reliability** — explicitly in scope for 2026

---

## 7. RelGate Fit Assessment

### Recommended Track: **Project Highlight (PH)**

RelGate qualifies as a Project Highlight because it satisfies each PH criterion:

| PH Criterion | RelGate Evidence |
|--------------|-----------------|
| Project methodology | Evidence-grounded reliability gates with structured prompting |
| Architecture/experimental framework | 3 modes (zero-shot, checklist-primed, evidence-grounded) × 3 models |
| Early/intermediate results | Pilot with 12 synthetic change bundles → 108 LLM calls |
| Datasets, benchmarks, tools | Benchmark cases, prompt templates, scoring scripts (to be released) |
| Emerging directions | False-ready detection, evidence hallucination as a reliability threat |

### Primary Fit Dimensions

1. **Reliability of AI-powered systems (Topic 5):** RelGate directly measures whether LLMs produce reliable production-readiness decisions — treating the LLM reviewer itself as a system whose dependability must be assessed.

2. **Faults and dependability threats (Topic 2):** Introduces two novel threat classes:
   - **False-ready decisions:** LLM approves a change that would cause production failures
   - **Evidence hallucination:** LLM fabricates justifications for its gate verdict

3. **Metrics and measurement (Topic 4):** Gate pass/fail accuracy, evidence-grounding rate, hallucination frequency, mode comparison.

4. **Keynote alignment:** Don Syme's keynote on "The Agentic Repository Automation Revolution" positions RelGate as a timely contribution — it addresses reliability concerns in exactly this agentic automation space.

### Differentiation from ISSRE 2025 Papers

| ISSRE 2025 Paper | RelGate Distinction |
|------------------|---------------------|
| Code Review with MoE LLMs | RelGate targets **production-readiness** (operational risk), not code quality |
| DeST incident management | RelGate is **pre-deployment** (prevention), not post-incident (reaction) |
| Production Incidents in GenAI Cloud | RelGate is a **tool/gate**, not an observational study |
| AIOps Capacity Forecasting | RelGate addresses **change safety**, not capacity |

---

## 8. Paper Structure Recommendations (2-Page Constraint)

### Patterns to Emulate (from successful ISSRE papers)

1. **Problem first:** Open with a concrete motivating failure scenario (a false-ready decision that would have caused production impact)
2. **One architecture figure:** Change bundle → gate modes → evidence check → decision
3. **Small but clean pilot:** 12 cases × 3 modes × 3 models = 108 calls (sufficient for a PH)
4. **One compact results table:** Mode × metric comparison
5. **Honest limitations paragraph:** Synthetic cases, single-domain pilot, prompt sensitivity
6. **Clear "why ISSRE should care" framing:** LLM reliability in safety-critical automation decisions

### Suggested Section Layout

| Section | ~Words | Content |
|---------|--------|---------|
| Title + Authors | — | Include names (not anonymized) |
| Abstract | 100 | Problem, approach, key finding |
| 1. Motivation | 200 | False-ready scenario, gap in pre-deployment review |
| 2. Approach | 300 | Three modes, evidence grounding, architecture figure |
| 3. Pilot Results | 250 | Table: accuracy, hallucination rate by mode × model |
| 4. Discussion & Limitations | 150 | Threats to validity, future work |
| References | — | ~8–10 refs (IEEE format) |

---

## 9. Competitive Positioning

### Strengths for ISSRE Reviewers
- ✅ Directly addresses a 2026 CFP topic (reliability of LLMs/agents)
- ✅ Aligns with keynote theme (agentic automation)
- ✅ Production-realistic framing (cloud change bundles)
- ✅ Quantitative pilot results (not just an idea)
- ✅ Introduces named failure modes (false-ready, evidence hallucination)
- ✅ Promises artifact release (benchmark, prompts, scripts)
- ✅ Industry-relevant (DevOps/SRE practitioners)

### Risks to Mitigate
- ⚠️ Synthetic cases only → acknowledge, frame as "controlled pilot before production deployment"
- ⚠️ Small scale (12 cases) → emphasize this is a PH, not a full research paper; 108 total calls provides statistical signal
- ⚠️ Prompt sensitivity → report it honestly as a finding, not hide it
- ⚠️ No production deployment yet → frame as "readiness for deployment" with concrete next steps

---

## 10. Action Items for Submission

- [ ] Finalize 2-page PDF in IEEE Computer Society format
- [ ] Ensure all fonts are embedded in PDF
- [ ] Include author names and affiliations (no anonymization needed)
- [ ] Submit via EasyChair by **June 25, 2026 AoE**
- [ ] Verify no overlap with any concurrent submission
- [ ] Prepare both short-talk slides and poster (presentation format TBD upon notification)

---

## 11. Key Dates Summary

```
TODAY:          2026-06-22  ← 3 days to deadline
DEADLINE:       2026-06-25 (AoE)
NOTIFICATION:   2026-08-05
CAMERA-READY:   2026-08-19
CONFERENCE:     2026-10-20 to 2026-10-23 (Limassol, Cyprus)
```

---

*Last updated: 2026-06-22*
