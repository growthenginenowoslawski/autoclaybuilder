# Repo Map

Use this file to orient quickly.

## What This Repo Is

AutoClayBuilder builds Clay tables — correctly and verifiably — from an approved
plan. The reverse-engineering / parity tooling is the **calibration harness**
that proves a build is correct; it is not the product. The repo holds no live
Clay credentials, raw manifests, or customer data.

## Key Files

- `CLAUDE.md`: auto-loaded plan-mode note — the entry point for any AI agent.
- `README.md`: project overview and start-here path.
- `AGENTS.md`: full agent rules, plan-before-build, learnings log.
- `plans/TEMPLATE.md`: the build-plan template every build starts from.
- `docs/build-a-table.md`: the forward "how to build" guide.
- `docs/autoresearch-clone-loop.md`: the calibration harness (clone & verify).
- `docs/frontend-api-patterns.md`: observed Clay frontend endpoint and payload patterns.
- `docs/browser-automation-patterns.md`: when and how to use browser automation.
- `docs/recent-table-patterns.md`: reusable workflow families from recent Clay tables.
- `docs/benchmark-2026-05-03.md`: benchmark outcome and blocker summary.
- `docs/roadmap.md`: prioritized backlog toward a plan-mode builder.
- `scripts/redact_clay_manifest.py`: recursive JSON redaction utility.
- `scripts/score_clay_parity.py`: source/target manifest parity scorer.
- `examples/benchmark-program.md`: template for a calibration run.
- `examples/fixtures/`: fake Clay-like JSON fixtures for tests and examples.

## Architecture

```text
user spec / reference table
        |
        v
  PLAN MODE  (CLAUDE.md -> plans/TEMPLATE.md -> approval)
        |
        v
  build into scratch table  (save without running)
        |
        v
  fresh API readback
        |
        v
  redact_clay_manifest.py --> score_clay_parity.py --> parity report
        |
        v
  perfect parity  OR  evidence-backed blocker  -->  learnings file
```

The next structural step is factoring reusable manifest normalization and the
payload builders into a `autoclaybuilder/` Python package (see roadmap).

## Good First Contribution Areas

- Add real (redacted) approved plans under `plans/EXAMPLES/` for common archetypes.
- Add fake fixtures covering formulas, action fields, extracted fields, views, field groups.
- Improve parity scoring for views and extracted fields.
- Add unit tests around ID remapping and redaction.
- Add payload builders for `http-api-v2`, formula fields, extracted fields, `use-ai`.
- Add browser automation recipes as docs or small harness scripts, without live credentials.

## What Not To Do

- Do not commit local `~/output/...` run folders.
- Do not add raw `source-manifest.json` or `target-manifest.json` from live work.
- Do not hardcode workspace IDs, auth account IDs, campaign IDs, Slack channels, Google Sheet IDs, or webhook URLs.
- Do not claim an endpoint is stable unless it has a readback verification step.
- Do not build a Clay table without an approved plan.
