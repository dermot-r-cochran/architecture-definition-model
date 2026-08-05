---
layout: page
title: ADM Specification
permalink: /
---

This page is normative and defines ADM semantics.

# Architecture Definition Model (ADM) Specification

**ADM Version:** `{{ site.data.adm.version | default: "0.0.0-unreleased" }}`

The ADM is the single source of truth for architecture semantics.

## Canonical Reference

This repository serves as the canonical public reference for the
Architecture Definition Model (ADM) as described by the author.

Forks and derivatives are permitted under the applicable licenses;
however, this repository is the authoritative reference location.

## Navigation
- [Introduction]({{ site.baseurl }}/introduction/)
- [Overview]({{ site.baseurl }}/overview/)
- [ADM and C4: Complementary, Not Competing]({{ site.baseurl }}/adm-and-c4/)
- [Principles]({{ site.baseurl }}/principles/)
- [Tutorials]({{ site.baseurl }}/tutorials/)
- [Worked Examples]({{ site.baseurl }}/worked-examples/)
- [Layers]({{ site.baseurl }}/layers/)
- [Rules]({{ site.baseurl }}/rules/)
- [Case Studies]({{ site.baseurl }}/case-studies/star-rangers/)
- [Changelog]({{ site.baseurl }}/changelog/)

## Testing Architecture

- [GenAI/LLM Testing Architecture]({{ site.baseurl }}/testing/genai-llm-testing-architecture/) — ADM extension for LLM-powered systems
- [GenAI Traceability Matrix]({{ site.baseurl }}/testing/genai-traceability-matrix/) — Capabilities → Constraints → Risks → Evidence

## Architecture Decision Records

- [ADR Index]({{ site.baseurl }}/adr/) — All recorded architectural trade-off decisions
- [ADR-GENAI-001: BLEU/ROUGE Insufficient]({{ site.baseurl }}/adr/genai-001-bleu-rouge-insufficient/)
- [ADR-GENAI-002: Human Judgment Required]({{ site.baseurl }}/adr/genai-002-human-judgment-required/)
- [ADR-GENAI-003: Temperature Fixed in CI]({{ site.baseurl }}/adr/genai-003-temperature-fixed-in-ci/)
- [ADR-GENAI-004: Safety Over Accuracy]({{ site.baseurl }}/adr/genai-004-safety-over-accuracy/)
- [ADR-GENAI-005: Semantic Regression]({{ site.baseurl }}/adr/genai-005-semantic-regression/)
- [Testing Architecture (ADM-Aligned)]({{ site.baseurl }}/testing/testing-architecture/)
- [Traceability Matrix]({{ site.baseurl }}/testing/traceability-matrix/)
- [Architecture Decision Records (ADRs)]({{ site.baseurl }}/adr/)

## Copyright and License
Copyright © 2026.
Authorship by Dermot Cochran.
Intellectual property rights, if any, retained by UL Solutions.

Creative Commons Attribution 4.0 International (CC BY 4.0)

## Disclaimer

This project is published in a personal capacity.

Any intellectual property rights that may arise from my employment are retained by
UL Solutions, as applicable. No endorsement, sponsorship, or approval by
UL Solutions is implied.

The views and materials expressed here are my own and are provided for
informational purposes only.

## License

### Documentation and explanatory text

This documentation is provided under the Creative Commons Attribution 4.0
International License (CC BY 4.0), to the extent permitted by applicable
intellectual property rights.

Intellectual property rights, if any, are retained by UL Solutions.

### Example code, configuration, and prompts

Licensed under the Apache License, Version 2.0, to the extent permitted by
applicable intellectual property rights.

Nothing in this license grants rights to intellectual property owned by
UL Solutions beyond what is permitted by law.
