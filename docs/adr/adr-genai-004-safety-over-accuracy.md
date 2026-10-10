---
layout: page
title: "ADR-GENAI-004: Safety Metrics Outweigh Accuracy"
permalink: /adr/genai-004-safety-over-accuracy/
---

This page is non-normative and records an architectural decision.

# ADR-GENAI-004: Safety Metrics Outweigh Accuracy

**Status:** Accepted  
**Date:** 2026-05  
**Context:** GenAI/LLM Testing Architecture

---

## Context

Evaluation pipelines for LLM systems produce multiple types of metrics: quality/accuracy metrics (how correct or helpful is the output?) and safety metrics (does the output violate safety policies?).

In some cases, these metrics conflict. A model may produce highly accurate, relevant responses that also contain harmful, biased, or policy-violating content. Without a clear decision rule, these conflicts create ambiguity in the quality gate decision.

---

## Decision

Safety metrics are **first-class gate conditions** and take precedence over accuracy or quality metrics in all deployment decisions.

Specifically:
- A safety violation **always blocks deployment**, regardless of accuracy score
- There is no trade-off calculation between safety and accuracy at the quality gate
- Safety thresholds are non-negotiable and cannot be overridden by accuracy improvements

---

## Rationale

| Reason | Detail |
|---|---|
| Safety failures cause direct harm | A high-accuracy but unsafe output can harm users, expose the organization to liability, and violate regulatory requirements |
| Accuracy improvements do not offset safety failures | A 5% accuracy gain does not justify a 1% increase in harmful outputs |
| Trust requires consistent safety guarantees | Users and regulators require predictable safety behavior, not probabilistic averages |
| Implicit safety gating creates false confidence | Treating safety as a sub-dimension of accuracy allows unsafe outputs to pass gates |

Safety is not a dimension of quality—it is a precondition for deployment.

---

## Consequences

- The **Safety Evaluation Engine** is a blocking gate, independent of the evaluation pipeline's accuracy scoring.
- Quality gate configuration must place safety checks **before** accuracy checks in the enforcement order.
- Safety metrics are reported separately from accuracy metrics in all evaluation artifacts.
- Teams cannot "accept risk" on safety violations at the gate level—escalation to human review is required, not a bypass.

---

## Risk Mitigated

- R-01: Model output is harmful or toxic
- R-07: Borderline safety case auto-approved without human review

## Capability Enabled

- Safety Evaluation
- Policy Enforcement

## Constraint Enforced

- Safety violations always block deployment
- Human review required for safety-critical domains

---

## Related ADRs

- [ADR-GENAI-002: Human Judgment Required](./adr-genai-002-human-judgment-required.md)
- [ADR-GENAI-001: BLEU/ROUGE Insufficient](./adr-genai-001-bleu-rouge-insufficient.md)
