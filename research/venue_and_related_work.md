# RelGate Venue And Related-Work Notes

Date checked: 2026-06-16.

## Venue Facts: ISSRE 2026 FA/PH

Official page: https://cyprusconferences.org/issre2026/fast-abstract-track/

Verified facts:

- Fast Abstract / Project Highlight papers are two-page, lightly reviewed technical articles.
- The track accepts early ideas, work-in-progress, lessons learned, tools, datasets, benchmarks, architectures, and experimental frameworks.
- Project Highlights may report methodologies, architectures, experimental frameworks, tools, datasets, and early/intermediate results.
- Accepted contributions will appear in the ISSRE 2026 Supplemental Proceedings and IEEE Xplore.
- Submission deadline is June 25, 2026 AoE.
- Notification is August 05, 2026.
- Camera-ready deadline is August 19, 2026.
- Manuscripts must be submitted as PDF, in English, using IEEE Computer Society format.
- Manuscripts must not have been previously published or be under submission elsewhere.
- Presentation may be a short talk or poster.

Main ISSRE 2026 page: https://cyprusconferences.org/issre2026/

Conference facts:

- ISSRE 2026 is October 20-23, 2026.
- Location is Limassol, Cyprus.
- The conference says it will take place in all cases and may shift to hybrid or remote participation if conditions require.

## ISSRE Fit

RelGate fits ISSRE FA/PH as a software reliability project because it measures production-readiness review quality for cloud changes. The framing should emphasize:

- reliability process;
- evidence-grounded review;
- observability, alerting, rollout, rollback, ownership, and SLO/customer-impact readiness;
- false-ready decisions;
- evidence hallucination;
- preliminary pilot evidence.

Avoid writing this as a generic "LLMs for DevOps" idea.

## Accepted-Paper Pattern Notes

ISSRE 2025 research-program patterns suggest the venue rewards:

- empirical rigor;
- datasets and benchmark construction;
- reliability metrics;
- cloud/microservice/log/observability relevance;
- clear dependability threat or failure model;
- modest claims tied to measured evidence.

ISSRE 2025 research program: https://issre.github.io/2025/program_research.html

## Production-Readiness Foundations

Google SRE production-readiness framing:

- PRR identifies reliability needs of a service from its specific details.
- Relevant areas include system architecture, dependencies, instrumentation, monitoring, capacity planning, change management, and performance.
- Source: https://sre.google/sre-book/evolving-sre-engagement-model/

Google SRE workbook:

- Supports early engagement and continuous improvement for reliable services.
- Source: https://sre.google/workbook/engagement-model/

USENIX PRR article:

- Defines PRR as assessing services' operational capabilities and characteristics.
- Lists observability, reliability, scalability, security, disaster recovery, alerting, deployments, and production signals as common PRR areas.
- Source: https://www.usenix.org/publications/loginonline/production-readiness-reviews-surprisingly-versatile-practice

OpenTelemetry:

- Provides vendor-neutral telemetry concepts for traces, metrics, and logs.
- Source: https://opentelemetry.io/docs/

Prometheus:

- Alerting guidance emphasizes actionable symptom-based alerts.
- Alerting rules formalize conditions over metric expressions.
- Sources: https://prometheus.io/docs/practices/alerting/ and https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/

## Acceptance-Critical Framing

Strong two-page thesis:

> RelGate converts informal cloud-change readiness review into a structured, evidence-grounded gate. In a pilot over seeded cloud-change bundles, free-form LLM review may miss readiness gaps or hallucinate readiness evidence, while RelGate-style evidence grounding can be measured through false-ready, recall, hallucination, and actionability metrics.

Use actual pilot numbers only after live OpenRouter results.

