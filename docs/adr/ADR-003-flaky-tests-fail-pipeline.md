---
layout: page
title: "ADR-003: Flaky Tests Fail the Pipeline Instead of Retrying"
permalink: /adr/ADR-003-flaky-tests-fail-pipeline/
---

This page is non-normative and records an architectural decision.

# ADR-003: Flaky Tests Fail the Pipeline Instead of Retrying

## Status

Accepted

---

## Context

Flaky tests—tests that produce inconsistent results without code changes—erode trust in the test suite and obscure real failures. Automatic retry logic masks flakiness rather than resolving it; over time, teams treat flaky failures as expected noise and stop acting on them.

If a test is non-deterministic, it cannot reliably serve as a quality gate. Retrying a non-deterministic test produces a stochastic pass, not a meaningful signal.

---

## Decision

Flaky tests fail the pipeline.  
Retry logic is not applied to mask non-deterministic behavior.  
A Flakiness Detection Agent may identify and quarantine confirmed flaky tests, but quarantined tests are tracked and must be resolved or removed.

---

## Consequences

- Teams are forced to address flakiness rather than normalizing it.
- The flakiness backlog becomes a visible, governable artifact.
- Pipeline pass rates are meaningful; a passing pipeline is a trustworthy signal.
- Short-term friction is accepted in exchange for long-term pipeline integrity.
- A Flakiness Detection Agent is a recommended but optional enhancement (see [Testing Architecture — Agents](../testing/testing-architecture.md#8-agents)).

---

## Linked ADM Elements

**Capabilities:**
- Quality Gates — gates must produce trustworthy, deterministic decisions
- Regression Detection — detects unintended changes; flakiness masks regression signals

**Constraints:**
- Tests must be deterministic
- Tests must be repeatable
- CI feedback must be trustworthy

**Risks addressed:**
- Flaky pipelines normalized as "CI issues" rather than test quality failures
- Real regressions hidden by retry-induced false passes
- Loss of confidence in the test suite as a governance instrument

---

## Related Documents

- [ADR Index](index.md)
- [Testing Architecture — Agents](../testing/testing-architecture.md#8-agents)
- [Testing Architecture — Constraints](../testing/testing-architecture.md#9-constraints)
- [Traceability Matrix](../testing/traceability-matrix.md)
