---
layout: page
title: "ADR-GENAI-001: BLEU/ROUGE Are Insufficient Alone"
permalink: /adr/genai-001-bleu-rouge-insufficient/
---

This page is non-normative and records an architectural decision.

# ADR-GENAI-001: BLEU/ROUGE Are Insufficient Alone

**Status:** Accepted  
**Date:** 2026-05  
**Context:** GenAI/LLM Testing Architecture

---

## Context

BLEU (Bilingual Evaluation Understudy) and ROUGE (Recall-Oriented Understudy for Gisting Evaluation) are widely used automated metrics for evaluating text generation. They measure n-gram overlap between a generated output and one or more reference texts.

When building automated evaluation pipelines for LLM-powered systems, teams often default to BLEU/ROUGE because they are fast, cheap, and fully automatable.

---

## Decision

BLEU and ROUGE **must not** be used as the sole quality metrics for LLM output evaluation.

They may be used as **supplementary signals** within a broader evaluation portfolio, but cannot serve as the primary quality gate for production deployment decisions.

---

## Rationale

| Problem | Consequence |
|---|---|
| BLEU/ROUGE measure lexical overlap, not semantic correctness | A paraphrase that is semantically identical to the reference scores poorly |
| Reference texts are often incomplete or single-authored | High overlap with one reference does not imply correctness |
| Metrics do not penalize harmful or unsafe content | A toxic response that closely mirrors a reference text scores well |
| LLM outputs are inherently paraphrastic | The same correct answer rarely uses the exact same tokens as a reference |

---

## Consequences

- Evaluation pipelines must include at least one **semantic similarity** measure (e.g., embedding-based) in addition to lexical metrics.
- Safety evaluation is always a separate, first-class gate—not a sub-metric of BLEU/ROUGE.
- Human review is required for cases where automated metrics are ambiguous (see [ADR-GENAI-002](./adr-genai-002-human-judgment-required.md)).

---

## Risk Mitigated

- R-02: Quality silently regresses after model update
- R-08: Textual regression check misses semantic change

## Capability Enabled

- Output Evaluation
- Regression Detection

## Constraint Enforced

- Baselines are frozen per release
- Regression is semantic, not textual

---

## Related ADRs

- [ADR-GENAI-002: Human Judgment Required](./adr-genai-002-human-judgment-required.md)
- [ADR-GENAI-005: Semantic Regression](./adr-genai-005-semantic-regression.md)
