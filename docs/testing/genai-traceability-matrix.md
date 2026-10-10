---
layout: page
title: GenAI Traceability Matrix
permalink: /testing/genai-traceability-matrix/
---

This page is non-normative and provides a governance-oriented traceability matrix for GenAI/LLM testing.

# GenAI Traceability Matrix

> **Purpose:** Map each GenAI testing capability to the constraints it enforces, the risks it mitigates, and the evidence artifacts it produces. Use this matrix for governance reviews, audit readiness, and quality gate configuration.

---

## Matrix: Capabilities → Constraints → Risks → Evidence

| Capability | Enforced Constraint(s) | Risk Mitigated | Evidence / Artifact |
|---|---|---|---|
| **Prompt Validation** | No unreviewed prompt changes in production | Malformed or policy-violating prompts reaching the model | Prompt lint report; policy check log |
| **Output Evaluation** | Baselines frozen per release; datasets versioned and immutable | Silent quality regression; incorrect outputs deployed | Evaluation report (scored); golden dataset diff |
| **Safety Evaluation** | Safety violations always block deployment | Harmful, toxic, or policy-violating outputs released to users | Safety report; red-line threshold log; escalation record |
| **Consistency Analysis** | Non-determinism must be measured, not ignored | Unreported output variance masking real quality problems | Variance report; run-to-run comparison artifact |
| **Regression Detection** | Baselines frozen per release | Semantic drift from model updates going undetected | Regression comparison report (baseline vs candidate) |
| **Dataset Management** | Evaluation datasets are versioned and immutable | Evaluation results not reproducible; dataset contamination | Dataset version manifest; immutability audit log |
| **Cost Evaluation** | Cost overruns can block deployment | Unbounded token spend or latency degradation in production | Cost/performance report; threshold breach log |
| **Policy Enforcement** | Safety violations always block deployment; compliance thresholds enforced | Non-compliant outputs passing quality gates | Policy enforcement log; gate decision record |
| **Human‑in‑the‑Loop Review** | Human review required for safety-critical domains and low-confidence metrics | Ambiguous or borderline outputs incorrectly auto-approved | Human review record; structured reviewer decision artifact |

---

## Risk Register (GenAI‑Specific)

| Risk ID | Risk Description | Likelihood | Impact | Mitigating Capability |
|---|---|---|---|---|
| R-01 | Model output is harmful or toxic | Medium | Critical | Safety Evaluation |
| R-02 | Quality silently regresses after model update | High | High | Regression Detection, Output Evaluation |
| R-03 | Prompt change alters behavior without review | Medium | High | Prompt Validation |
| R-04 | Evaluation not reproducible due to dataset mutation | Low | High | Dataset Management |
| R-05 | Output variance misinterpreted as quality improvement | Medium | Medium | Consistency Analysis |
| R-06 | Cost overrun from unbounded token usage | Medium | Medium | Cost Evaluation |
| R-07 | Borderline safety case auto-approved without human review | Low | Critical | Human‑in‑the‑Loop Review |
| R-08 | Textual regression check misses semantic change | High | High | Regression Detection (semantic) |

---

## Constraint Traceability

| Constraint | Enforced By (Capability) | ADR Reference |
|---|---|---|
| Evaluation datasets are versioned and immutable | Dataset Management | — |
| Baselines are frozen per release | Output Evaluation, Regression Detection | — |
| Safety violations always block deployment | Safety Evaluation, Policy Enforcement | [ADR-GENAI-004](../adr/adr-genai-004-safety-over-accuracy.md) |
| Cost overruns can block deployment | Cost Evaluation | — |
| No unreviewed prompt changes in production | Prompt Validation | — |
| Human review required for safety-critical or low-confidence cases | Human‑in‑the‑Loop Review | [ADR-GENAI-002](../adr/adr-genai-002-human-judgment-required.md) |
| Non-determinism must be measured, not ignored | Consistency Analysis | [ADR-GENAI-003](../adr/adr-genai-003-temperature-fixed-in-ci.md) |
| Regression is semantic, not textual | Regression Detection | [ADR-GENAI-005](../adr/adr-genai-005-semantic-regression.md) |

---

## Evidence Artifact Reference

| Artifact | Produced By | Consumed By | Retention Requirement |
|---|---|---|---|
| Prompt lint report | Prompt Evaluation Runner | CI quality gate | Per release |
| Evaluation report (scored) | Model Evaluation Engine | Quality Gate Enforcer, human reviewers | Per release |
| Safety report | Safety Evaluation Engine | Quality Gate Enforcer, compliance reviewers | Per release + audit period |
| Regression comparison report | Regression Analysis Engine | Release managers | Per release |
| Dataset version manifest | Dataset Management | Evaluation audit | Permanent |
| Cost/performance report | Cost & Performance Analyzer | Release managers | Per release |
| Human review record | Human Review Coordinator | Compliance reviewers | Per release + audit period |

---

## Related Documents

- [GenAI/LLM Testing Architecture](./genai-llm-testing-architecture.md)
- [ADR-GENAI-001: BLEU/ROUGE Insufficient](../adr/adr-genai-001-bleu-rouge-insufficient.md)
- [ADR-GENAI-002: Human Judgment Required](../adr/adr-genai-002-human-judgment-required.md)
- [ADR-GENAI-003: Temperature Fixed in CI](../adr/adr-genai-003-temperature-fixed-in-ci.md)
- [ADR-GENAI-004: Safety Over Accuracy](../adr/adr-genai-004-safety-over-accuracy.md)
- [ADR-GENAI-005: Semantic Regression](../adr/adr-genai-005-semantic-regression.md)
