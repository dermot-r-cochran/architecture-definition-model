---
layout: page
title: Changelog
permalink: /changelog/
---

This page is normative and defines ADM semantics.

# Changelog

Version numbers follow [Semantic Versioning](https://semver.org/). While the specification is pre-1.0, minor versions may still refine normative semantics; from 1.0.0 onward, breaking changes to normative content require a major version.

## [Unreleased]

### Fixed
- ADR index (`/adr/`): removed a stray front-matter fragment left by a merge, which rendered as text and a heading after the GenAI table; the general testing ADRs' heading is now a section heading, so the page has one title.
- The ADR-index and layer-index links in the Testing Architecture and Traceability Matrix pages now name the index pages, so they resolve on the published site (a bare directory link resolved under the page's own path).

### Documentation
- Tutorials (`/tutorials/`): each tutorial in the set now links to where it is already practised (Worked Examples, the Star Rangers case study's Violations section, ADM and C4). No new tutorial content.

## [0.1.0] - 2026-08-05

First tagged release of the public ADM specification site: the canonical page structure (layers, rules, principles, testing extensions, ADRs, tutorials, worked examples), the ADM/C4 positioning, and the first case study. The published site now displays its specification version, sourced from `_data/adm.yml` and matching this changelog and the `v0.1.0` git tag.

### Added
- Initial public ADM specification site scaffolding and canonical page structure.

### Documentation
- Added **Case Study: Star Rangers** (`/docs/case-studies/star-rangers.md`) — a non-normative case study of a generative-AI-coauthored publishing system governed under ADM-style discipline: statements classified against existing layers, the Agent layer's authority tiers in practice, historical layer-discipline violations with their corrections, and what the case illustrates about prose architecture definitions, agent authority, and lightweight decision records.
- Added **ADM and C4: Complementary, Not Competing** (`/docs/adm-and-c4.md`) to explain how ADM and C4 work together without redefining either model.
- Added explicit positioning that ADM is authoritative, normative, and enforceable, while C4 is descriptive and illustrative.
- Added explicit statement that C4 diagrams are derived artifacts from ADM, not the architecture itself.
- Added an ADM-to-C4 mapping section aligned with ADM layer discipline.
- Updated main documentation navigation (`docs/index.md`) to include the new ADM and C4 page.
- Updated the ADM Overview page (`docs/overview.md`) with a new **How ADM Relates to C4** section linking to the new page.
