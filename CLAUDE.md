# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The canonical public reference for the **Architecture Definition Model (ADM)** — a layered framework for defining, governing, and enforcing the architecture of Generative AI systems. This is a specification repo, not a program: there is no application code, no package.json, and nothing to unit-test. The deliverable is a Jekyll-rendered GitHub Pages site built from the Markdown under `docs/`.

Published in a personal capacity by Dermot Cochran; the README's disclaimer and IP notice (rights, if any, retained by UL Solutions) are load-bearing text — don't edit or remove them casually.

## Build and deploy

Do **not** install Jekyll or run a local build. The site is built entirely by CI:

- `.github/workflows/pages.yml` runs on every push to `main` (and manual dispatch): it derives the ADM version from the latest git tag and **overwrites `_data/adm.yml`** with it, builds with `actions/jekyll-build-pages` (theme `minima`, kramdown, `baseurl: /architecture-definition-model` — see `_config.yml`), and deploys to GitHub Pages.
- The Jekyll build is the only automated gate: broken front matter, a bad Liquid tag, or an invalid `_config.yml` fails the deploy.
- **Nothing runs on pull requests.** A build-breaking PR merges green and fails only when `main` deploys — keep that in mind before merging anything touching front matter or Liquid.

`TestingStrategy.md` covers this in full — what runs, why nothing else does, and the candidate checks (PR builds, an internal link checker, changelog/tag consistency). Read it before adding any check; extend it rather than duplicating its content here.

## Versioning

The site's displayed version (`docs/index.md` reads `site.data.adm.version`) comes **from git tags at deploy time**, not from the tracked `_data/adm.yml` — the workflow regenerates that file. The tracked copy exists for reference and is bumped on release alongside the `CHANGELOG.md` roll and the matching `vX.Y.Z` tag (its own comment says so). `CHANGELOG.md` follows Semantic Versioning with an `[Unreleased]` section; pre-1.0, minor versions may still refine normative semantics.

## Structure and conventions

Every page carries Jekyll front matter (`layout: page`, `title`, `permalink`) and, immediately after it, a **normative-status line** — one of:

- `This page is normative and defines ADM semantics.` (layers, rules, principles, the main index, the changelog)
- `This page is non-normative and indexes recorded architectural decisions.` (the ADR index)
- `This page is illustrative and non-normative. It does not define ADM semantics.` (case studies)

Keep that line accurate on any new page — the normative/non-normative split is the spec's core discipline.

**Permalinks are citations.** Pages are cross-referenced by permalink throughout the site and externally; changing one breaks citations silently (no link checker exists yet). Internal links use `{{ site.baseurl }}/...` because the site serves under a subpath.

The docs tree:

- `docs/layers/` — the ADM layers: seven **vertical** (Intent, Context, Capability, Service Interface, Execution Unit, Component, Technical Interface) and three **horizontal** (Agent, Constraints, Decisions), indexed in `docs/layers/index.md`. Each layer page follows the same shape: Definition / Allowed Content / Forbidden Content / Common Violations. A new layer follows that shape and is added to the index.
- `docs/rules/` — Layer Discipline, Derivation, Refusal.
- `docs/testing/` — the ADM testing-architecture extension (general + GenAI/LLM variants, each with a traceability matrix). This is normative content *of* the specification, governing systems built under ADM — distinct from testing *of* this repo (that's `TestingStrategy.md`).
- `docs/adr/` — two ADR families: general testing ADRs (`ADR-NNN-slug.md`, e.g. ADR-001…004) and GenAI testing ADRs (`adr-genai-NNN-slug.md`, GENAI-001…005) — note the differing filename casing, and that GenAI permalinks drop the `adr-` filename prefix (`/adr/genai-001-.../`). `docs/adr/index.md` carries a table per family plus the ADR template (Status / Context / Decision / Consequences / Linked ADM Elements). A new ADR follows the template, links the ADM capabilities/constraints/risks it touches, and is added to its family's table in the index **and** to the README's ADR table (and `docs/index.md` lists the GenAI ones).
- `docs/case-studies/` — illustrative, non-normative. `star-rangers.md` is the model: statements from a real system classified against **existing ADM layers only**, with rationale per assignment. A new case study follows that pattern and gets a link from `docs/index.md`'s navigation.
- `docs/adm-and-c4.md` — positioning: ADM is authoritative/normative, C4 is descriptive/derived.

Top-level navigation lives in two places: `_config.yml`'s `header_pages` (the site header) and `docs/index.md`'s Navigation section — check both when adding a top-level page.

## Making changes

- Per the README: architectural changes must respect ADM layer discipline and semantic rules, and **significant changes should be proposed as ADRs**, not implicit edits.
- Record changes under `CHANGELOG.md`'s `[Unreleased]`; released sections describe tagged releases and stay as they are.
- Licensing is split (see `LICENSE.md` for the summary): documentation and explanatory text are **CC BY 4.0** (`LICENSE.docs`); example code, configuration, and prompt templates are **Apache-2.0** (`LICENSE.code`). Know which side a new file falls on.
