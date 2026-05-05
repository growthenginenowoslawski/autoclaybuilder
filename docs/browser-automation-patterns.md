# Browser Automation Patterns

Use browser automation for UI-only behavior and evidence, not as the first choice for every Clay operation.

## When To Use The Browser

Use the browser for:

- formula editor behavior and validation
- integration edit drawers and account/output popovers
- column header menus
- duplicate/edit flows
- run controls, batch toggles, warnings, and disabled states
- representative cell detail panes
- network calls triggered by UI actions that are absent from the saved manifest

Use API readbacks for final truth.

## Harness

In this environment, the working harness was:

```bash
uvx --from 'browser-use[cli]' browser-use
```

Use the real Chrome profile selected by the operator. Profile presence is not proof of live auth; immediately check whether Clay opens the target table or shows an expired-session screen.

## Formula Editing

Stable UI path observed in Clay:

1. Insert or edit the column.
2. Open the drawer.
3. Switch the input type to Formula from the drawer popover.
4. Type into the visible `div role=textbox` instead of mutating raw DOM.
5. Save without running.
6. Fetch the table API readback and compare the saved formula/config.

Direct `innerHTML` replacement and generic formula modals were less reliable than state-index-driven input into the visible editor.

## Action Drawer Inspection

For action, enrichment, HTTP API, Claygent, Use AI, Smartlead, Slack, Sheets, HubSpot, Mixrank, normalizer, subroutine, and write-to-table columns, inspect:

- action key and package/version metadata
- use case, model/provider, prompt, and structured outputs where relevant
- `inputsBinding`, `inputFieldIds`, mapped outputs, and extracted fields
- conditional run formula
- run-as-button, batch mode, rate limits, and delay controls
- reusable account/auth reference by redacted label or opaque ID
- one representative populated cell when available

Do not assume visible helper-column names prove lineage. Confirm source bindings from `fields[].typeSettings.inputsBinding` and `inputFieldIds`.

## Evidence

Capture only the cheapest useful evidence:

- browser state for locator ground truth
- screenshots of menus/drawers without secrets
- endpoint notes with method and path template
- fresh table readbacks after save

Do not screenshot credentials, auth headers, tokens, webhook URLs, or sensitive row data.
