# Testing Strategy

What "testing" means for this repository, which is a specification, not a
program.

## Two different subjects, kept distinct

1. **Testing done *by* this repo** — verifying the ADM specification site
   itself. There is no code here to unit-test; the repository's executable
   artefact is the Jekyll site, and its automated checks are two: a source
   check over the Markdown pages and the Jekyll build, both run on every
   pull request.
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
  is the final gate: broken front matter, a bad Liquid tag, or an invalid
  `_config.yml` fails the deploy. Since 12 November 2026 it writes the
  version without the tag's leading "v", the form the tracked file and the
  changelog use.
- **GitHub's own branch build** ("pages build and deployment") — also on
  every push to `main`, because the Pages source is set to deploy from the
  `main` branch (as observed 12 November 2026). It builds the site as
  committed, reading the tracked `_data/adm.yml`, and deploys seconds apart
  from `pages.yml`; the later of the two is what the site serves.
- **`.github/workflows/check.yml`** — on every pull request, two jobs. The
  `build` job (added 7 November 2026) runs the same
  `actions/jekyll-build-pages` step as the deploy, against the tracked
  `_data/adm.yml` rather than a tag-derived one, and uploads nothing: a
  Liquid or `_config.yml` break now fails the pull request instead of the
  deploy of `main`. The `check` job runs
  `.github/scripts/check_docs.py` (stdlib Python, no install) over the
  Markdown sources of every page under `docs/` and `CHANGELOG.md`. It
  asserts that each page opens with exactly one front-matter block (no
  `layout:`/`title:`/`permalink:` line reappears in the body, the shape a
  merge leaves behind), and that every internal link resolves: a
  `{{ site.baseurl }}/...` link to a permalink some page declares, a
  relative link to an existing file. A relative link to a bare directory
  fails, because `jekyll-relative-links` rewrites only links to files and
  the directory form breaks under the page's own path. Anchors and external
  links are not checked. Added 2026-10-06. Since 10 October 2026 it also
  fails when the README's ADR table or Testing Architecture list names a
  different set of pages than `docs/adr/` (index aside) or `docs/testing/`
  holds — the README's *What Is Checked* section cites this check, and no
  README claim may cite a check that does not exist. Since 26 October 2026 it
  also fails when a page's first line after the front matter is not one of
  the recognised normative-status lines (listed in `CLAUDE.md` and in the
  script's `STATUS_LINES`), which closed the README's last "no test yet". The
  check proves presence and form; whether a page's status is the right one
  stays a judgement, so a new form of the line is a convention change made in
  both places. Since 12 November 2026 it also fails when the site's version
  records disagree: a `CHANGELOG.md` release heading not of the form
  `## [X.Y.Z] - YYYY-MM-DD`, releases not running newest first under
  `[Unreleased]`, a `_data/adm.yml` version or released date other than the
  newest release's, or a tag that is not of the form `vX.Y.Z` or is newer
  than the newest release. It finds the tag with the deploy's own command,
  `git describe --tags --abbrev=0`, over a full checkout, and its summary
  line names the version and the tag it compared. A tag older than the
  newest release, or no tag at all, only warns, as an annotation on the pull
  request: pushing a release tag is Dermot's call and a desktop step
  (`CLAUDE.md`, *Work that needs the desktop*), and a release pull request is
  necessarily ahead of its own tag. Since 14 November 2026 the link check
  reads the permalink links it was written for. Its pattern read no link
  target with a space in it, and every permalink link on the site is
  written with spaces inside the braces of its `site.baseurl` tag; so from
  6 October to 14 November 2026 a link to a permalink no page declares
  passed, and only relative links were checked. On 14 November that was 69
  unchecked of the 142 internal links on the pages the check reads; all 69
  resolve. The pattern now reads both forms. A link whose target it still
  cannot read fails instead of passing unchecked, and the summary line
  counts the internal links checked, so a check that has stopped looking
  shows in its own output.

## What a spec repo's checks should assert

For a specification, the failure modes are editorial rather than
computational: a dead internal link between layers, an ADR that no index
references, a rule page whose permalink changed under a citation, version
drift between the tag-derived site version and the changelog. The source
check above catches the dead internal link and the missing normative-status
line, and since 12 November 2026 the version drift; the rest are not caught
today.

## Known gaps (candidates for next)

- ~~Run the Jekyll build on pull requests~~ — **closed 2026-11-07** by the
  `build` job in `check.yml` above. The original note: **run the Jekyll
  build on pull requests**, not just on `main` — the same build step in a
  PR-triggered job turns deploy-time failures into review-time failures at
  near-zero cost.
- ~~An internal link checker~~ — **closed 2026-10-06** at the source level by
  `check.yml` above, for relative links only until 14 November 2026, when
  the permalink links were first read; anchors are still unchecked. The
  original note:
  **an internal link checker** over the built site (or the Markdown sources)
  — for a document whose value is cross-referenced layers, rules, ADRs and
  case studies, a resolving-links check is the closest thing a spec has to a
  test suite. The `star-rangers` repo's `check-internal-links.js` is the
  in-account precedent for how much this catches.
- ~~Changelog/version consistency~~ — **closed 2026-11-12** by the version
  check in `check_docs.py` above. The original note: **changelog/version
  consistency** — the site version is derived from git tags at deploy time;
  a check that the newest `CHANGELOG.md` section agrees with the newest tag
  would pin the two together.
- Markdown lint (heading structure, front-matter presence per page) if the
  document set keeps growing.
