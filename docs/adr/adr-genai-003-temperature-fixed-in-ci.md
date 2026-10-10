---
layout: page
title: "ADR-GENAI-003: Temperature Is Fixed During CI"
permalink: /adr/genai-003-temperature-fixed-in-ci/
---

This page is non-normative and records an architectural decision.

# ADR-GENAI-003: Temperature Is Fixed During CI

**Status:** Accepted  
**Date:** 2026-05  
**Context:** GenAI/LLM Testing Architecture

---

## Context

LLM inference includes a **temperature** parameter that controls the randomness of token sampling. Higher temperatures produce more varied outputs; lower temperatures (approaching zero) produce more deterministic outputs.

In development and production, variable temperature is often desirable for creative or open-ended tasks. However, in automated CI/CD evaluation pipelines, uncontrolled temperature introduces non-determinism that makes evaluation results unreliable and non-reproducible.

---

## Decision

During CI/CD evaluation, temperature and all other sampling parameters (top-p, top-k, seed) **must be explicitly set to fixed, documented values**.

The fixed values are:
- Documented in the evaluation configuration
- Version-controlled alongside prompt and dataset definitions
- Applied consistently across all evaluation runs for a given baseline

---

## Rationale

| Problem with variable temperature in CI | Consequence |
|---|---|
| Same prompt produces different outputs across runs | Evaluation results are not reproducible |
| Variance in outputs is attributed to quality change | False positive regressions or false negative passes |
| Non-determinism obscures real behavioral changes | Genuine model drift is hidden by sampling noise |
| Audit trail is incomplete | Cannot replay a CI run with identical model outputs |

Fixing temperature does not mean setting it to zero (which may not be appropriate for all models). It means the value is **explicit, controlled, and identical across all comparable runs**.

---

## Consequences

- The **Prompt Evaluation Runner** must expose temperature and sampling configuration as versioned, explicit parameters.
- CI evaluation results are reproducible given the same model version, prompt, dataset, and sampling config.
- This constraint applies to **evaluation runs only**; production inference may use different temperature settings.
- Consistency Analysis capability uses fixed-temperature runs as the baseline for measuring production variance.

---

## Risk Mitigated

- R-05: Output variance misinterpreted as quality improvement
- R-04: Evaluation not reproducible due to dataset mutation (adjacent: configuration mutation)

## Capability Enabled

- Consistency Analysis
- Output Evaluation
- Regression Detection

## Constraint Enforced

- Non-determinism must be measured, not ignored
- All randomness is explicitly configured

---

## Related ADRs

- [ADR-GENAI-001: BLEU/ROUGE Insufficient](./adr-genai-001-bleu-rouge-insufficient.md)
- [ADR-GENAI-005: Semantic Regression](./adr-genai-005-semantic-regression.md)
