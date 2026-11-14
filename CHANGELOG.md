---
layout: page
title: Changelog
permalink: /changelog/
---

This page is normative and defines ADM semantics.

# Changelog

Version numbers follow [Semantic Versioning](https://semver.org/). While the specification is pre-1.0, minor versions may still refine normative semantics; from 1.0.0 onward, breaking changes to normative content require a major version.

## [Unreleased]

### Added
- Context layer (`/layers/context/`, 7 November 2026): *Allowed Content* now lists *External conditions and obligations the system operates under*, the kind of statement the Overview's running example already places in Context (answers may affect regulated product usage; responses must be logged for review). The definition, the other allowed items and the forbidden list are unchanged.

### Fixed
- ADR index (`/adr/`): removed a stray front-matter fragment left by a merge, which rendered as text and a heading after the GenAI table; the general testing ADRs' heading is now a section heading, so the page has one title.
- The ADR-index and layer-index links in the Testing Architecture and Traceability Matrix pages now name the index pages, so they resolve on the published site (a bare directory link resolved under the page's own path).

### Documentation
- PR checks (14 November 2026): the source check now checks the site's permalink links. Its pattern read no link target with a space in it, which is how every `site.baseurl` link is written, so since 6 October 2026 those links had passed unchecked and only relative links were checked. On 14 November they were 69 of the 142 internal links on the pages the check reads; all 69 resolve. A link the check cannot read now fails, and its summary line counts the links checked. No page changed.
- PR checks (12 November 2026): the source check now fails when the site's version records disagree: a release heading not of the form `[X.Y.Z] - YYYY-MM-DD` or out of order, a `_data/adm.yml` version or date other than the newest release's, or a tag the newest release does not describe. A release whose tag is not yet pushed only warns. The deploy workflow now writes the version without the tag's "v", so both builds that publish the site show the same string once a release's tag is pushed. No page changed.
- Main index (7 November 2026): the last line under *Architecture Decision Records* linked `/adr/` a second time, after the *ADR Index* line at the top of the same list; it is removed. No other link moved.
- PR checks (7 November 2026): the Jekyll build now runs on every pull request as a second job in `check.yml`, the same build step the deploy uses, so a Liquid or `_config.yml` break fails at review instead of when `main` deploys. `TestingStrategy.md` closes that known gap and now counts two automated checks where it said one. No page changed.
- Layer pages (`/layers/`, 5 November 2026): each of the ten pages now ends with *See it in use*, linking to that layer in the Overview's running example and to Worked Examples, and for Decisions to the ADR index. Pointers only; no definition, allowed or forbidden text moved.
- Overview (`/overview/`, 30 October 2026): the running example now carries a *Decisions* section after *Constraints*, so it walks all ten layers of the canonical set it lists instead of stopping at nine. Three decisions, each referencing elements the example already places and defining none. No existing text changed.
- Main index (26 October 2026): the two normative testing pages (Testing Architecture, Traceability Matrix) now sit under the *Testing Architecture* heading instead of under *Architecture Decision Records*, and the general ADRs 001–004 are listed beside the GenAI ones. Links moved only; no wording changed.
- Source check (26 October 2026): the PR check now fails when a page's first line after the front matter is not a recognised normative-status line, so the README's claim that every page says whether it is normative names its check instead of "no test yet". No page changed.
- Licence and disclaimer (18 October 2026, Dermot's direction): `LICENSE.md`, the README and the two docs pages that repeated it now name Dermot Cochran as copyright holder, and the unconditional lines saying rights are retained by UL Solutions are removed. The conditional disclaimer stays, now adding that ADM was never adopted or used by any of his employers.
- Case study (`/case-studies/star-rangers/`): retitled under the work's current title, *Fian Ilchruinne*, and the opening reworded to say plainly that the page studies the publishing system and its governance, not the novel, whose world, ideas and direction are the author's and whose prose he has approved as its own voice. The permalink is unchanged.
- Tutorials (`/tutorials/`): each tutorial in the set now links to where it is already practised (Worked Examples, the Star Rangers case study's Violations section, ADM and C4). No new tutorial content.
- Normative-status lines (10 October 2026): the Testing Architecture and Testing Traceability Matrix pages now state that they are normative, and each of the nine ADRs states that it is non-normative and records an architectural decision, in the line after the front matter as every other page does. No normative content changed.
- README: a *What Is Checked* section names the check behind each claim it makes, or says there is none yet; the PR source check now also fails when the README's ADR table or testing list does not match the pages on disk.

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
