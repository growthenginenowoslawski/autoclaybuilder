# Clay Frontend API Patterns

These notes come from live Clay table rebuild and scratch-table benchmark work. Treat them as implementation guidance, not official Clay API documentation.

## Core Read Endpoints

```text
GET /v3/tables/:tableId?extraDataViewId=:viewId&includeExtraData=true
GET /v3/tables/:tableId/count
GET /v3/sources?tableId=:tableId
GET /v3/workspaces/:workspaceId/tables/:tableId/fields/runstatus
GET /v3/workspaces/:workspaceId/app-accounts
```

Use the table readback as the authority. Some writes return HTTP 200 while Clay normalizes or rejects parts of the persisted config.

## Scratch Creation

Observed useful paths:

```text
POST /v3/workbooks
POST /v3/tables
POST /v3/tables/:sourceTableId/duplicate/
```

For exact API-visible view parity, `POST /v3/tables` with `template: "no_views"` can create a table with no preconfigured system views. Ordinary table creation may add API-visible preconfigured views that cannot be deleted.

## Field Creation

Use:

```text
POST /v3/tables/:tableId/fields
PATCH /v3/tables/:tableId/fields/:fieldId
DELETE /v3/tables/:tableId/fields/:fieldId
```

Rules observed in benchmark work:

- Create action columns as actions with the full action payload. Do not create a text field and later promote it into an action.
- `PATCH` is useful for same-action updates such as names, run guards, mappings, and settings.
- Clay rejects switching a saved action to a different `actionKey`.
- New field creation ignores supplied source field IDs, so generated field IDs must be mapped.
- Always remap field IDs inside formulas, `inputsBinding`, `inputFieldIds`, extracted fields, conditional-run formulas, view settings, and table settings.

## Views And Ordering

```text
PATCH /v3/tables/:tableId/views/:viewId/fields/:fieldId
```

Sequential moves with `beforeFieldId` or `afterFieldId` are a reliable fallback when bulk field reorder paths fail.

Rebuild visible/hidden state from the API, not just what the UI currently shows. Export views often hide many implementation fields.

## Records

```text
POST /v3/tables/:tableId/records
DELETE /v3/tables/:tableId/records
```

Clay expects direct scalar cell values:

```json
{
  "records": [
    {
      "cells": {
        "f_target": "example value"
      }
    }
  ]
}
```

Do not wrap values as `{ "value": "example" }`; that stores nested values and can cause coercion errors.

## Field Groups

Generic groups can be recreated with:

```text
POST /v3/tables/:tableId/fields/group
POST /v3/tables/:tableId/fields/group/:groupId
```

Map generated group IDs separately. Source `fieldGroupMap` can contain stale field references that are not present in the live `fields[]` array, so score only live refs.

## HTTP API Columns

Clay HTTP API columns use:

```json
{
  "type": "action",
  "typeSettings": {
    "actionKey": "http-api-v2",
    "actionVersion": 1,
    "actionPackageId": "4299091f-3cd3-4d68-b198-0143575f471d"
  }
}
```

Use `inputsBinding[].formulaMap` for headers. Keep placeholder values when the correct key is unavailable, and verify `cellCount = 0` before handoff so placeholders cannot run accidentally.

## Use AI And Claygent

`use-ai` fields require extra care:

- inspect `typeSettings.useCase`, model, prompt, extracted-field wiring, and run guards
- distinguish standard OpenAI prompt columns from Claygent-style generated variants
- fetch a fresh table readback after every write

Benchmark blocker: new/copy-created `use-ai` fields normalized hidden `customRateLimitRules` from a legacy source value of `200/1000ms` to the current workspace default of `5/1000ms`, even after direct field patches returned HTTP 200. The Edit Column drawer exposed model, account, prompt, output, run condition, and delay controls, but no editable custom-rate control.

Treat the readback value as authoritative.
