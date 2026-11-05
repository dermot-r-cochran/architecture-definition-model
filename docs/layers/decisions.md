---
layout: page
title: Decisions
permalink: /layers/decisions/
---

This page is normative and defines ADM semantics.

# Decisions

## Definition
Recorded choices (ADRs) that reference ADM elements but do not redefine them.

## Allowed Content
- Decision records tied to ADM elements
- Rationale for choices
- Implications on existing ADM elements

## Forbidden Content
- New architectural structure definitions
- Layer redefinitions
- Standalone semantics outside ADM

## Common Violations
- Using ADRs to introduce new layers
- Using ADRs to replace ADM definitions

## See it in use
- [Running example]({{ site.baseurl }}/overview/#decisions): the AI support assistant's Decisions
- [Worked Examples]({{ site.baseurl }}/worked-examples/)
- [ADR Index]({{ site.baseurl }}/adr/)
