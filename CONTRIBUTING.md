# Contributing

External contributions are welcome through pull requests.

## Rules

- Do not commit credentials, cookies, bearer tokens, API keys, private keys, webhook URLs, or raw authenticated Clay manifests.
- Redact public artifacts with `scripts/redact_clay_manifest.py` before attaching them to a PR.
- Prefer docs, small reproducible scripts, fixtures with fake IDs, and endpoint path templates.
- Keep destructive or billing-affecting Clay operations behind explicit operator confirmation.
- Save without running first when documenting new Clay action creation patterns.

## Pull Requests

Only `growthenginenowoslawski` can merge PRs in this repository. PRs should explain:

- what workflow or endpoint the change covers
- what was verified live versus inferred
- what sensitive artifacts were intentionally excluded
- any remaining blocker or unknown
