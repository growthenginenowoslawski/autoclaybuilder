# Repo Map

Use this file to orient quickly.

## What This Repo Is

AutoClayBuilder collects public-safe Clay table building knowledge and lightweight tooling. It is not a store for live Clay credentials, raw manifests, or customer data.

## Key Files

- `README.md`: project overview and quick start.
- `AGENTS.md`: instructions for AI agents and contributors.
- `CONTRIBUTING.md`: contribution rules and PR expectations.
- `docs/autoresearch-clone-loop.md`: end-to-end scratch-table clone workflow.
- `docs/frontend-api-patterns.md`: observed Clay frontend endpoint and payload patterns.
- `docs/browser-automation-patterns.md`: when and how to use browser automation.
- `docs/recent-table-patterns.md`: reusable workflow families from recent Clay tables.
- `docs/benchmark-2026-05-03.md`: benchmark outcome and blocker summary.
- `docs/roadmap.md`: prioritized backlog for making this a usable builder.
- `scripts/redact_clay_manifest.py`: recursive JSON redaction utility.
- `scripts/score_clay_parity.py`: basic source/target manifest parity scorer.
- `examples/benchmark-program.md`: template for a future clone run.
- `examples/fixtures/`: fake Clay-like JSON fixtures for tests and examples.

## Current Architecture

The repo currently has docs plus two standalone scripts:

```text
Clay table readback JSON
        |
        v
redact_clay_manifest.py
        |
        v
redacted manifest + field map
        |
        v
score_clay_parity.py
        |
        v
score report
```

The next useful step is to factor reusable manifest normalization into a small Python package under `autoclaybuilder/`, then move the scripts onto that package.

## Good First Contribution Areas

- Add fake fixtures that cover formulas, action fields, extracted fields, views, and field groups.
- Improve parity scoring for views and extracted fields.
- Add unit tests around ID remapping and redaction.
- Add payload builders for `http-api-v2`, formula fields, extracted fields, and `use-ai`.
- Add browser automation recipes as docs or small harness scripts, without requiring live credentials.

## What Not To Do

- Do not commit local `~/output/...` run folders.
- Do not add raw `source-manifest.json` or `target-manifest.json` from live work.
- Do not hardcode workspace IDs, auth account IDs, campaign IDs, Slack channels, Google Sheet IDs, or webhook URLs.
- Do not claim an endpoint is stable unless it has a readback verification step.
