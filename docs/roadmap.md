# Roadmap

This is the current build plan for turning AutoClayBuilder from a knowledge base into a practical builder.

## Phase 1: Make Artifacts Testable

- Add a fake Clay manifest fixture set with fields, views, field groups, records, action fields, formulas, and extracted fields.
- Add unit tests for recursive redaction.
- Add unit tests for source-to-target field ID remapping.
- Extend parity scoring to report nested diffs instead of only field-level mismatch.
- Add view parity scoring: view names, order, field order, hidden state, filters, sorts, and grouping.

## Phase 2: Normalize Manifests

- Create a small Python package under `autoclaybuilder/`.
- Move redaction and parity code into importable modules.
- Add a normalized manifest schema with:
  - fields
  - views
  - field groups
  - table settings
  - seed records
  - endpoint notes
- Add CLI commands for `redact`, `score`, and `summarize`.

## Phase 3: Payload Builders

Add payload builders for the common Clay column types:

- text/manual fields
- formulas
- extracted fields
- `http-api-v2`
- `use-ai`
- `chat-gpt-schema-mapper`
- Smartlead add/lookup/forward patterns
- Slack notification actions
- Google Sheets append/update actions
- HubSpot lookup/create/update actions
- lookup/write to other Clay tables

Every builder should include a save-without-run path and a readback verification check.

## Phase 4: Browser Verification Recipes

- Document browser-use recipes as deterministic steps.
- Add optional harness scripts for:
  - opening a table with a selected Chrome profile
  - checking auth state
  - capturing safe drawer screenshots
  - validating formula editor save behavior
- Keep browser automation optional and clearly separated from API-only logic.

## Phase 5: End-To-End Scratch Clone

Build a guarded CLI that can:

1. read a redacted or live source manifest
2. create a scratch table
3. recreate safe fields/views/rows
4. save without running action columns
5. fetch target readback
6. score parity
7. write a public-safe run summary

Live mutation support should require explicit flags and should default to scratch-only behavior.
