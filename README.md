# AutoClayBuilder

[![Live demo](https://img.shields.io/badge/live%20demo-how%20it%20works-ff6a3d?style=flat-square)](https://growthenginenowoslawski.github.io/autoclaybuilder/)
[![Builds Clay tables](https://img.shields.io/badge/builds-Clay%20tables-4338ca?style=flat-square)](docs/build-a-table.md)
[![Plan-mode gated](https://img.shields.io/badge/plan--mode-gated-0f9d58?style=flat-square)](CLAUDE.md)
[![Benchmark parity](https://img.shields.io/badge/calibration%20parity-98.45%25-0f9d58?style=flat-square)](docs/benchmark-2026-05-03.md)
[![CI](https://img.shields.io/github/actions/workflow/status/growthenginenowoslawski/autoclaybuilder/ci.yml?style=flat-square&label=CI)](https://github.com/growthenginenowoslawski/autoclaybuilder/actions/workflows/ci.yml)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776ab?style=flat-square)

**AutoClayBuilder builds Clay tables — correctly, verifiably, the first time.**

> **[▶ See how it works (live visualization)](https://growthenginenowoslawski.github.io/autoclaybuilder/)** — the plan → build → prove workflow, in plain English with a technical-detail toggle.

Describe the table you want (or point at one to learn from). The workflow here
produces an exact, approved build plan, builds it into a safe scratch table, and
proves the result matches the spec field-for-field.

Reverse-engineering an existing table is part of this — but it is the
**calibration** step, not the point. You clone known-good tables to prove the
build payloads are exactly right, then you build new tables with that confidence.

This repository intentionally contains no cookies, bearer tokens, API keys, raw
table manifests, row dumps, sensitive screenshots, webhook URLs, Slack IDs,
Google Sheet IDs, or Smartlead campaign IDs.

## Start here

If you opened this repo in an AI coding agent (Claude Code, etc.), **`CLAUDE.md`
loads automatically and puts the agent into plan mode**: it will not build
anything in Clay until it has written, and you have approved, an exact build
plan. No command to run — the repo self-activates.

Building by hand? Read, in order:

1. [CLAUDE.md](CLAUDE.md) — what this repo does and the plan-before-build rule
2. [docs/build-a-table.md](docs/build-a-table.md) — the forward "how to build a table" guide
3. [plans/TEMPLATE.md](plans/TEMPLATE.md) — the build-plan template every build starts from
4. [docs/autoresearch-clone-loop.md](docs/autoresearch-clone-loop.md) — the calibration harness (how a build is proven correct)

## How it works

1. **Lock the spec** — interview until the goal, source of truth, every column
   and type, and the non-goals are unambiguous.
2. **Read the accumulated knowledge** — patterns and prior `docs/learnings/`
   scars constrain what is actually buildable.
3. **Write the plan** — fill `plans/TEMPLATE.md`; mark every endpoint verified
   vs inferred.
4. **Get explicit approval** — no silent builds, no "I'll start and iterate."
5. **Build into a scratch table** — never mutate the source; save action
   columns without running them.
6. **Calibrate / verify** — fresh API readback, score config parity, loop until
   perfect or an evidence-backed blocker.
7. **Write the learning** — redacted learnings file so the next build inherits
   the scar, not the wound.

## Repo contents

- [CLAUDE.md](CLAUDE.md): auto-loaded plan-mode note for AI agents.
- [AGENTS.md](AGENTS.md): full agent rules — plan-before-build, learnings log, safety.
- [plans/TEMPLATE.md](plans/TEMPLATE.md): the build-plan template.
- [docs/build-a-table.md](docs/build-a-table.md): forward build guide.
- [docs/repo-map.md](docs/repo-map.md): quick map of the repo.
- [docs/autoresearch-clone-loop.md](docs/autoresearch-clone-loop.md): the calibration harness used to prove a build is correct.
- [docs/frontend-api-patterns.md](docs/frontend-api-patterns.md): Clay frontend endpoint and payload rules.
- [docs/browser-automation-patterns.md](docs/browser-automation-patterns.md): browser-use patterns for Clay drawers, formulas, UI verification.
- [docs/recent-table-patterns.md](docs/recent-table-patterns.md): reusable patterns from recent Clay tables.
- [docs/benchmark-2026-05-03.md](docs/benchmark-2026-05-03.md): benchmark run and current blocker.
- [docs/roadmap.md](docs/roadmap.md): path from knowledge base to a usable builder.
- [scripts/redact_clay_manifest.py](scripts/redact_clay_manifest.py): recursive credential redaction.
- [scripts/score_clay_parity.py](scripts/score_clay_parity.py): source-to-target parity scorer.

## Quick start (the calibration tools)

Use Python 3.11+.

```bash
python3 scripts/redact_clay_manifest.py source-manifest.raw.json source-manifest.redacted.json
python3 scripts/score_clay_parity.py source-manifest.redacted.json target-manifest.redacted.json --field-map field-map.json
```

Try the scorer with fake fixtures:

```bash
python3 scripts/score_clay_parity.py \
  examples/fixtures/source-table.example.json \
  examples/fixtures/target-table.example.json \
  --field-map examples/fixtures/field-map.example.json
```

`field-map.json` maps source field IDs to target field IDs:

```json
{
  "f_source": "f_target"
}
```

## Public repo safety

Keep live artifacts out of git unless they are deliberately redacted and
reviewed. The `.gitignore` blocks common Clay run outputs, auth files,
manifests, screenshots, and browser state by default.

## Contributing

External contributors can open pull requests from forks. Only
`growthenginenowoslawski` currently has write/admin access, so only the owner
can merge.
