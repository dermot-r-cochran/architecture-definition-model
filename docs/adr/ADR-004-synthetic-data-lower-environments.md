---
layout: page
title: "ADR-004: Synthetic Data Used in Lower Environments"
permalink: /adr/ADR-004-synthetic-data-lower-environments/
---

This page is non-normative and records an architectural decision.

# ADR-004: Synthetic Data Used in Lower Environments

## Status

Accepted

---

## Context

Testing with production data in lower environments (development, CI, staging) creates privacy, compliance, and reproducibility risks. Production data cannot always be refreshed to reflect edge cases; it may contain personally identifiable information (PII); and data volumes may be impractical for ephemeral environments.

Synthetic and masked data avoids these issues while still enabling meaningful tests.

---

## Decision

Synthetic or masked data is used in all environments below production.  
Production data is not used in lower environments unless explicitly governed by a data access and masking policy.  
Datasets used for testing and evaluation are versioned, and the version is recorded alongside test results.

---

## Consequences

- Test environments can be provisioned and torn down freely without data-access controls.
- Test data can be seeded deterministically, improving reproducibility.
- Data edge cases must be constructed deliberately; this is accepted as a quality practice.
- For ML systems, synthetic evaluation datasets must be validated for representativeness before they are used as quality gates (see [ADR-002](ADR-002-model-evaluation-blocks-deployment.md)).
- A data versioning and masking capability is required as part of the Data Management capability.

---

## Linked ADM Elements

**Capabilities:**
- Data Management — seeds, masks, and versions test data

**Constraints:**
- Environments are ephemeral and reproducible
- Tests must be environment-independent
- Evaluation datasets are versioned and immutable (ML)

**Risks addressed:**
- PII exposure in lower environments
- Non-reproducible tests caused by uncontrolled data state
- Compliance violations from production data use in CI

---

## Related Documents

- [ADR Index](index.md)
- [ADR-002: Model Evaluation Blocks Deployment](ADR-002-model-evaluation-blocks-deployment.md)
- [Testing Architecture — Capabilities](../testing/testing-architecture.md#3-capabilities)
- [Testing Architecture — Constraints](../testing/testing-architecture.md#9-constraints)
- [Traceability Matrix](../testing/traceability-matrix.md)
