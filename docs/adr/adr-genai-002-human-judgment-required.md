---
layout: page
title: "ADR-GENAI-002: Human Judgment Is Required for Quality"
permalink: /adr/genai-002-human-judgment-required/
---

This page is non-normative and records an architectural decision.

# ADR-GENAI-002: Human Judgment Is Required for Quality

**Status:** Accepted  
**Date:** 2026-05  
**Context:** GenAI/LLM Testing Architecture

---

## Context

Automated metrics (including BLEU/ROUGE, semantic similarity scores, and classifier-based safety checks) are necessary but not sufficient for governing LLM output quality in safety-critical or high-stakes domains.

There are classes of LLM outputs where automated evaluation cannot reliably distinguish between acceptable and unacceptable responses—particularly in cases involving nuance, implicit harm, regulatory interpretation, or domain-specific correctness.

---

## Decision

Human judgment **must** be incorporated into the evaluation pipeline for:

1. Safety-critical domains (medical, legal, financial, regulatory)
2. Low-confidence automated evaluation results (below defined threshold)
3. Novel output patterns not covered by existing golden datasets
4. Any output flagged by the Safety Evaluation Engine for escalation

Human review decisions must be **captured as structured data** and retained as audit artifacts.

---

## Rationale

| Reason | Detail |
|---|---|
| Automated metrics have known blind spots | No metric reliably detects subtle harm, regulatory non-compliance, or contextually incorrect but plausible-sounding output |
| LLM behavior is emergent | New failure modes appear that were not anticipated during metric design |
| Accountability requires a human decision point | In regulated domains, a human must be in the approval chain |
| Structured human feedback improves future evaluation | Captured judgments become training signal for better automated evaluation |

---

## Consequences

- The **Human Review Coordinator** execution unit is a required architectural component, not optional.
- Human review throughput is a **constraint on deployment velocity**—pipelines must account for review time.
- Human review records are retained per release and through audit periods.
- The architecture must provide a structured interface for capturing reviewer decisions (not free-text comments).

---

## Risk Mitigated

- R-07: Borderline safety case auto-approved without human review
- R-01: Model output is harmful or toxic

## Capability Enabled

- Human‑in‑the‑Loop Review
- Safety Evaluation

## Constraint Enforced

- Human review required for safety-critical domains and low-confidence metrics

---

## Related ADRs

- [ADR-GENAI-001: BLEU/ROUGE Insufficient](./adr-genai-001-bleu-rouge-insufficient.md)
- [ADR-GENAI-004: Safety Over Accuracy](./adr-genai-004-safety-over-accuracy.md)
