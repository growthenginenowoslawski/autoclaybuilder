# Roadmap

The path from knowledge base to a builder that produces correct Clay tables on
demand. The clone/parity tooling is the **test suite** that gates every phase —
not a separate deliverable.

## Phase 1: Plan-Mode Builder (the product)

- `CLAUDE.md` + `plans/TEMPLATE.md` make any agent that opens the repo refuse to
  build without an approved plan. (Done — keep tightening.)
- `docs/build-a-table.md` as the canonical forward build guide. (Done.)
- Add a `plans/EXAMPLES/` set: real (redacted) approved plans for the common
  table archetypes, so new builds start from a proven plan, not a blank one.
- Add a `docs/learnings/` index so plan-mode can cite the relevant scar fast.

## Phase 2: Calibration Test Suite

- Fake Clay manifest fixtures: fields, views, field groups, records, action
  fields, formulas, extracted fields.
- Unit tests for recursive redaction.
- Unit tests for source-to-target field ID remapping.
- Parity scoring reports nested diffs, not only field-level mismatch.
- View parity scoring: names, order, field order, hidden state, filters, sorts, grouping.

## Phase 3: Builder Library + CLIs

- Python package under `autoclaybuilder/`.
- Move redaction and parity code into importable modules.
- Normalized manifest schema (fields, views, field groups, table settings, seed
  records, endpoint notes).
- CLI commands: `redact`, `score`, `summarize`, and `plan` (scaffold a build
  plan from a spec or a reference manifest).

## Phase 4: Payload Builders

Payload builders for the common Clay column types, each with a save-without-run
path and a readback verification check:

- text/manual fields
- formulas
- extracted fields
- `http-api-v2`
- `use-ai`
- `chat-gpt-schema-mapper`
- Smartlead add/lookup/forward
- Slack notification actions
- Google Sheets append/update
- HubSpot lookup/create/update
- lookup/write to other Clay tables

## Phase 5: Browser Verification Recipes

- Deterministic browser-use recipes.
- Optional harness scripts: open a table with a selected Chrome profile, check
  auth state, capture safe drawer screenshots, validate formula editor save.
- Browser automation stays optional and clearly separated from API-only logic.

## Phase 6: End-To-End Guarded Builder

A guarded CLI that, from an approved plan: creates a scratch table, recreates
fields/views/rows, saves without running action columns, fetches the target
readback, scores parity, and writes a public-safe run summary. Live mutation
requires explicit flags and defaults to scratch-only.
