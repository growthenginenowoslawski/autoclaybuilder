# Agent Instructions

This repository is a public-safe knowledge base and toolkit for rebuilding Clay tables with frontend APIs and browser automation.

## First Read

Before changing code or docs, read:

1. `README.md`
2. `docs/repo-map.md`
3. `docs/autoresearch-clone-loop.md`
4. the specific doc or script you are editing

## Safety Rules

- Never commit cookies, bearer tokens, API keys, private keys, webhook URLs, Slack webhook URLs, Google Sheet IDs, Smartlead campaign IDs, or raw authenticated Clay manifests.
- Keep endpoint notes as method/path templates, not full secret-bearing URLs.
- Use fake IDs and fake rows in examples.
- Prefer redacted fixtures under `examples/fixtures/`.
- Do not add live screenshots unless they have been reviewed for sensitive content.
- Treat Clay frontend APIs as unstable. Document whether behavior was live-verified, inferred, or copied from a prior note.

## Project Priorities

The useful long-term shape is a small, testable builder library:

1. manifest extraction and redaction
2. field/view/record normalization
3. source-to-target ID remapping
4. parity scoring
5. payload builders for common Clay actions
6. browser automation recipes for UI-only verification

Do not turn the repo into a dump of local run artifacts. Convert learnings into clean docs, small scripts, fake fixtures, or issue-backed tasks.

## Change Style

- Keep docs concise and operational.
- Add tests or fake fixtures when changing scripts.
- Keep scripts runnable with standard Python unless a dependency is clearly justified.
- Preserve public safety over completeness.
- When adding a new Clay endpoint pattern, include:
  - method and path template
  - purpose
  - minimum payload shape
  - readback verification step
  - known failure or normalization behavior

## Verification

Before finishing script changes, run:

```bash
python3 -m py_compile scripts/*.py
```

If fixtures are relevant, run the exact command from `README.md` or `docs/repo-map.md` and include the output summary in the PR.
