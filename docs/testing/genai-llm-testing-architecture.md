---
layout: page
title: GenAI/LLM Testing Architecture (ADM Extension)
permalink: /testing/genai-llm-testing-architecture/
---

This page is non-normative and provides an illustrative ADM-aligned architecture for GenAI/LLM testing.

# GenAI/LLM Testing Strategy and Automation Architecture (ADM Extension)

> **Scope:** This document extends the ADM testing architecture for systems that incorporate Large Language Models (LLMs) or other generative AI capabilities. It follows the same layer discipline as the canonical ADM.

---

## 1. Intent (GenAI‑specific)

Continuously establish justified confidence that LLM‑powered behavior is **correct enough**, **safe enough**, **aligned enough**, and **economical enough** for its intended use—despite non‑determinism and model evolution.

**Key shift from classical systems:**

| Classical Testing | GenAI Testing |
|---|---|
| Correctness is binary | Correctness is probabilistic |
| Behavior is deterministic | Behavior is emergent |
| Risk is functional | Risk includes semantic, ethical, and safety failure modes |

Testing exists to **bound and govern uncertainty**, not eliminate it.

---

## 2. Context (GenAI Realities)

### Actors

- Application developers
- Prompt engineers
- Model owners
- Safety/compliance reviewers
- CI/CD and release automation
- End users (implicit evaluators)

### External Systems

- Foundation model providers (API or self‑hosted)
- Vector databases
- Prompt/version stores
- Evaluation datasets
- Observability and cost tracking

### Environmental Realities

- Model behavior may change without code changes
- Outputs are stochastic
- Evaluation often requires judgment, not assertion

---

## 3. Capabilities (GenAI Testing Capabilities)

These capabilities are model‑agnostic and tool‑independent.

| Capability | Description |
|---|---|
| Prompt Validation | Verify prompts meet structure, policy, and intent |
| Output Evaluation | Assess quality, relevance, and correctness |
| Safety Evaluation | Detect harmful, disallowed, or risky outputs |
| Consistency Analysis | Measure output variance across runs |
| Regression Detection | Identify semantic drift over time |
| Dataset Management | Version, freeze, and audit evaluation datasets |
| Cost Evaluation | Track and gate token and latency costs |
| Policy Enforcement | Enforce safety and compliance thresholds |
| Human‑in‑the‑Loop Review | Enable structured human judgment |

---

## 4. Service Interfaces (Contracts)

Examples of stable, testable interfaces. No implementation detail appears here.

```
evaluatePrompt(promptRef, datasetRef) → EvaluationReport
evaluateSafety(outputBatch) → SafetyReport
compareEvaluations(baseline, candidate) → RegressionReport
enforceGenAIQualityGate(reports...) → Pass | Fail | Review
```

**Rules:**

- Interfaces never depend on UI
- All evaluations produce machine‑readable artifacts
- Human input is captured as structured data

---

## 5. Execution Units (Runtime Responsibilities)

Each unit is independently deployable and scalable.

| Execution Unit | Responsibility |
|---|---|
| Prompt Evaluation Runner | Executes prompts against models; manages temperature, seed, and sampling configs |
| Model Evaluation Engine | Computes quality metrics; aggregates scores and judgments |
| Safety Evaluation Engine | Runs toxicity, policy, and risk checks; applies red‑line thresholds |
| Regression Analysis Engine | Compares semantic behavior over time |
| Cost & Performance Analyzer | Tracks tokens, latency, and spend |
| Human Review Coordinator | Routes samples for manual evaluation; captures reviewer decisions |

Each unit can evolve independently without changing its service interface contract.

---

## 6. Components (Internal Composition)

**Inside a Model Evaluation Engine:**

- Dataset Loader
- Prompt Renderer
- Model Adapter
- Output Normalizer
- Metric Calculator
- Aggregation Logic
- Report Generator

**Inside a Safety Evaluation Engine:**

- Policy Classifier
- Risk Heuristic Evaluator
- Threshold Comparator
- Escalation Handler

Components are replaceable without changing the Execution Unit's contract.

---

## 7. Technical Interfaces (Concrete Mechanisms)

Typical (non‑prescriptive) mechanisms:

- Model APIs (HTTP/gRPC)
- Batch job execution
- JSON evaluation schemas
- Artifact storage (reports, traces)
- Event emission for CI gating

**Rules:**

- All randomness is explicitly configured
- Inputs and outputs are logged and reproducible
- No "best effort" evaluation paths

---

## 8. Agents (Autonomous Decision‑Support)

Agents are especially valuable for GenAI testing.

| Agent | Role |
|---|---|
| Test Case Generation Agent | Proposes adversarial or edge‑case prompts |
| Prompt Drift Detection Agent | Flags changes in prompt effectiveness |
| Evaluation Triage Agent | Prioritizes samples for human review |
| Cost Optimization Agent | Recommends cheaper evaluation strategies |

**Agent rules:**

- Agents recommend, explain, and justify
- Agents do not bypass quality gates without explicit authority

---

## 9. Constraints (Non‑Negotiables)

### Core Constraints

- Evaluation datasets are versioned and immutable
- Baselines are frozen per release
- Safety violations always block deployment
- Cost overruns can block deployment

### GenAI‑Specific Constraints

- No unreviewed prompt changes in production
- Human review required for:
  - Safety‑critical domains
  - Low‑confidence metrics
- Non‑determinism must be measured, not ignored

---

## 10. Decisions (Recorded Trade‑offs)

The following ADR stubs document key GenAI architectural choices. Each references the risk mitigated, capability enabled, and constraint enforced.

| Decision | ADR |
|---|---|
| Why BLEU/ROUGE are insufficient alone | [ADR-GENAI-001](../adr/adr-genai-001-bleu-rouge-insufficient.md) |
| Why human judgment is required for quality | [ADR-GENAI-002](../adr/adr-genai-002-human-judgment-required.md) |
| Why temperature is fixed during CI | [ADR-GENAI-003](../adr/adr-genai-003-temperature-fixed-in-ci.md) |
| Why safety metrics outweigh accuracy | [ADR-GENAI-004](../adr/adr-genai-004-safety-over-accuracy.md) |
| Why regression is semantic, not textual | [ADR-GENAI-005](../adr/adr-genai-005-semantic-regression.md) |

---

## 11. GenAI Testing Strategy (Derived)

This strategy is **derived from the architecture**—it is not the architecture itself.

### Evaluation Portfolio

| Evaluation Type | Purpose |
|---|---|
| Prompt Linting | Prevent malformed or unsafe prompts |
| Golden Dataset Evaluation | Track quality over time |
| Adversarial Testing | Expose unsafe behavior |
| Consistency Testing | Measure variance |
| Regression Comparison | Detect semantic drift |
| Human Review | Resolve ambiguity |
| Production Sampling | Detect post‑release issues |

This is not a pyramid—it is a **risk‑coverage portfolio**.

---

## 12. CI/CD Flow (Derived View)

```
1. Prompt or code change
2. Prompt validation
3. Model evaluation on golden datasets
4. Safety evaluation
5. Regression comparison vs baseline
6. Cost/performance evaluation
7. Quality gate decision
8. Deploy, block, or require review
```

This flow is **derived**, not architectural. The architecture defines what confidence is; the CI/CD flow implements it.

---

## Key GenAI Principle

> You cannot assert correctness for LLMs.
> You can only **bound behavior**, **measure risk**, and **enforce policy**.

---

## What This Architecture Prevents

- "It looks good to me" deployments
- Prompt changes without evaluation
- Safety as a post‑hoc filter
- Silent quality regression
- Cost surprises in production

---

## Related Documents

- [GenAI Traceability Matrix](./genai-traceability-matrix.md)
- [ADR-GENAI-001: BLEU/ROUGE Insufficient](../adr/adr-genai-001-bleu-rouge-insufficient.md)
- [ADR-GENAI-002: Human Judgment Required](../adr/adr-genai-002-human-judgment-required.md)
- [ADR-GENAI-003: Temperature Fixed in CI](../adr/adr-genai-003-temperature-fixed-in-ci.md)
- [ADR-GENAI-004: Safety Over Accuracy](../adr/adr-genai-004-safety-over-accuracy.md)
- [ADR-GENAI-005: Semantic Regression](../adr/adr-genai-005-semantic-regression.md)
