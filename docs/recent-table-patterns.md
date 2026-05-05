# Recent Clay Table Patterns

This summarizes a read-only pass over 30 recent Growth Engine X Clay tables. The original local artifacts were compact and redacted; raw manifests and customer-specific destination IDs are intentionally not copied here.

## Corpus Shape

- 30 unique tables.
- 1,294 total fields.
- 717 formula fields.
- 311 action fields.
- 181 text fields.
- 61 date fields.
- 18 source fields.
- 6 number fields.

Common action families:

- Smartlead add/lookup/forward actions
- `http-api-v2`
- `use-ai` and Claygent variants
- `chat-gpt-schema-mapper`
- `filter-list-of-objects`
- lookup/write to other Clay tables
- Slack notifications
- Google Sheets append/update
- HubSpot lookup/create/update
- Mixrank person/company enrichments
- URL and company-name normalizers
- subroutines

## Builder Capabilities To Prioritize

The builder should reliably support:

- base workbooks and scratch tables
- source placeholders, manual columns, formulas, and extracted helper formulas
- action fields with metadata, `inputsBinding`, run guards, custom rates, and reusable account refs
- payload adapters for `http-api-v2`, `use-ai`, schema mapper, Smartlead, Slack, Sheets, HubSpot, Mixrank, normalizers, cross-table operations, and subroutines
- field ID remapping inside formulas, action bindings, run guards, views, table settings, and cross-table refs
- view reconstruction with field order and hidden-column state

Always save without running first, fetch a fresh readback, then run a tiny sample only when validation requires it.

## Reply Forwarding Tables

Common skeleton:

1. Webhook source.
2. Extraction formulas for email, sender, recipient, body, subject, message/stat IDs, campaign fields, category, sentiment, and event time.
3. Body cleanup and forwarded-message formatting.
4. Optional AI/category layer for actionable-positive routing.
5. `http-api-v2` reply forwarding.
6. Slack and/or Google Sheets review actions.

Guard new forwarding actions on required message IDs, campaign fields, destination, positive/category checks, and formatted body.

## Outbound And Smartlead Tables

Recommended build order:

1. raw input identity fields
2. domain/name/LinkedIn normalization helpers
3. person/company enrichment
4. email lookup, cache, waterfall, and validation
5. validation/writeback API columns
6. research/context columns
7. `use-ai` or Claygent copy/research columns
8. output extraction helpers
9. routing formulas and random split logic
10. one Smartlead action per campaign branch
11. export views with implementation columns hidden

Every Smartlead branch should repeat all prerequisites in its own run guard. Do not depend only on an upstream randomizer.

## CRM, API, And Internal Routing

Reusable patterns:

- lookup by validated email or stable object key before update/create
- update only when lookup returns an ID
- create only when lookup is missing
- remove blank values where supported
- gate writes by category, language, destination table, and required normalized fields
- preserve a mapping document for destination table IDs and field IDs

HTTP API columns commonly use POST fanout, GET enrichment, and cache PATCH/POST writeback. Redact body, header, URL, and query formulas recursively.

## Redaction

Secrets often live inside formulas and action inputs, not just obvious header fields. Redact recursively through:

- `inputsBinding[].formulaText`
- `inputsBinding[].formulaMap`
- conditional run formulas
- headers, body, query string, and URL
- table settings and metadata
- AI examples or prompts that contain customer-specific sensitive data

Keep account IDs and destination IDs opaque unless they are required for a live operator handoff.
