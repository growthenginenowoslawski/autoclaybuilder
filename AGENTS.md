# Agent Instructions

This repository **builds Clay tables — correctly, verifiably, the first time.**
The reverse-engineering / parity tooling is the calibration harness that proves
a build is correct; it is the test suite, not the product. `CLAUDE.md` is the
short version of this file and loads automatically — read it first.

## First Read

Before changing code or docs, or building a table, read:

1. `CLAUDE.md`
2. `README.md`
3. `docs/build-a-table.md`
4. `docs/repo-map.md`
5. `docs/autoresearch-clone-loop.md`
6. the specific doc or script you are editing

## Safety Rules

- Never commit cookies, bearer tokens, API keys, private keys, webhook URLs, Slack webhook URLs, Google Sheet IDs, Smartlead campaign IDs, or raw authenticated Clay manifests.
- Keep endpoint notes as method/path templates, not full secret-bearing URLs.
- Use fake IDs and fake rows in examples.
- Prefer redacted fixtures under `examples/fixtures/`.
- Do not add live screenshots unless they have been reviewed for sensitive content.
- Treat Clay frontend APIs as unstable. Document whether behavior was live-verified, inferred, or copied from a prior note.

## Project Priorities

The useful long-term shape is a plan-mode builder backed by a small, testable
library:

1. plan-mode gating (`CLAUDE.md` + `plans/TEMPLATE.md`) — the product
2. manifest extraction and redaction
3. field/view/record normalization
4. source-to-target ID remapping
5. parity scoring (the calibration test suite)
6. payload builders for common Clay actions
7. browser automation recipes for UI-only verification

Do not turn the repo into a dump of local run artifacts. Convert learnings into
clean docs, small scripts, fake fixtures, or issue-backed tasks.

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

## Plan Before Build (Required)

This is the core rule of the repo. If a user gives you an outline of a Clay table
they want built — even a rough one, even "just add a column" — you MUST produce a
written build plan and get explicit approval before creating anything in Clay.
No silent builds. No "I'll start and we can iterate." The user sees the plan
first. The short procedure is in `CLAUDE.md`; the full version follows.

**What "an outline" looks like:**

- A few bullet points describing the table's purpose
- A list of fields they want
- A reference to an existing table to clone
- A screenshot, a doc link, or a verbal description of the workflow
- Any combination of the above

Treat all of these as a trigger to plan.

**Step 1 — Ground the plan in this repo's knowledge.**

Before drafting, read (or re-skim) the docs that constrain what's actually buildable:

- `docs/build-a-table.md` — the forward build pipeline
- `docs/repo-map.md` — what the repo knows how to do
- `docs/recent-table-patterns.md` — reusable patterns from past tables
- `docs/frontend-api-patterns.md` — which Clay endpoints are verified vs inferred
- `docs/browser-automation-patterns.md` — when UI automation is required
- `docs/learnings/` — every prior learnings file (these are the scars; read them)

If the user's outline asks for something a prior `learnings/` file flagged as
broken, unstable, or unverified, call that out in the plan with a link to the
specific learnings file.

**Step 2 — Draft the plan.**

Copy `plans/TEMPLATE.md` to `plans/YYYY-MM-DD-<short-slug>.md` (create the
`plans/` directory if it doesn't exist) and fill every section:

1. **Goal** — one sentence on what the finished table should do.
2. **Source of truth** — what the user gave you (outline, screenshot, existing table ID in redacted form). Quote the user's words where useful.
3. **Target table shape** — proposed name, workbook, field list with types, field groups, views, action columns, and any formulas. Be explicit about each field's purpose.
4. **Field-by-field mapping** (if cloning) — source field -> target field, with type and any normalization. Flag fields you can't map cleanly.
5. **Endpoints and methods you'll use** — call out which are live-verified in `docs/frontend-api-patterns.md` and which are inferred. Inferred endpoints need the user's explicit go-ahead.
6. **Browser automation steps** — anything that has to go through the UI rather than the API, and why.
7. **Known risks / unknowns** — pulled from `docs/learnings/` and your own read of the outline. Be specific: "Clay's formula field POST has been inconsistent — see `docs/learnings/2026-04-12-...md`."
8. **What you will NOT do** — explicit non-goals. Prevents scope creep mid-build.
9. **Verification plan** — how you'll prove the table matches the plan after building (parity score, manual UI check, etc.).
10. **Estimated steps and order** — numbered list of the actual build sequence.

Keep it operational. No filler. A reader should be able to predict every API
call you're about to make.

**Step 3 — Show the plan and ask for approval.**

Surface the plan to the user with a direct question. Examples:

- "I've written `plans/2026-05-11-pe-targets-rebuild.md`. Want to review before I start building?"
- "Plan is at `plans/2026-05-11-icp-signal-table.md`. Two parts I'm least sure about: [X] and [Y]. OK to proceed, or do you want to change anything?"

Do not start building until the user says yes. If they push back on a section,
edit the plan, show the diff, and ask again. The plan is a living document until
approved — once approved, treat it as the contract for the build.

**Step 4 — Reference the plan in the learnings log.**

When you write the post-task learnings file (see "Learnings Log" below), link
back to the plan and note any place the build deviated from it and why. That's
how the next agent learns what plans tend to hold up vs. break under contact
with Clay.

## Verification

Before finishing script changes, run:

```bash
python3 -m py_compile scripts/*.py
```

If fixtures are relevant, run the exact command from `README.md` or
`docs/repo-map.md` and include the output summary in the PR.

## Learnings Log (Required)

Every agent that uses this repo to build or rebuild a Clay table MUST finish the
task by writing a markdown file documenting what it learned and what mistakes it
made along the way. This is how the repo compounds knowledge across runs — your
future-self (and other agents) inherit your scars.

**Where to write it:**

- Path: `docs/learnings/YYYY-MM-DD-<short-slug>.md` (e.g. `docs/learnings/2026-05-11-pe-targets-rebuild.md`)
- Keep it redacted — same safety rules as the rest of the repo (no cookies, tokens, real IDs, etc.)

**What to include:**

1. **Table / task summary** — what Clay table you were building, the source manifest shape (if any), the target Clay workspace shape (in generic terms).
2. **What worked** — endpoints, payload shapes, sequencing, normalization steps that succeeded on the first try.
3. **What didn't work** — every dead end, every misread of a Clay endpoint, every payload that 4xx'd, every assumption that turned out wrong. Include the symptom and the actual root cause.
4. **Mistakes you made** — be specific. "I assumed X but Y was true." Don't sanitize this section.
5. **Recommendations for the next agent** — concrete additions or edits to `docs/`, `scripts/`, or `AGENTS.md` that would have saved you time.
6. **Open questions** — anything you couldn't verify, anything Clay's behavior was ambiguous about, anything that needs a live re-check next time.

**After writing the file:**

Suggest to the user that you open a pull request against this repo with the new
learnings file (and any doc/script edits implied by section 5). Phrase it as a
question, not an action — the user should approve the PR before you run
`gh pr create`. Example: "I've written
`docs/learnings/2026-05-11-pe-targets-rebuild.md`. Want me to open a PR to add
it to the repo?"

Do not create the PR silently. Do not skip the learnings file because the task
"went smoothly" — write the file anyway and say so.
