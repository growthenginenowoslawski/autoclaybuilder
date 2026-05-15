# Build Plan — <table name>

> Fill every section before building. An empty section is a question you haven't
> answered yet, and unanswered questions are how Clay builds break silently.
> Status: DRAFT -> AWAITING APPROVAL -> APPROVED -> BUILT -> VERIFIED

## 1. Goal
What does this table do? What question does it answer, what does it output, and
who consumes the output? One paragraph, no jargon.

## 2. Source of truth
What is this build measured against?
- [ ] Reference Clay table — URL: `...` (read its real config; don't guess)
- [ ] Screenshot / outline / field list — attached where: `...`
- [ ] Net-new — designed from the goal above

## 3. Target shape
Every column, in order. For each: name, type, what feeds it.

| # | Column | Type | Input / formula / prompt | Notes |
|---|--------|------|--------------------------|-------|
| 1 |        |      |                          |       |

Also specify: views (order, hidden/visible, filters, sorts, grouping),
field groups, and seed rows (first 10, scalar values).

## 4. Field mapping
If cloning/adapting a reference table: the source->target field-ID strategy.
Clay generates new IDs and ignores supplied ones — list every place an ID is
referenced and must be remapped (formulas, inputsBinding, inputFieldIds,
extracted fields, conditional-run formulas, views, cross-table refs).

## 5. Endpoints used
| Step | Endpoint | Verified or Inferred? | Source |
|------|----------|-----------------------|--------|
|      |          |                       | docs/  |

"Inferred" = higher risk. Flag each one explicitly in the approval ask.

## 6. Browser steps
Anything the API can't do or can't confirm (formula editor, integration drawers,
run/batch toggles, disabled states). List the exact UI actions and what each one
verifies.

## 7. Risks from learnings
Read `docs/learnings/`. List every past scar that could bite this build, and how
this plan avoids it (e.g. the use-ai `timeWindow.limit` server-side normalization).

## 8. Non-goals
What this table explicitly will NOT do. Prevents scope creep mid-build.

## 9. Verification plan
How parity is proven: fresh API readback -> `score_clay_parity.py` -> target
score -> 10-row seed check -> which browser evidence closes the remaining gaps.
Define the stop condition: perfect parity, OR a specific evidence-backed blocker.

## 10. Step order
The exact ordered sequence of operations. This is the runbook the build follows.
1.
2.
3.

---
**Approval:** _do not build until the user gives an unambiguous "go" on this whole plan._
