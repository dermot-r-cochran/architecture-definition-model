# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The canonical public reference for the **Architecture Definition Model (ADM)** — a layered framework for defining, governing, and enforcing the architecture of Generative AI systems. This is a specification repo, not a program: there is no application code, no package.json, and nothing to unit-test. The deliverable is a Jekyll-rendered GitHub Pages site built from the Markdown under `docs/`.

Published in a personal capacity by Dermot Cochran; the copyright is his (Dermot, 18 October 2026: ADM is his own idea, inspired by his years of software engineering and never adopted or used by any employer). The README's conditional disclaimer (rights that *may arise from my employment* retained by UL Solutions, as applicable) is load-bearing text, kept at his choice the same day: don't edit or remove it casually, and don't reintroduce an unconditional UL rights line.

## Build and deploy

Do **not** install Jekyll or run a local build. The site is built entirely by CI:

- `.github/workflows/pages.yml` runs on every push to `main` (and manual dispatch): it derives the ADM version from the latest git tag and **overwrites `_data/adm.yml`** with it, builds with `actions/jekyll-build-pages` (theme `minima`, kramdown, `baseurl: /architecture-definition-model` — see `_config.yml`), and deploys to GitHub Pages.
- The Jekyll build is the only automated gate: broken front matter, a bad Liquid tag, or an invalid `_config.yml` fails the deploy.
- On pull requests only a source check runs (`.github/workflows/check.yml`: one front-matter block per page, a recognised normative-status line on every page, internal links resolve, the README's ADR table and testing list match the pages on disk; see `TestingStrategy.md`). Each claim the README makes names the check that proves it, or says "no test yet" — never a check that does not exist. **The Jekyll build does not run on pull requests**: a Liquid or `_config.yml` break merges green and fails only when `main` deploys — keep that in mind before merging anything touching Liquid.

`TestingStrategy.md` covers this in full — what runs, why nothing else does, and the candidate checks (PR builds, an internal link checker, changelog/tag consistency). Read it before adding any check; extend it rather than duplicating its content here.

## Versioning

The site's displayed version (`docs/index.md` reads `site.data.adm.version`) comes **from git tags at deploy time**, not from the tracked `_data/adm.yml` — the workflow regenerates that file. The tracked copy exists for reference and is bumped on release alongside the `CHANGELOG.md` roll and the matching `vX.Y.Z` tag (its own comment says so). `CHANGELOG.md` follows Semantic Versioning with an `[Unreleased]` section; pre-1.0, minor versions may still refine normative semantics.

## Structure and conventions

Every page carries Jekyll front matter (`layout: page`, `title`, `permalink`) and, immediately after it, a **normative-status line** — one of:

- `This page is normative and defines ADM semantics.` (layers, rules, principles, the main index, the changelog)
- `This page is non-normative and indexes recorded architectural decisions.` (the ADR index)
- `This page is non-normative and records an architectural decision.` (each ADR)
- `This page is illustrative and non-normative. It does not define ADM semantics.` (case studies)
- `This page is non-normative and provides ...` (the two GenAI/LLM testing pages, each finishing the sentence with what it provides; kept non-normative by Dermot's ruling of 10 October 2026 because they describe practice that is still settling)

Keep that line accurate on any new page — the normative/non-normative split is the spec's core discipline. The PR source check fails a page whose first body line is not one of these forms (`STATUS_LINES` in `.github/scripts/check_docs.py`, added 26 October 2026); it checks presence and form, not whether the status is right, so a new form of the line is added in both places.

**Permalinks are citations.** Pages are cross-referenced by permalink throughout the site and externally; changing one breaks internal links, which the PR source check now catches, and external citations silently. Internal links use `{{ site.baseurl }}/...` because the site serves under a subpath.

The docs tree:

- `docs/layers/` — the ADM layers: seven **vertical** (Intent, Context, Capability, Service Interface, Execution Unit, Component, Technical Interface) and three **horizontal** (Agent, Constraints, Decisions), indexed in `docs/layers/index.md`. Each layer page follows the same shape: Definition / Allowed Content / Forbidden Content / Common Violations. A new layer follows that shape and is added to the index.
- `docs/rules/` — Layer Discipline, Derivation, Refusal.
- `docs/testing/` — the ADM testing-architecture extension (general + GenAI/LLM variants, each with a traceability matrix). The general testing pages are normative content *of* the specification (the two GenAI/LLM pages are the stated exception, non-normative since 10 October 2026), governing systems built under ADM — distinct from testing *of* this repo (that's `TestingStrategy.md`).
- `docs/adr/` — two ADR families: general testing ADRs (`ADR-NNN-slug.md`, e.g. ADR-001…004) and GenAI testing ADRs (`adr-genai-NNN-slug.md`, GENAI-001…005) — note the differing filename casing, and that GenAI permalinks drop the `adr-` filename prefix (`/adr/genai-001-.../`). `docs/adr/index.md` carries a table per family plus the ADR template (Status / Context / Decision / Consequences / Linked ADM Elements). A new ADR follows the template, links the ADM capabilities/constraints/risks it touches, and is added to its family's table in the index **and** to the README's ADR table (and `docs/index.md` lists both families under its ADR heading, since 26 October 2026).
- `docs/case-studies/` — illustrative, non-normative. `star-rangers.md` is the model: statements from a real system classified against **existing ADM layers only**, with rationale per assignment. A new case study follows that pattern and gets a link from `docs/index.md`'s navigation.
- `docs/adm-and-c4.md` — positioning: ADM is authoritative/normative, C4 is descriptive/derived.

Top-level navigation lives in two places: `_config.yml`'s `header_pages` (the site header) and `docs/index.md`'s Navigation section — check both when adding a top-level page.

## Making changes

- Per the README: architectural changes must respect ADM layer discipline and semantic rules, and **significant changes should be proposed as ADRs**, not implicit edits.
- Record changes under `CHANGELOG.md`'s `[Unreleased]`; released sections describe tagged releases and stay as they are.
- Licensing is split (see `LICENSE.md` for the summary): documentation and explanatory text are **CC BY 4.0** (`LICENSE.docs`); example code, configuration, and prompt templates are **Apache-2.0** (`LICENSE.code`). Know which side a new file falls on.

## Which model does which work

Dermot's direction, 2026-10-11: the account-wide split recorded in `star-rangers`' `CLAUDE.md`, applied here. Opus is the default. Fable is kept for narrative prose and image prompts and has no work in this repository.

- **Haiku: reading and trivial fixes.** Read-only searches, broken internal links, front-matter fixes and table drift the PR source check reports.
- **Sonnet: code and tests.** Changes to `.github/workflows/` and the source-check script. (No application code lives here.)
- **Opus: the protected parts.** Every page's content: the normative semantics, the ADRs, each page's normative-status line, and the README's disclaimer and IP notice. No model below Opus edits these, even where a gate would catch the mistake.
- **Opus reviews and approves** a Haiku or Sonnet subagent's diff, and it merges when CI is green. Opus escalates where a change needs a judgement it should not make alone: to Fable where one is available, otherwise to Dermot directly as choices (Dermot, 2026-10-11). Haiku may also work under a Sonnet subagent, its searches and summaries feeding Sonnet's job as input; approval still comes from Opus, never from Sonnet.
- **Chrome extension:** Opus for anything that signs in, submits or posts; Sonnet for read-only browsing; never Haiku. The extension acts in Dermot's own Chrome with his sign-ins, and a web page can carry text written to steer the model.

A subagent runs on its parent session's model unless the call names another, so name the model on every delegation.

## Work that needs the desktop

A Claude Code cloud session has this repository in a fresh container and
nothing else of Dermot's. It cannot read `F:\` (the working folder and its
TODO lists), the local memory store, or a key that lives only on his Windows
machine, and the GitHub path it pushes through cannot publish tags. **When a
piece of work stops at one of those limits, the step that is left gets an
issue here labelled `needs-desktop`**, saying what is owed, the exact command
or file where it is known, and anything it waits on. A sentence in a pull
request body or in a session's closing report is not a record, because
nothing reads those again (added 2026-10-05 at Dermot's direction, after a
release tag in `star-rangers` sat unpushed for three days with a sentence in
a merged pull request as the only note that it was owed).

A desktop session lists the whole queue, across every repository, with
`gh search issues --owner dermot-r-cochran --label needs-desktop --state open`.
It checks the queue when it starts work, does what it can, and closes each
issue with a line saying what was done.

Two limits on what goes in. Issues here are publicly readable, so nothing
personal goes in one. And a decision that is Dermot's is not a desktop step:
it stays in the pull request or ADR that names it and does not take this
label.

In this repository the usual case is **the release tag**. The site's version
comes from git tags at deploy time (*Versioning* above), so a release is not
finished until `vX.Y.Z` is pushed, and that push is a local step. Cutting a
release is Dermot's call: the issue records that the tag is owed and at
which commit; it does not authorize a desktop session to cut it.

## Related repositories

The map of Dermot's public repositories and what crosses between them is
`RELATED-REPOSITORIES.md` in `dermot-r-cochran/star-rangers`; this section
names only this repository's own neighbours (added 2026-09-29 at his
direction).

- **`dermot-r-cochran/star-rangers`** is this specification's worked case
  study (`docs/case-studies/star-rangers.md`): its `CLAUDE.md` is the
  human-owned governance document the case study classifies against the
  layers. The relationship runs both ways: that repository's About page names
  the ADM as lineage under *The engineering behind the record*, and
  `TestingStrategy.md` here cites its `check-internal-links.js` as the
  in-account precedent for a link checker. When the governance in that
  repository changes shape, read the case study again; it is illustrative and
  dated, but a statement in it that is no longer true of the system it
  describes is worth correcting.
- **`dermot-r-cochran/shadow-architect`** is the nearest in subject on the
  enforcement side: it gates deployed AI systems at defined boundaries, where
  this document defines architecture. Neither cites the other today.
- **Siblings by convention:** the account's engineering repositories share a
  way of working, not code: a `TestingStrategy.md` that keeps testing
  mechanics apart from the repository's rules, a CI coverage ratchet at the
  measured baseline, and architecture decision records guarded by named tests
  where a repository keeps them. Which repositories follow which, and how far
  each one's tests reach its decisions, is listed once, in the map's *Siblings
  by convention* section, and not restated here: counts copied into several
  files drift (this paragraph said `swarm` guarded "three of its four" ADRs
  after its fifth guard had landed). Here the two ADR families are the
  specification's own and no test guards them, as `TestingStrategy.md`
  explains.
