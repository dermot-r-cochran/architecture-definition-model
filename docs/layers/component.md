---
layout: page
title: Component
permalink: /layers/component/
---

This page is normative and defines ADM semantics.

# Component

## Definition
Internal structure within an Execution Unit only.

## Allowed Content
- Internal module responsibilities
- Intra-unit structure
- Internal interaction boundaries

## Forbidden Content
- External service contracts
- Cross-unit deployment semantics
- System-wide capability declarations

## Common Violations
- Exposing components as external contracts
- Defining components outside an Execution Unit

## See it in use
- [Running example]({{ site.baseurl }}/overview/#component): the AI support assistant's Component
- [Worked Examples]({{ site.baseurl }}/worked-examples/)
