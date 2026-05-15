# AutoClayBuilder

**This repo builds Clay tables — correctly, verifiably, the first time.**

You (the AI agent reading this) are the builder. Someone cloned this repo because
they want a Clay table built or improved. The reverse-engineering / clone tooling
here exists to *calibrate* you — it is how this project proves its build payloads
are exactly right. It is the test suite, not the product.

---

## HARD RULE: Plan before you build. No exceptions.

When the user describes a table they want — even a small one, even "just add a
column" — **do not call the Clay API yet.** First enter PLAN MODE and produce a
written build plan they explicitly approve.

Building before an approved plan is the single most common way this goes wrong.
A wrong field type or a missing input binding silently breaks a Clay run with no
error. The plan is what catches that before it costs API credits and trust.

---

## PLAN MODE — the procedure

### 1. Lock the spec
Interview the user until you can state, with zero ambiguity:
- The **goal** of the table (what question it answers, what it outputs)
- The **source of truth** (a reference table URL? a screenshot? a field list? a written outline?)
- The **target shape**: every column, its type, and what feeds it
- **Non-goals** — what this table explicitly should *not* do

If a reference Clay table exists, treat it as the spec and read its real config
(see `docs/autoresearch-clone-loop.md`) rather than guessing.

### 2. Read the accumulated knowledge — do not skip this
- `docs/build-a-table.md` — the forward build guide
- `docs/recent-table-patterns.md` — reusable column/integration patterns
- `docs/frontend-api-patterns.md` — verified Clay endpoints & payload shapes
- `docs/learnings/` — every scar from past builds. These are non-obvious
  failures someone already paid for. Read them before you repeat one.

### 3. Write the plan
Copy `plans/TEMPLATE.md` to `plans/YYYY-MM-DD-<slug>.md` and fill **every**
section. Mark each endpoint you intend to use as **verified** (seen working in
the patterns/learnings docs) or **inferred** (educated guess — higher risk,
call it out explicitly).

### 4. Get explicit approval
Present the plan. Ask for a yes. Do not interpret silence, enthusiasm, or
"looks good" on one section as approval of the whole plan. Wait for an
unambiguous go.

### 5. Build — into a scratch table only
- Never mutate a source/reference table. Build into a fresh scratch workbook.
- Create action columns as full actions up front (Clay won't promote a text
  field into an action later).
- Save action columns **without running them**. Verify `cellCount = 0` so no
  placeholder API calls fire.

### 6. Verify with the calibration loop
Read the scratch table back fresh from the API (a `200 OK` on write does not
mean Clay persisted what you sent — it silently normalizes). Score config
parity against the spec. Loop until parity is perfect or you hit an
evidence-backed blocker (the exact failing step, with proof no other path
bypasses it).

### 7. Write the learning
End every build with a redacted `docs/learnings/YYYY-MM-DD-<slug>.md`: what
worked, what didn't, the mistakes, what the next builder should do differently.
Then *ask* the user before opening a PR — never auto-push.

---

## Safety (always, no flag required)

- **Public-safe repo.** No credentials, real workspace/table IDs, raw manifests,
  or customer data ever get committed. Run `scripts/redact_clay_manifest.py` on
  any captured config *before* it touches disk.
- **Scratch tables only** for builds. The source is read-only.
- **Save-without-run** until the user explicitly approves a live run.

---

## Quick orientation
- `docs/build-a-table.md` — the forward "how to build" guide
- `docs/autoresearch-clone-loop.md` — the calibration harness (how we verify)
- `plans/TEMPLATE.md` — the build-plan template (step 3 above)
- `scripts/score_clay_parity.py` — the parity scorer (step 6)
- `scripts/redact_clay_manifest.py` — secret redaction (safety)
- `AGENTS.md` — full agent rules, plan-before-build, learnings log
