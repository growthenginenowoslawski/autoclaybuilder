# How To Build a Clay Table

This is the forward guide: you have a table you want to *build*, not one you are
reverse-engineering. The clone loop
([docs/autoresearch-clone-loop.md](autoresearch-clone-loop.md)) is the harness
that *proves* a build is correct — this doc is the build itself.

## The one rule

**No build without an approved plan.** See `CLAUDE.md` and the
"Plan Before Build" section of `AGENTS.md`. If you skip the plan, you will ship a
silently-broken table — Clay does not error on a wrong field type or a missing
input binding; it just produces wrong output.

## The build pipeline

### 1. Lock the spec
You cannot build what you cannot state exactly. Pin down:
- **Goal** — the question the table answers and what it outputs.
- **Source of truth** — a reference table (read its real config — don't guess),
  a screenshot, a field list, or a written outline.
- **Target shape** — every column in order: name, type, and what feeds it.
  Plus views, field groups, and the first 10 seed rows.
- **Non-goals** — what it must not do.

Write all of this into `plans/TEMPLATE.md`.

### 2. Resolve every column type
For each column, decide the Clay column type and its payload shape *before*
building. The recurring types and their patterns are in
[docs/recent-table-patterns.md](recent-table-patterns.md):
text/manual, formula, extracted field, `http-api-v2`, `use-ai` (Claygent),
`chat-gpt-schema-mapper`, Smartlead, Slack, Google Sheets, HubSpot, cross-table
lookup, subroutines, normalizers.

Check each endpoint you'll use against
[docs/frontend-api-patterns.md](frontend-api-patterns.md) and mark it **verified**
or **inferred**. Inferred endpoints are the риск you flag to the user.

### 3. Build into a scratch table
- `POST /v3/workbooks` -> `POST /v3/tables` with `template:"no_views"`.
- Create **action columns as full actions up front** — Clay will not promote a
  text field into an action later, and will not change a saved action's
  `actionKey`.
- Clay **generates its own field IDs** and ignores the ones you send. Keep a
  source->target ID map and remap IDs everywhere they appear: formulas,
  `inputsBinding`, `inputFieldIds`, extracted fields, conditional-run formulas,
  views, table settings, cross-table refs.
- Rebuild field groups, then view order / hidden state.
- Seed the first 10 rows with **direct scalar values**.
- **Save action columns without running them.** Verify `cellCount = 0`.

### 4. Prove it (calibration)
Re-fetch the scratch table fresh — a `200 OK` write is not proof Clay persisted
what you sent; it silently normalizes. Score config parity with
`scripts/score_clay_parity.py`. Loop fixes until parity is perfect or you hit an
evidence-backed blocker. Full procedure:
[docs/autoresearch-clone-loop.md](autoresearch-clone-loop.md).

### 5. Capture the learning
Write a redacted `docs/learnings/YYYY-MM-DD-<slug>.md`. The next build should
inherit your scar, not rediscover it. Then *ask* before opening a PR.

## What "done" means

A build is done when one is true:
- **Perfect config parity** proven by source+target manifests, a 100% score, the
  10-row seed check, and browser evidence for UI-only settings; or
- **An evidence-backed blocker** — the exact failing API/UI step, fresh
  readback, redacted request/response, and proof no remaining path bypasses it.

Sample rows running successfully is *not* "done." Config parity is the stricter,
honest bar.
