# Testing Strategy

What "testing" means for this repository, which is a specification, not a
program.

## Two different subjects, kept distinct

1. **Testing done *by* this repo** — verifying the ADM specification site
   itself. There is no code here to unit-test; the repository's executable
   artefact is the Jekyll site, and its one automated check is the build.
2. **Testing defined *in* this repo** — the ADM's own testing-architecture
   layer, [`docs/testing/testing-architecture.md`](docs/testing/testing-architecture.md),
   which is a formal architectural artifact governing what confidence means
   for systems *built under* ADM and how implementations must produce it.
   That document is normative content of the specification; this file never
   restates it, only points at it.

Conflating the two would be exactly the category error the ADM warns
against, so this file covers only subject 1.

## What runs today

- **`.github/workflows/pages.yml`** — on every push to `main` (and manual
  dispatch): derives the ADM version from git tags, builds the site with
  `actions/jekyll-build-pages`, and deploys to GitHub Pages. The Jekyll build
  is the de facto gate: broken front matter, a bad Liquid tag, or an invalid
  `_config.yml` fails the deploy.
- **`.github/workflows/check.yml`** — on every pull request: runs
  `.github/scripts/check_docs.py` (stdlib Python, no install) over the
  Markdown sources of every page under `docs/` and `CHANGELOG.md`. It
  asserts that each page opens with exactly one front-matter block (no
  `layout:`/`title:`/`permalink:` line reappears in the body, the shape a
  merge leaves behind), and that every internal link resolves: a
  `{{ site.baseurl }}/...` link to a permalink some page declares, a
  relative link to an existing file. A relative link to a bare directory
  fails, because `jekyll-relative-links` rewrites only links to files and
  the directory form breaks under the page's own path. Anchors and external
  links are not checked. Added 2026-10-06.
- The Jekyll build itself still does not run on pull requests: a PR that
  breaks Liquid or `_config.yml` merges green and fails only when `main`
  tries to deploy.

## What a spec repo's checks should assert

For a specification, the failure modes are editorial rather than
computational: a dead internal link between layers, an ADR that no index
references, a rule page whose permalink changed under a citation, version
drift between the tag-derived site version and the changelog. The source
check above catches the dead internal link; the rest are not caught today.

## Known gaps (candidates for next)

- **Run the Jekyll build on pull requests**, not just on `main` — the same
  build step in a PR-triggered job turns deploy-time failures into
  review-time failures at near-zero cost.
- ~~An internal link checker~~ — **closed 2026-10-06** at the source level by
  `check.yml` above; anchors are still unchecked. The original note:
  **an internal link checker** over the built site (or the Markdown sources)
  — for a document whose value is cross-referenced layers, rules, ADRs and
  case studies, a resolving-links check is the closest thing a spec has to a
  test suite. The `star-rangers` repo's `check-internal-links.js` is the
  in-account precedent for how much this catches.
- **Changelog/version consistency** — the site version is derived from git
  tags at deploy time; a check that the newest `CHANGELOG.md` section agrees
  with the newest tag would pin the two together.
- Markdown lint (heading structure, front-matter presence per page) if the
  document set keeps growing.
