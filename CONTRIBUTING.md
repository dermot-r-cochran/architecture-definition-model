# Contributing to the Architecture Definition Model

Contributions are welcome: corrections, clarifications, examples and proposed decisions.

## Before you start

- For anything beyond a small fix, open an issue first describing the problem and the change you have in mind, so the approach can be agreed before you spend time on it.
- Changes must respect ADM layer discipline and semantic rules. A significant change is proposed as an Architecture Decision Record, not made as an implicit edit.
- Every page opens with its normative-status line. Keep it accurate on a page you change, and give a new page one.
- Permalinks are citations: don't change one.

## Making a change

- Keep a pull request to one change, and say in its description what it changes and why.
- Run what CI runs before you push:

```bash
python .github/scripts/check_docs.py
```

- Record your change under `CHANGELOG.md`'s `[Unreleased]`.
- Every claim the README makes names the check that proves it, or says *no test yet*.

## How a pull request is reviewed

The repository has one maintainer, Dermot Cochran, so a pull request may wait a while before anyone looks at it.

- CI must be green. A failing check is the first thing to fix.
- The review may be assisted by an AI tool, which reads the change and reports to the maintainer. It does not approve or merge anything.
- **Every outside pull request is merged by the maintainer, never by an automated process or an AI tool,** however small.
- A pull request may be declined, or asked to change shape, when it moves the project somewhere it is not meant to go. That is not a judgement on the work.

## Licence

Contributions are accepted under this repository's licences: documentation and explanatory text under CC BY 4.0 (`LICENSE.docs`), example code, configuration and prompt templates under Apache-2.0 (`LICENSE.code`), the same terms everyone else receives them under. No sign-off line and no contributor licence agreement are required. Only contribute work you have the right to license on these terms.

## Security

Please don't describe a security problem in a public issue. Open an issue saying only that you have one, and a private way to send the details will be arranged.
