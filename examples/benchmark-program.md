# Benchmark Program Template

Run tag: `clay-clone-benchmark`

Goal: reverse-engineer the source Clay table and recreate it in scratch table attempts until config parity is perfect or a real blocker is proven.

## Inputs

- Source table URL:
- Workspace ID:
- Table ID:
- View ID:
- Safety row limit: 10

## Canonical Extraction Endpoint

```text
GET /v3/tables/:tableId?extraDataViewId=:viewId&includeExtraData=true
```

## Attempt Paths

- Path A, API-first: configure through Clay frontend APIs, browser only for gaps and verification.
- Path B, browser-first: recreate through Clay UI workflows and verify through API snapshots.
- Path C, duplicate-then-patch: duplicate source table/workbook if available, then patch mismatches.

## Stop Condition

- `perfect_config_parity` in `results.tsv`, with source and target manifests, 100% score report, first 10 rows copied, and browser evidence saved; or
- evidence-backed blocker with exact failing API/UI step, screenshot or browser-state proof, redacted error/request/response, and explanation why no remaining path can bypass it.
