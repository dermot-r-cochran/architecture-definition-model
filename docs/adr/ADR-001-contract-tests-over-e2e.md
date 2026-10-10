---
layout: page
title: "ADR-001: Contract Tests Favored Over E2E in CI"
permalink: /adr/ADR-001-contract-tests-over-e2e/
---

This page is non-normative and records an architectural decision.

# ADR-001: Contract Tests Favored Over E2E in CI

## Status

Accepted

---

## Context

End-to-end (E2E) tests validate full journeys through a deployed system but are slow, environment-dependent, and costly to maintain. In CI pipelines where feedback time is a hard constraint, running a full E2E suite on every change makes the pipeline impractical.

Contract tests verify the behavioral agreement between a consumer and a provider at the service interface level. They run in isolation, require no deployed environment, and produce fast, deterministic feedback.

---

## Decision

Contract tests are the primary mechanism for protecting service boundaries in CI.  
E2E tests are reserved for critical journeys and are run at a defined stage in the pipeline—not on every commit.

---

## Consequences

- CI feedback time is reduced significantly for service-boundary changes.
- Service teams own their contracts; violations surface at the interface, not in an opaque E2E failure.
- E2E test coverage is intentionally narrower; critical journey selection is a governed decision.
- Teams must maintain consumer-driven contracts alongside their service code.

---

## Linked ADM Elements

**Capabilities:**
- Test Execution — tests run deterministically and with bounded feedback time
- Quality Gates — gates are enforced at the contract level in CI

**Constraints:**
- Feedback time is bounded (fast enough to block bad changes)
- Tests must be deterministic and repeatable

**Risks addressed:**
- E2E test suites becoming the primary CI bottleneck
- Service boundary regressions going undetected in fast feedback cycles
- Teams adding more E2E tests as a default response to integration failures

---

## Related Documents

- [ADR Index](index.md)
- [Testing Architecture — Testing Strategy](../testing/testing-architecture.md#11-testing-strategy)
- [Traceability Matrix](../testing/traceability-matrix.md)
