# AutoClayBuilder

AutoClayBuilder is a public-safe collection of patterns, scripts, and benchmark notes for rebuilding Clay tables with Clay frontend APIs plus browser automation.

The goal is practical table cloning and table generation:

- extract a source table through Clay's logged-in frontend API
- redact credentials and destination-specific IDs before saving artifacts
- create scratch workbooks and tables without mutating the source
- rebuild fields, views, formulas, extracted fields, action columns, and row seeds
- use browser automation only for UI-only checks and missing API coverage
- score source-to-target config parity from fresh readbacks

This repository intentionally does not include cookies, bearer tokens, API keys, raw table manifests, row data dumps, screenshots with sensitive UI, webhook URLs, Slack IDs, Google Sheet IDs, or Smartlead campaign IDs.

## Current Contents

- [docs/autoresearch-clone-loop.md](docs/autoresearch-clone-loop.md): the scratch-table clone loop and safety model.
- [docs/frontend-api-patterns.md](docs/frontend-api-patterns.md): Clay frontend endpoint and payload rules found during benchmark work.
- [docs/browser-automation-patterns.md](docs/browser-automation-patterns.md): browser-use patterns for Clay drawers, formulas, and UI verification.
- [docs/recent-table-patterns.md](docs/recent-table-patterns.md): reusable patterns from recent Growth Engine X Clay tables.
- [docs/benchmark-2026-05-03.md](docs/benchmark-2026-05-03.md): summary of the benchmark run and current blocker.
- [scripts/redact_clay_manifest.py](scripts/redact_clay_manifest.py): recursively redacts credential-shaped values from Clay JSON artifacts.
- [scripts/score_clay_parity.py](scripts/score_clay_parity.py): compares source and target table manifests with source-to-target field ID remapping.

## Quick Start

Use Python 3.11+.

```bash
python3 scripts/redact_clay_manifest.py source-manifest.raw.json source-manifest.redacted.json
python3 scripts/score_clay_parity.py source-manifest.redacted.json target-manifest.redacted.json --field-map field-map.json
```

`field-map.json` should map source field IDs to target field IDs:

```json
{
  "f_source": "f_target"
}
```

## Clone Loop

1. Extract the source table with:

   ```text
   GET /v3/tables/:tableId?extraDataViewId=:viewId&includeExtraData=true
   ```

2. Redact the manifest before writing it to disk.
3. Create a scratch workbook/table. Do not mutate the source table.
4. Recreate fields, field groups, views, and the first 10 seed rows.
5. Fetch the target table through the same API.
6. Score parity from the source and target readbacks.
7. Use browser automation for formula validation, edit drawers, menus, run controls, and representative cell inspection.

The first milestone is config parity. Runtime outputs are useful evidence, but they should be logged separately from config parity unless the task explicitly requires output equality.

## Public Repo Safety

Keep live artifacts out of git unless they are deliberately redacted and reviewed. The `.gitignore` blocks common Clay run outputs, auth files, manifests, screenshots, and browser state by default.

## Contributing

External contributors can open pull requests from forks. Only `growthenginenowoslawski` currently has write/admin access to this repository, so only the owner can merge.
