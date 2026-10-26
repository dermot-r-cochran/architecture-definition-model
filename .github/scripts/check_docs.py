"""Source check for the ADM site's Markdown pages (stdlib only).

Four checks, all on the Markdown sources rather than the built site:

1. Every page under docs/ (and CHANGELOG.md) opens with exactly one Jekyll
   front-matter block, and no front-matter key line (layout:, title:,
   permalink:) appears again in the body, which is what a stray fragment
   left by a merge looks like.
2. Every internal link resolves: a `{{ site.baseurl }}/...` link must name a
   permalink some page declares, and a relative link must name an existing
   file (jekyll-relative-links rewrites links to .md files; a link to a bare
   directory is not rewritten and breaks on the published site).
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

External links (http, https, mailto) and in-page anchors are not checked.
Run from anywhere: python .github/scripts/check_docs.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRONT_KEY = re.compile(r"^(layout|title|permalink)\s*:")
INLINE_CODE = re.compile(r"`[^`\n]*`")
LINK = re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
BASEURL = re.compile(r"^\{\{\s*site\.baseurl\s*\}\}")
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)

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


def main() -> int:
    errors: list[str] = readme_counts()
    permalinks: set[str] = set()
    bodies: dict[Path, list[tuple[int, str]]] = {}

    for page in pages():
        rel = page.relative_to(ROOT).as_posix()
        text = page.read_text(encoding="utf-8").replace("\r\n", "\n")
        front, lines, first = split_front_matter(text)
        if front is None:
            errors.append(f"{rel}: does not open with a front-matter block")
            continue
        match = re.search(r"^permalink\s*:\s*(\S+)", front, re.MULTILINE)
        if match:
            permalinks.add(normalise(match.group(1)))
        status = status_line(rel, lines, first)
        if status:
            errors.append(status)
        prose = prose_lines(lines, first)
        for number, line in prose:
            stray = FRONT_KEY.match(line)
            if stray:
                errors.append(f"{rel}:{number}: front-matter key '{stray.group(1)}:' outside the front-matter block")
        bodies[page] = [(number, INLINE_CODE.sub("", line)) for number, line in prose]

    for page, body in bodies.items():
        rel = page.relative_to(ROOT).as_posix()
        for number, line in body:
            for match in LINK.finditer(line):
                target = match.group(1)
                if SCHEME.match(target) or target.startswith("#"):
                    continue
                path = target.split("#", 1)[0].split("?", 1)[0]
                where = f"{rel}:{number}: link {target!r}"
                if BASEURL.match(path):
                    if normalise(BASEURL.sub("", path)) not in permalinks:
                        errors.append(f"{where} names no known permalink")
                    continue
                if path.startswith("/"):
                    errors.append(f"{where} is root-absolute; the site serves under a subpath, so use site.baseurl")
                    continue
                resolved = (page.parent / path).resolve()
                if resolved.is_dir():
                    errors.append(f"{where} names a directory, which is not rewritten on the site; link its index.md")
                elif not resolved.is_file():
                    errors.append(f"{where} resolves to no file")

    for error in errors:
        print(error)
    print(f"{len(bodies)} pages, {len(permalinks)} permalinks, {len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
