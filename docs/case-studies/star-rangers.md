---
layout: page
title: "Case Study: Star Rangers — a Generative-AI-Coauthored Publishing System"
permalink: /case-studies/star-rangers/
---

This page is illustrative and non-normative. It does not define ADM semantics.

# Case Study: Star Rangers — a Generative-AI-Coauthored Publishing System

## The system

[Star Rangers / *Fian Ilchruinne*](https://github.com/dermot-r-cochran/star-rangers)
is an Eleventy-based interactive novel published from one repository to several
independently branded production domains. It is maintained jointly by a human
author and a generative AI agent (Claude Code) working directly against the
repository — drafting prose, performing mechanical fixes, and evolving the
engine — under a written governance document (`CLAUDE.md`) that functions as
the system's human-owned architecture definition.

Two properties make it a useful ADM case study:

1. **The generative agent is a first-class worker inside the system**, not a
   tool outside it — so the architecture must govern agent behavior, not just
   code structure.
2. **The architecture document is prose**, yet remains enforceable, because
   its constraints split cleanly into machine-checkable structural gates (CI
   validators) and human-judgment gates (review tiers) — a working
   demonstration of the principle recorded in
   [ADR-GENAI-002: Human Judgment Required]({{ site.baseurl }}/adr/genai-002-human-judgment-required/).

## Statements and Layer Assignments

Statements below are drawn from the repository's own governance and code
documentation, classified against existing ADM layers only.

| Statement | ADM Layer | Rationale |
|---|---|---|
| "Publish one canonical interactive novel as a single trustworthy record, readable through several independently branded doors." | Intent | The system's purpose and its governing quality attribute (record integrity); no structure or implementation. |
| "GitHub hosts the repository and CI; cPanel clones pull and deploy per domain; reader comments live in GitHub Discussions via giscus; readers arrive through several production domains." | Context | External actors and neighboring systems; none of them are the system's own structure. |
| "Content filtering: narrow a deployment to a subset of one record without ever contradicting it." | Capability | A stable, tool-agnostic ability; the *subset-never-variant* property is what the capability promises, independent of implementation. |
| "Edition resolution: resolve a domain's identity — palette, branding, content scope — from a reviewed registry, falling back key by key." | Capability | Names an ability (identity resolution), not the module that performs it. |
| "One schema per content type, in a single registry consumed by both the validator and the scaffolder, so they cannot drift apart." | Service Interface | A named contract with two consumers; the shared-registry design is the contract's single-meaning guarantee. |
| "The editions registry is keyed by domain; the deploy script queries it to fill any key the machine-local configuration leaves unset, and logs each key's provenance." | Service Interface | A queryable contract between repository and deployment, with defined precedence semantics. |
| "The Eleventy build; the per-clone deploy script run." | Execution Unit | Deployable runtime responsibilities that perform the work. |
| "`content-filter.js`, `storyline-threads.js`, `markdown-containers.js`, the schema validator, the link checker." | Component | Internal, replaceable parts of the build; invisible across the service boundary. |
| "Markdown front matter; `CHARACTERS`/`TOPICS`/`THREADS` environment variables; an untracked `deploy.conf`; cPanel Git Version Control." | Technical Interface | Concrete mechanisms by which contracts are carried; examples, not prescriptions. |
| "The generative agent drafts narrative, performs mechanical fixes, and merges engine changes — under a three-tier authority boundary: *proceed and merge when CI is green* (engine, docs, mechanical fixes), *draft it and stop* (anything asserting a fact about the fictional world), *never without an explicit instruction in the current session* (history rewrites, live-domain identity changes)." | Agent (horizontal) | An autonomous role defined by which capabilities it may exercise at which authority level; it references structure and never defines it. |
| "Canon is centralised: nothing a deployment variant carries may assert a fact about the world. Private content is included only by explicit naming, on every build. A chapter's discussion identity is permanent and moves with content, never with position." | Constraints (horizontal) | Non-negotiable rules that bind every vertical layer, stated independently of any mechanism that enforces them. |
| "Dated *settled* decisions recorded inline in the governance document and design notes (e.g. 'settled 2026-07-30: `CUSTOM_LORE_FILE` deprecated — it was the one route to per-domain canon, and there is deliberately no replacement'), plus a Keep-a-Changelog history." | Decisions (horizontal) | Recorded trade-offs with dates and rationale — ADR practice in lightweight form. |

## The Agent layer in practice

The repository's stated rationale for its authority boundary is a compact
statement of ADM's own division of labor:

> "The gates prove structure, not judgement. [The validators] can show that a
> page is well-formed, uniquely identified and fully resolved. Nothing in the
> toolchain can show that a sentence is *true in this world* … So mechanical
> correctness is delegable and assertions about the world are not."

Machine-checkable conformance is delegated to the agent with standing
permission; semantic authority is retained by the human. Two supporting
practices complete the loop:

- **Auditable evolution.** Every agent session is required to "say what you
  did" — report drafted narrative, canon changes, and configuration touches
  plainly, "so nothing lands by default because nobody noticed it."
- **Constraint asymmetry by construction.** Deployment-side rules are
  enforced *structurally* (the configuration format has no field that could
  violate them), while fork-side rules are enforced *contractually* (by
  licence) — the system chooses, per boundary, whether a constraint is made
  unbreakable or made accountable.

## Violations (historical, since corrected)

Real defects from the repository's history, classified as layer-discipline
violations — each was corrected by moving the statement to its proper layer.

| Violating arrangement | What was wrong | Correction |
|---|---|---|
| A single `theme` value selected both a domain's palette and its identity/copy ("`{% raw %}{% if theme == "fellowship" %}{% endraw %}`"). | A Technical Interface value (a CSS palette name) was carrying Capability-level meaning (domain identity); two concerns, one token, single-meaning semantics broken. | Split into independent axes (`EDITION` for identity, `THEME` for palette), with a migration fallback recorded as a dated decision. |
| `CUSTOM_LORE_FILE` allowed a deployment to inject a content page per clone. | A deployment-scope mechanism violated the system's governing Constraint (canon is centralised; variants may only subtract). | Deprecated with deliberately no replacement — the decision record states that the absence *is* the design. |
| Page inclusion was classified by the page's `layout` value. | A derived, computed field was used as if it were an authoritative input, making classification order-dependent and fragile. | Reclassified by input path (an invariant of the page), with the reasoning preserved as an in-code decision record. |

## Conformance summary

All classified statements map to existing ADM layers without introducing new
layers or redefining concepts. What the case contributes as illustration:

1. An architecture definition can be prose and still be enforceable, when
   every constraint is assigned to either a structural gate or a judgment
   gate — and the assignment itself is explicit.
2. An agent can hold broad standing permissions without holding semantic
   authority, if the Agent-layer definition is written as *which capabilities
   at which authority tier* rather than as a task list.
3. Dated inline "settled" decisions function as ADRs at a scale where a
   formal ADR process would go unmaintained — the discipline survives because
   it costs one sentence.
