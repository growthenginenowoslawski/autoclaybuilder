# The Calibration Loop (Clone & Verify)

This loop is how AutoClayBuilder **proves a build is correct**. You recreate a
known table in a scratch table and score config parity until it is perfect or a
real blocker is proven. It is the test harness behind
[docs/build-a-table.md](build-a-table.md) — clone a table you already trust to
calibrate the build payloads, then build new tables with that confidence.

It is also the verification step (step 6) of every build: read the result back
fresh and score it against the spec.

## Safety Rules

- Do not mutate the source/reference table.
- Use scratch workbooks and scratch tables for every attempt.
- Copy only the first 10 source rows unless the operator explicitly raises the limit.
- Save columns without running them first where possible.
- Run external or integration columns only on the scratch sample rows when validation requires it.
- Redact cookies, bearer tokens, API keys, passwords, webhook URLs, auth headers, and credential-like values before writing artifacts.

## Source Manifest

Extract the reference table through the logged-in Clay frontend API:

```text
GET /v3/tables/:tableId?extraDataViewId=:viewId&includeExtraData=true
```

The redacted manifest should preserve:

- workspace/table/view identifiers
- ordered fields
- field names, types, formulas, extracted-field parents, and action metadata
- `typeSettings.inputsBinding`, `inputFieldIds`, conditional run formulas, batch settings, and rate limits
- view order, field order, hidden/visible state, filters, sorts, and grouping
- first 10 seed values needed to recreate input rows
- endpoint notes with method and path template
- unknowns that require UI inspection

## Attempt Paths

Run attempts as separate folders with clear status:

- `api-first`: configure as much as possible through frontend APIs; browser automation only for missing endpoints and verification.
- `browser-first`: recreate through Clay UI workflows, then verify by fetching the API manifest.
- `duplicate-then-patch`: use Clay's duplicate path when allowed, then patch and compare mismatches.
- `from-scratch-api-browser`: API-created scratch base, then browser automation for columns or settings the API cannot reproduce.

## Parity Scoring

Score against fresh source and target readbacks from the same endpoint. Compare:

- field count, order, names, types, formulas, extracted-field config, action metadata, bindings, guards, batch settings, and reusable auth/account references
- view count, names, order, field order, hidden-column state, filters, sorts, and grouping
- first 10 seed rows
- UI evidence for edit drawers, formulas, column menus, run controls, and representative cell inspection

Runtime output equality is separate evidence. A config-perfect scratch table can
still need runtime logging if external APIs are async, permissioned, or rate
limited.

## Run Log Format

Use one append-only row per attempt:

```tsv
timestamp	run_tag	sprint	attempt	path	target_table_url	parity_score	status	notes
2026-05-03T18:00:00Z	clay-clone-benchmark	1	attempt-001	api-first	https://app.clay.com/...	0.82	partial	missing action payload fields
```

Recommended statuses:

- `perfect_config_parity`
- `partial`
- `blocked`
- `failed`
- `abandoned_by_better_path`

## Stop Conditions

Stop when one of these is true:

- perfect config parity is proven by source/target manifests, score report, row seed check, and browser evidence
- a blocker is proven with an exact failing API/UI step, fresh readback, redacted request/response or screenshot, and evidence that the remaining known paths cannot bypass it
