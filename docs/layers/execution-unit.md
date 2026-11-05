---
layout: page
title: Execution Unit
permalink: /layers/execution-unit/
---

This page is normative and defines ADM semantics.

# Execution Unit

## Definition
An independently deployable and running unit.

## Allowed Content
- Deployable units
- Runtime ownership boundaries
- Unit-level operational boundaries

## Forbidden Content
- Pure capability statements
- Non-deployable service contracts
- Cross-unit internal decomposition details

## Common Violations
- Modeling non-deployable concepts as Execution Units
- Collapsing multiple layers into one unit definition

## See it in use
- [Running example]({{ site.baseurl }}/overview/#execution-unit): the AI support assistant's Execution Unit
- [Worked Examples]({{ site.baseurl }}/worked-examples/)
