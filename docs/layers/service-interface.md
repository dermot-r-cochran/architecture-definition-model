---
layout: page
title: Service Interface
permalink: /layers/service-interface/
---

This page is normative and defines ADM semantics.

# Service Interface

## Definition
A contractual boundary (API, schema, SLA); not deployable.

## Allowed Content
- API contracts
- Schemas
- Service-level agreements

## Forbidden Content
- Deployment descriptors
- Runtime process ownership
- Internal component structure

## Common Violations
- Treating a service contract as a deployable unit
- Embedding component internals in interface definitions

## See it in use
- [Running example]({{ site.baseurl }}/overview/#service-interface): the AI support assistant's Service Interface
- [Worked Examples]({{ site.baseurl }}/worked-examples/)
