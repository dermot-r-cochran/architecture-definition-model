---
layout: page
title: "ADR-002: Model Evaluation Blocks Deployment"
permalink: /adr/ADR-002-model-evaluation-blocks-deployment/
---

This page is non-normative and records an architectural decision.

# ADR-002: Model Evaluation Blocks Deployment

## Status

Accepted

---

## Context

For ML systems, model behavior is not fully captured by unit or integration tests. Accuracy, bias, drift, and safety properties can regress without any change to application code. If model evaluation is treated as advisory rather than blocking, safety and compliance regressions can reach production.

The ADM places safety metrics as first-class architectural elements, not annotations. Quality gates must reflect this.

---

## Decision

Model evaluation results are a required quality gate.  
A deployment is blocked if the evaluation engine returns a failing report.  
Evaluation thresholds are governed artifacts—changes to thresholds require an ADR or equivalent documented decision.

---

## Consequences

- The deployment pipeline has a mandatory evaluation stage for every model change.
- Evaluation datasets must be versioned and immutable to ensure gate reproducibility.
- Evaluation threshold configuration is treated as a governed artifact, not an operational setting.
- Release velocity for model changes is bounded by evaluation time; this is accepted as a necessary constraint.

---

## Linked ADM Elements

**Capabilities:**
- (ML) Evaluation — measures accuracy, bias, drift, and safety
- Quality Gates — enforces pass/fail decisions; blocks deployment on failure

**Constraints:**
- Safety metrics are first-class (not annotations)
- Evaluation datasets are versioned and immutable
- Test results must be auditable and retained

**Risks addressed:**
- Model safety or compliance regressions reaching production undetected
- Evaluation treated as a post-deployment diagnostic rather than a pre-deployment gate
- Threshold changes made informally without governance trail

---

## Related Documents

- [ADR Index](index.md)
- [Testing Architecture — Capabilities](../testing/testing-architecture.md#3-capabilities)
- [Testing Architecture — Constraints](../testing/testing-architecture.md#9-constraints)
- [Traceability Matrix](../testing/traceability-matrix.md)
