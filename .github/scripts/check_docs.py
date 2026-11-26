"""Source check for the ADM site's Markdown pages (stdlib only).

Five checks, all on the sources rather than the built site:

1. Every page under docs/ (and CHANGELOG.md) opens with exactly one Jekyll
   front-matter block, and no front-matter key line (layout:, title:,
   permalink:) appears again in the body, which is what a stray fragment
   left by a merge looks like.
2. Every internal link resolves: a `{{ site.baseurl }}/...` link must name a
   permalink some page declares, and a relative link must name an existing
   file (jekyll-relative-links rewrites links to .md files; a link to a bare
   directory is not rewritten and breaks on the published site). A link
   whose target the check cannot read fails, and the summary line counts
   the internal links checked (both since 14 November 2026; until then the
   pattern read no target with a space in it, the form every
   `{{ site.baseurl }}` link takes, so those links passed unchecked). Since
   26 November 2026 a link's anchor is checked too: `#fragment` on a link
   to a page, or alone for a link within the page, must be the id of a
   heading on the page it lands on. The ids are derived from the sources
   by the rule the site's Markdown converter applies (kramdown reading
   GitHub-flavoured Markdown; see `heading_ids`), which on that day gave,
   for every page, exactly the heading ids the published site carried.
   Only `#` headings starting a line are read, and a heading whose markup
   could change its id gets none, so an anchor to one fails. A `#` line
   the site does not render as a heading under the derived id (inside a
   `~~~` fence, an HTML comment or a Liquid block, or with a kramdown
   `{: #id}` line beneath it) still counts as one here; no page has one
   (TestingStrategy.md records the limits). The summary line counts the
   anchors.
3. The README's counts match the disk: its ADR table links every ADR page
   under docs/adr/ (index.md aside) and nothing else, and its Testing
   Architecture list links every page under docs/testing/ and nothing else
   (added 10 October 2026).
4. Every page carries a normative-status line: the first non-blank line after
   the front matter is one of the recognised forms listed in CLAUDE.md
   (normative; non-normative index; non-normative decision record;
   illustrative case study; non-normative "provides ..."). The check proves
   the line is present and well-formed; whether a page's chosen status is the
   right one stays a judgement, which is why the forms are few and fixed
   (added 26 October 2026).
5. The site's displayed version agrees across its three records (added
   12 November 2026). CHANGELOG.md's release headings have the form
   `## [X.Y.Z] - YYYY-MM-DD`, newest first, with `## [Unreleased]` above
   them if present; _data/adm.yml's version, and its released date where
   the key is present, equal the newest release's; and the tag pages.yml would publish, found with its own
   command (`git describe --tags --abbrev=0`), is of the form vX.Y.Z and is
   not newer than that release. A tag older than the release, or no tag at
   all, is printed as a warning and does not fail: pushing a release tag is
   Dermot's call and a desktop step, and the release pull request is
   necessarily ahead of its tag.

External links (http, https, mailto) are not checked.
Run from anywhere: python .github/scripts/check_docs.py
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
FRONT_KEY = re.compile(r"^(layout|title|permalink)\s*:")
INLINE_CODE = re.compile(r"`[^`\n]*`")
# A link's target is either the site.baseurl tag and whatever follows it, or
# a run of characters with no space. The first form is there because the tag
# has spaces inside its braces, `{{ site.baseurl }}/overview/`, which is how
# every permalink link on the site is written.
LINK = re.compile(r"\]\(\s*<?(\{\{\s*site\.baseurl\s*\}\}[^)\s>]*|[^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
BASEURL = re.compile(r"^\{\{\s*site\.baseurl\s*\}\}")
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
HEADING = re.compile(r"^#{1,6}[ \t]+(.*)$")
# Markup that could change which letters, digits or hyphens reach a heading's
# id: typographic dashes, underscore emphasis, a link's target, HTML, an
# entity, a backslash escape, Liquid or an explicit {#id}. Other markup is
# made of characters the id rule drops whether or not it is read as markup.
ID_NOT_DERIVED = re.compile(r"--|_|\]\(|\]\[|[<&\\{]")
RELEASE = re.compile(r"^## \[(\d+)\.(\d+)\.(\d+)\] - (\d{4}-\d{2}-\d{2})$")
RELEASE_TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")

# The recognised normative-status lines (CLAUDE.md, "Structure and
# conventions"). A new form is a convention change: add it here and there.
STATUS_LINES = (
    re.compile(r"^This page is normative and defines ADM semantics\.$"),
    re.compile(r"^This page is non-normative and indexes recorded architectural decisions\.$"),
    re.compile(r"^This page is non-normative and records an architectural decision\.$"),
    re.compile(r"^This page is illustrative and non-normative\. It does not define ADM semantics\.$"),
    re.compile(r"^This page is non-normative and provides \S.*\.$"),
)


def pages() -> list[Path]:
    found = sorted((ROOT / "docs").rglob("*.md"))
    changelog = ROOT / "CHANGELOG.md"
    if changelog.exists():
        found.append(changelog)
    return found


def split_front_matter(text: str) -> tuple[str | None, list[str], int]:
    """Return (front matter, body lines, line number of the first body line)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, lines, 1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), lines[i + 1 :], i + 2
    return None, lines, 1


def prose_lines(lines: list[str], first: int) -> list[tuple[int, str]]:
    """Body lines outside fenced code blocks, with their line numbers."""
    kept, fenced = [], False
    for number, line in enumerate(lines, start=first):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            kept.append((number, line))
    return kept


def normalise(url: str) -> str:
    return "/" + url.strip("/") + "/" if url.strip("/") else "/"


def heading_ids(prose: list[tuple[int, str]]) -> tuple[set[str], list[int]]:
    """The ids the published page gives its headings, and the lines of headings given none here.

    The rule is the one kramdown's GitHub-flavoured Markdown parser applies:
    lower-case the heading's text, drop every character that is not a letter,
    a mark, a digit, an underscore, a hyphen, a space or a tab, turn each
    space or tab into a hyphen, and give a repeat of an id already used on
    the page the suffix -1, -2 and so on.
    """
    ids: set[str] = set()
    not_derived: list[int] = []
    seen: dict[str, int] = {}
    for number, line in prose:
        match = HEADING.match(line)
        if not match:
            continue
        text = re.sub(r"[ \t]#+$", "", match.group(1).rstrip()).rstrip()
        if not text:
            continue
        if ID_NOT_DERIVED.search(text):
            not_derived.append(number)
            continue
        slug = "".join(
            char
            for char in text.lower()
            if char in "- \t" or unicodedata.category(char)[0] in "LM" or unicodedata.category(char) in ("Nd", "Nl", "Pc")
        )
        slug = slug.replace(" ", "-").replace("\t", "-")
        repeat = seen.get(slug, 0)
        seen[slug] = repeat + 1
        if slug:
            ids.add(f"{slug}-{repeat}" if repeat else slug)
    return ids, not_derived


def anchor_problem(landing: Path, fragment: str, anchors: dict[Path, tuple[set[str], list[int]]]) -> str | None:
    """Why `#fragment` does not land on a heading of the page, or None if it does."""
    rel = landing.relative_to(ROOT).as_posix() if landing.is_relative_to(ROOT) else landing.as_posix()
    if landing not in anchors:
        return f"has an anchor on {rel}, which is not a page the check reads, so the anchor would go unchecked"
    ids, not_derived = anchors[landing]
    if fragment in ids:
        return None
    problem = f"lands on {rel}, where no heading has the id {fragment!r}"
    if not_derived:
        lines = ", ".join(str(number) for number in not_derived)
        problem += (
            f"; the check derives no id for the heading(s) at line {lines} there, whose markup "
            "could change the id, so an anchor to one of them cannot be confirmed"
        )
    return problem


def status_line(rel: str, lines: list[str], first: int) -> str | None:
    """An error if the page's first body line is not a recognised status line."""
    for number, line in enumerate(lines, start=first):
        text = line.strip()
        if not text:
            continue
        if any(form.match(text) for form in STATUS_LINES):
            return None
        return f"{rel}:{number}: first line after the front matter is not a recognised normative-status line"
    return f"{rel}: has no body after the front matter, so no normative-status line"


def readme_counts() -> list[str]:
    """The README's ADR table and testing list name exactly the pages on disk."""
    readme = ROOT / "README.md"
    if not readme.exists():
        return []
    text = readme.read_text(encoding="utf-8")
    linked = {match.group(1).split("#", 1)[0] for match in LINK.finditer(text)}
    errors = []
    for folder, what in (("docs/adr", "ADR table"), ("docs/testing", "Testing Architecture list")):
        on_disk = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / folder).glob("*.md")
            if path.name != "index.md"
        }
        stated = {target for target in linked if target.startswith(folder + "/") and target.endswith(".md")}
        stated.discard(folder + "/index.md")
        if len(stated) != len(on_disk):
            errors.append(f"README.md: {what} lists {len(stated)} pages; {folder}/ holds {len(on_disk)}")
        for missing in sorted(on_disk - stated):
            errors.append(f"README.md: {what} omits {missing}")
        for extra in sorted(stated - on_disk):
            errors.append(f"README.md: {what} links {extra}, which is not on disk")
    return errors


def dotted(version: tuple[int, ...]) -> str:
    return ".".join(str(part) for part in version)


def changelog_releases() -> tuple[list[tuple[tuple[int, ...], str, int]], list[str]]:
    """CHANGELOG.md's releases as (version, date, line), top to bottom, and any errors in their form or order."""
    changelog = ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return [], ["CHANGELOG.md: not found, so the site's version has no release to agree with"]
    text = changelog.read_text(encoding="utf-8").replace("\r\n", "\n")
    _, lines, first = split_front_matter(text)
    releases: list[tuple[tuple[int, ...], str, int]] = []
    errors: list[str] = []
    headings = 0
    for number, line in prose_lines(lines, first):
        heading = line.rstrip()
        if not heading.startswith("## ["):
            continue
        headings += 1
        if heading == "## [Unreleased]":
            if headings != 1:
                errors.append(f"CHANGELOG.md:{number}: [Unreleased] must be the first section heading")
            continue
        match = RELEASE.match(heading)
        if not match:
            errors.append(f"CHANGELOG.md:{number}: release heading is not of the form '## [X.Y.Z] - YYYY-MM-DD'")
            continue
        try:
            date.fromisoformat(match.group(4))
        except ValueError:
            errors.append(f"CHANGELOG.md:{number}: release date {match.group(4)} is not a calendar date")
        version = tuple(int(part) for part in match.groups()[:3])
        if releases and version >= releases[-1][0]:
            errors.append(
                f"CHANGELOG.md:{number}: release {dotted(version)} is not older than "
                f"{dotted(releases[-1][0])} above it; releases run newest first"
            )
        releases.append((version, match.group(4), number))
    if not releases:
        errors.append("CHANGELOG.md: no release heading of the form '## [X.Y.Z] - YYYY-MM-DD'")
    return releases, errors


def adm_value(text: str, key: str) -> str | None:
    """A top-level scalar from _data/adm.yml, quoted or not (no YAML library)."""
    match = re.search(rf"^{key}\s*:\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s#]+))", text, re.MULTILINE)
    if not match:
        return None
    return next(group for group in match.groups() if group is not None)


def adm_data(version: str, released: str) -> list[str]:
    """_data/adm.yml, which GitHub's branch build publishes as it stands, names the newest release."""
    path = ROOT / "_data" / "adm.yml"
    if not path.exists():
        return ["_data/adm.yml: not found; the site's displayed version is read from it"]
    text = path.read_text(encoding="utf-8")
    errors = []
    stated = adm_value(text, "version")
    if stated is None:
        errors.append("_data/adm.yml: has no version key")
    elif stated != version:
        errors.append(f"_data/adm.yml: version {stated!r} is not CHANGELOG.md's newest release {version!r}")
    stated_date = adm_value(text, "released")
    if stated_date is not None and stated_date != released:
        errors.append(f"_data/adm.yml: released {stated_date!r} is not the date of release {version}, {released!r}")
    return errors


def deploy_tag() -> tuple[str | None, str | None]:
    """The tag pages.yml would publish, found with its own command.

    Returns (tag, None); (None, None) when no tag is reachable from HEAD, as in
    a shallow clone; or (None, reason) when git itself could not be run.
    """
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as error:
        return None, f"git could not be run ({error})"
    if result.returncode != 0:
        return None, None
    return result.stdout.strip() or None, None


def version_agreement() -> tuple[list[str], list[tuple[int, str]], str]:
    """The newest CHANGELOG release, _data/adm.yml and the deploy's tag agree.

    Returns errors, warnings as (CHANGELOG.md line, message), and a note of
    what was compared, for the summary line.
    """
    releases, errors = changelog_releases()
    if not releases:
        return errors, [], "no release to compare"
    newest, released, line = releases[0]
    version = dotted(newest)
    errors += adm_data(version, released)
    tag, unavailable = deploy_tag()
    warnings: list[tuple[int, str]] = []
    # A tag older than the newest release, or none at all, only warns. Cutting
    # a release and pushing its tag is Dermot's call and a desktop step
    # (CLAUDE.md, "Work that needs the desktop"), and the release pull request
    # is necessarily ahead of its own tag, so this state must not fail the
    # check; it must be visible on the pull request.
    if unavailable:
        warnings.append((line, f"{unavailable}, so no tag was compared with release {version}"))
    elif tag is None:
        warnings.append((
            line,
            f"release {version} has no tag reachable from HEAD (a clone without history and tags "
            f"has none): v{version} is owed, and until it is pushed pages.yml publishes 0.0.0-unreleased",
        ))
    else:
        match = RELEASE_TAG.match(tag)
        if not match:
            errors.append(
                f"CHANGELOG.md:{line}: the newest reachable tag {tag!r} is not of the form vX.Y.Z, "
                "and pages.yml would publish it as the site's version"
            )
        else:
            tagged = tuple(int(part) for part in match.groups())
            if tagged > newest:
                errors.append(
                    f"CHANGELOG.md:{line}: tag {tag} is newer than the newest release {version}, "
                    "so the changelog does not describe the version pages.yml would publish"
                )
            elif tagged < newest:
                warnings.append((
                    line,
                    f"release {version} is ahead of tag {tag}: v{version} is owed, and until it is "
                    f"pushed pages.yml publishes {dotted(tagged)}",
                ))
    return errors, warnings, f"version {version} against tag {tag or 'none'}"


def main() -> int:
    errors: list[str] = readme_counts()
    permalinks: dict[str, Path] = {}
    bodies: dict[Path, list[tuple[int, str]]] = {}
    anchors: dict[Path, tuple[set[str], list[int]]] = {}

    for page in pages():
        rel = page.relative_to(ROOT).as_posix()
        text = page.read_text(encoding="utf-8").replace("\r\n", "\n")
        front, lines, first = split_front_matter(text)
        if front is None:
            errors.append(f"{rel}: does not open with a front-matter block")
            continue
        match = re.search(r"^permalink\s*:\s*(\S+)", front, re.MULTILINE)
        if match:
            permalinks[normalise(match.group(1))] = page
        status = status_line(rel, lines, first)
        if status:
            errors.append(status)
        prose = prose_lines(lines, first)
        for number, line in prose:
            stray = FRONT_KEY.match(line)
            if stray:
                errors.append(f"{rel}:{number}: front-matter key '{stray.group(1)}:' outside the front-matter block")
        bodies[page] = [(number, INLINE_CODE.sub("", line)) for number, line in prose]
        anchors[page] = heading_ids(prose)

    checked = anchored = 0
    for page, body in bodies.items():
        rel = page.relative_to(ROOT).as_posix()
        for number, line in body:
            read = list(LINK.finditer(line))
            # A link the pattern cannot read must fail, not pass unchecked.
            if line.count("](") > len(read):
                errors.append(
                    f"{rel}:{number}: a link on this line has a target the check cannot read, "
                    "so it would go unchecked; write it as a plain path or as {{ site.baseurl }}/..."
                )
            for match in read:
                target = match.group(1)
                if SCHEME.match(target):
                    continue
                checked += 1
                path, _, fragment = target.partition("#")
                path = path.split("?", 1)[0]
                where = f"{rel}:{number}: link {target!r}"
                # The page the link lands on: this one, for a bare #fragment.
                landing = page
                if BASEURL.match(path):
                    known = permalinks.get(normalise(BASEURL.sub("", path)))
                    if known is None:
                        errors.append(f"{where} names no known permalink")
                        continue
                    landing = known
                elif path.startswith("/"):
                    errors.append(f"{where} is root-absolute; the site serves under a subpath, so use site.baseurl")
                    continue
                elif path:
                    landing = (page.parent / path).resolve()
                    if landing.is_dir():
                        errors.append(f"{where} names a directory, which is not rewritten on the site; link its index.md")
                        continue
                    if not landing.is_file():
                        errors.append(f"{where} resolves to no file")
                        continue
                fragment = unquote(fragment)
                if not fragment:
                    continue
                anchored += 1
                problem = anchor_problem(landing, fragment, anchors)
                if problem:
                    errors.append(f"{where} {problem}")

    agreement, warnings, compared = version_agreement()
    errors += agreement

    for error in errors:
        print(error)
    # Warnings neither fail the check nor count as problems. On GitHub they
    # print as annotations, so they show on the pull request.
    for line, message in warnings:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(f"::warning file=CHANGELOG.md,line={line}::{message}")
        else:
            print(f"warning: CHANGELOG.md:{line}: {message}")
    print(
        f"{len(bodies)} pages, {len(permalinks)} permalinks, {checked} internal links checked, "
        f"{anchored} of them to an anchor, "
        f"{compared}, {len(errors)} problem(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
