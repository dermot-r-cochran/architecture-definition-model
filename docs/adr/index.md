---
layout: page
title: Architecture Decision Records (ADR)
permalink: /adr/
---

This page is non-normative and indexes recorded architectural decisions.

# Architecture Decision Records (ADR)

ADRs document deliberate trade-off decisions that reference ADM elements. They explain **why** an architectural choice was made, not **what** was built.

Each ADR references the ADM layers it relates to: the risk mitigated, the capability enabled, and the constraint enforced.

---

## GenAI/LLM Testing ADRs

These ADRs govern the GenAI/LLM Testing Architecture extension.

| ADR | Title | Status |
|---|---|---|
| [ADR-GENAI-001](./adr-genai-001-bleu-rouge-insufficient.md) | BLEU/ROUGE Are Insufficient Alone | Accepted |
| [ADR-GENAI-002](./adr-genai-002-human-judgment-required.md) | Human Judgment Is Required for Quality | Accepted |
| [ADR-GENAI-003](./adr-genai-003-temperature-fixed-in-ci.md) | Temperature Is Fixed During CI | Accepted |
| [ADR-GENAI-004](./adr-genai-004-safety-over-accuracy.md) | Safety Metrics Outweigh Accuracy | Accepted |
| [ADR-GENAI-005](./adr-genai-005-semantic-regression.md) | Regression Is Semantic, Not Textual | Accepted |

## Testing Architecture ADRs

This index lists all recorded architectural decisions for the testing architecture.  
Each ADR documents a deliberate trade-off, links it to ADM capabilities and constraints, and identifies the risks it addresses.

---

## Index

| ID | Title | Status | Capabilities | Constraints |
|---|---|---|---|---|
| [ADR-001](ADR-001-contract-tests-over-e2e.md) | Contract tests favored over E2E in CI | Accepted | Test Execution, Quality Gates | Feedback time is bounded |
| [ADR-002](ADR-002-model-evaluation-blocks-deployment.md) | Model evaluation blocks deployment | Accepted | (ML) Evaluation, Quality Gates | Safety metrics are first-class |
| [ADR-003](ADR-003-flaky-tests-fail-pipeline.md) | Flaky tests fail the pipeline instead of retrying | Accepted | Quality Gates, Regression Detection | Tests must be deterministic |
| [ADR-004](ADR-004-synthetic-data-lower-environments.md) | Synthetic data used in lower environments | Accepted | Data Management | Environments are ephemeral and reproducible |

---

## ADR Template

New ADRs should follow this structure:

```
# ADR-NNN: [Short title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-NNN]

## Context
[Why this decision was needed]

## Decision
[What was decided]

## Consequences
[What changes; what trade-offs are accepted]

## Linked ADM Elements
- Capabilities: [list]
- Constraints: [list]
- Risks addressed: [list]
```

---

## Related Documents

- [GenAI/LLM Testing Architecture](../testing/genai-llm-testing-architecture.md)
- [GenAI Traceability Matrix](../testing/genai-traceability-matrix.md)
- [Testing Architecture](../testing/testing-architecture.md)
- [Traceability Matrix](../testing/traceability-matrix.md)
