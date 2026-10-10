---
layout: page
title: "ADR-GENAI-005: Regression Is Semantic, Not Textual"
permalink: /adr/genai-005-semantic-regression/
---

This page is non-normative and records an architectural decision.

# ADR-GENAI-005: Regression Is Semantic, Not Textual

**Status:** Accepted  
**Date:** 2026-05  
**Context:** GenAI/LLM Testing Architecture

---

## Context

In classical software testing, regression detection compares outputs precisely: either the output matches the expected value or it does not. This works because classical systems are deterministic.

LLM outputs are non-deterministic and paraphrastic. The same semantically correct response may be expressed with entirely different wording across runs, model versions, or temperature settings. Conversely, a response with high textual similarity to a reference may be semantically incorrect or subtly different in meaning.

Applying textual diff-based regression detection to LLM outputs produces high false-positive rates (flagging correct paraphrases as regressions) and misses genuine semantic regressions (accepting textually similar but semantically different outputs).

---

## Decision

Regression detection for LLM systems **must** be based on **semantic comparison**, not textual comparison.

Semantic regression is defined as a statistically significant change in:
- Meaning or intent of outputs across a golden dataset
- Capability-level behavior (e.g., instruction-following rate, factual accuracy category)
- Safety classification distribution

Textual similarity metrics (BLEU, ROUGE, exact match) may be computed but **must not** be the primary regression signal.

---

## Rationale

| Textual Regression Problem | Impact |
|---|---|
| LLMs paraphrase correct answers | Correct responses flagged as regressions, creating noise |
| Textual similarity does not detect meaning change | Semantically degraded outputs pass regression checks |
| Model updates change style without changing correctness | False regression signals block valid improvements |
| Prompt changes alter surface form, not intent | Textual diff detects prompt engineering as regression |

Semantic regression detection requires:
- Embedding-based similarity or semantic scoring
- Capability-level behavioral metrics tracked over time
- Statistical comparison against frozen baselines

---

## Consequences

- The **Regression Analysis Engine** must compute semantic similarity metrics, not textual diff.
- Baselines are defined as **behavioral distributions** over golden datasets, not as specific text outputs.
- Regression thresholds are statistical (e.g., mean semantic similarity drops below X over the evaluation set), not binary.
- Teams must invest in maintaining semantically meaningful golden datasets—not just reference text strings.
- Textual metrics remain available as supplementary signals but are not gating criteria.

---

## Risk Mitigated

- R-08: Textual regression check misses semantic change
- R-02: Quality silently regresses after model update

## Capability Enabled

- Regression Detection
- Output Evaluation
- Consistency Analysis

## Constraint Enforced

- Baselines are frozen per release
- Regression is semantic, not textual

---

## Related ADRs

- [ADR-GENAI-001: BLEU/ROUGE Insufficient](./adr-genai-001-bleu-rouge-insufficient.md)
- [ADR-GENAI-003: Temperature Fixed in CI](./adr-genai-003-temperature-fixed-in-ci.md)
