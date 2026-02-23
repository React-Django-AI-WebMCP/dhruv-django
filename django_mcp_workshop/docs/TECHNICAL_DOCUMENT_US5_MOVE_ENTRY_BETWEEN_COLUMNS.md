# Technical Document: US5 — Move an Entry Between Columns on the Task Board

**User story (source):** As a user, I want to drag an entry card from one column to another and see which column will receive it, so that I can move entries through stages (e.g. To do, In Progress, Done, Review, Backlog).

**Source:** ClickUp — [US5: Move an entry between columns on the task board](https://app.clickup.com/t/86d227tf5)  
**Requirement reference:** [COMBINED_REQUIREMENT_AND_UI_DOCUMENTATION.md](./COMBINED_REQUIREMENT_AND_UI_DOCUMENTATION.md)  
**Design reference:** Dragging entries through project tasks (task board) — [02.1 Time Tracker — Nexus (Figma)](https://www.figma.com/design/4Qf2rnpZ0qrOpR6vilPUQ3/02.1-Time-Tracker---Nexus?node-id=12568-210659&m=dev)

**Rules applied:** No invention of logic, APIs, fields, or validations. Existing UI components only. Missing story input or new components → NEEDS CLARIFICATION.

**Project rules used:** [.cursor/rules/django/](django_mcp_workshop/.cursor/rules/django/) — API response, URL routing, Django development, error handling. Where those rules define backend/API/data conventions, clarifications are resolved below.

---

## Scope Boundary

**In scope (from story + requirement doc only)**

- One screen: **task board** with vertical columns (e.g. To do, In Progress, Done, Review, Backlog).
- **Entry cards** inside columns; **"+"** at the bottom of each column (behavior of "+" not defined in story — NEEDS CLARIFICATION).
- **Drag:** When the user starts dragging an entry card, a **drag ghost** (or equivalent) follows the pointer.
- **Drop targets:** Columns that can receive the card **highlight** as drop targets during drag.
- **Drop:** When the user releases the card on a valid column, the **card moves** from its original column to the target column.
- No invention of: whether the move updates “status” vs “order” only; confirmation; undo.

**Out of scope for this document**

- How the user reaches the task board (navigation).
- Time Log list, New/Edit Time Log modals, calendar view, event creation, filters, search, empty state, Confirm Deletion.
- Authentication, authorization, ownership, validation rules beyond what is explicit in the story or requirement doc.
- Any API or field not required to support the above.

---

## Frontend Blueprint

**Stack:** React with **MUI** (Material-UI), per project context. Drag-and-drop and board UI: any component that is flexible and MUI-compatible (to be clarified).

**Required UI (from story + requirement doc only)**

| Element            | Source              | Notes                                                                                          |
| ------------------ | ------------------- | ---------------------------------------------------------------------------------------------- |
| Screen             | Story + §3.3        | Task board: vertical columns with entry cards.                                                  |
| Columns            | Story + §3.3, §3.4  | Labels: To do, In Progress, Done, Review, Backlog (per design).                               |
| Entry cards        | Story + §3.3        | Cards inside columns; draggable.                                                                |
| "+" at column foot | Story + §3.3        | Shown in design. Story/requirement doc do not define what "+" does (new entry vs add existing).|
| Drag ghost         | Story AC            | Follows pointer while dragging.                                                                |
| Column highlight   | Story AC + §3.2     | Columns that can receive the card highlight as drop targets during drag.                        |

**Behavior (from story only)**

- On task board load: user sees columns (To do, In Progress, Done, Review, Backlog) with entry cards and "+" at bottom of columns.
- Start drag on an entry card → drag ghost follows pointer; valid columns highlight as drop targets.
- Release on a valid column → card moves from source column to target column.

**Component choices (to be clarified)**

- **UI library:** MUI (Material-UI), per existing project context.
- **Drag-and-drop:** Doc references “Entries as cards; columns as drop targets with visual highlight” (§3.2). No existing component specified. **NEEDS CLARIFICATION:** Which existing drag-and-drop–capable component (and from which library) must be used for cards and columns.

---

## Backend Blueprint

**Stack:** Django (existing: `core` app; no task-board or entry-status APIs assumed).

**Required behavior (from story only)**

- Support the **visible outcome** of the move: after drop, the card appears in the target column. The story and requirement doc do **not** define whether this is a **status** change, an **order** change, or both; nor do they define the backend contract.

**API contract (conditional — only if move is persisted)**

- If product clarifies that “move” **persists** (e.g. status or order stored in backend):
  - **URL:** Plural resource per [url-routing-rules](django_mcp_workshop/.cursor/rules/django/url-routing-rules.mdc): e.g. `PATCH /api/entries/{id}/` or `PATCH /api/time-logs/{id}/` (or equivalent for the entity that represents the “entry” on the board). Resource name and path must match the chosen data model; no invention.
  - **Method:** PATCH (partial update) per RESTful design in [django-development-rules](django_mcp_workshop/.cursor/rules/django/django-development-rules.mdc).
  - **Success response:** Use `core.responses.success_response(data=..., message="...", status_code=200)`; body shape `{"status": 200, "message": "...", "data": <updated resource>}`.
  - **Error response:** Use `core.responses.error_response(...)` with optional `errors` and `error_code` (e.g. `VALIDATION_ERROR`, `NOT_FOUND`).
- If product clarifies that the move is **client-only** (e.g. reorder in memory, no persistence), no new backend endpoint is required for this story.

**Fields to accept (only if an update endpoint exists)**

- Only fields **explicitly** required to support “card moves to target column” (e.g. a status or column identifier, or order index)—to be defined when “status vs order” and the data model are clarified. **No invention** of field names or payload shape.

**Existing backend**

- `core`: `TimeStampedModel`, health/ready views, exception handler, responses. No task-board or entry-status API is assumed.

---

## Data Schema

**Scope:** Only entities and attributes **explicitly** required for “move an entry between columns” as described in the story. No extra tables or columns invented.

**From requirement doc**

- Task board has columns (To do, In Progress, Done, Review, Backlog) and entry cards.
- Doc does **not** define: what an “entry” is (time log, event, or separate card entity); whether it has a status/column field; whether order is stored; or the list of allowed status/column values.

**Proposed PostgreSQL-backed schema (minimal — only if product confirms)**

- **If “entry” is an existing entity (e.g. time log or event):** Add only a **status** or **column** field (or equivalent) **if** product confirms that moving the card updates that field. Type and allowed values (e.g. To do, In Progress, Done, Review, Backlog) to match product; no invention.
- **If “entry” is a new entity:** Do **not** add tables or columns until product defines the entity and its fields. **STOP — NEEDS CLARIFICATION.**

**Not added**

- Unique constraints, indexes, triggers, default values, or validation rules beyond what is stated in the requirement doc or clarified by product.

---

## NEEDS CLARIFICATION

These remain unresolved by the story or requirement doc. Implementation must **STOP** or avoid inventing until the following are confirmed.

**Product / UX**

1. **What “+” at the bottom of a column does** — New entry vs add existing entry. Required to implement or disable "+" correctly.
2. **Whether the move changes status, order, or both** — Required to define backend API and data schema (e.g. status field, order field, or none if client-only).
3. **What happens after drop** — Persisted (API + DB) vs client-only reorder. If persisted, which entity (time log, event, other) and which field(s) are updated.
4. **Confirmation or undo** — Story notes “NEEDS CLARIFICATION: Whether this changes status or only order; any confirmation or undo.” Required for UX and any backend side effects.

**Frontend**

5. **Existing drag-and-drop component** — Requirement doc (§3.2) mentions “Entries as cards; columns as drop targets with visual highlight” but does not map to an existing library or component. No existing task board or drag-and-drop component was identified in the repo. **If a new component is required, STOP and list here:** NEEDS CLARIFICATION — which approved library/component (e.g. MUI + dnd-kit, react-beautiful-dnd, or other) must be used for cards and columns?
6. **Mapping to design system** — Requirement doc (§3.6): “Map Figma elements to existing design system components.” Which existing components represent: (a) a column container, (b) an entry card, (c) drag ghost, (d) drop-target highlight?

**Backend / data**

7. **Identity of “entry”** — Is the draggable card a time log, a calendar event, or another entity? Required for URL, API, and schema.
8. **Allowed column/status values** — Are the labels (To do, In Progress, Done, Review, Backlog) the exact list of allowed values, and who defines them (config, DB, frontend only)?

---

## Summary

| Section                   | Status                                                                                       |
| ------------------------- | -------------------------------------------------------------------------------------------- |
| Scope Boundary            | Defined from story + requirement doc only.                                                   |
| Frontend Blueprint         | Required UI and behavior listed; drag-and-drop and board components not mapped to codebase. |
| Backend Blueprint          | Conditional on “status vs order” and “persist vs client-only”; no API invented.              |
| Data Schema                | No schema proposed until “entry” entity and status/order semantics are clarified.           |
| NEEDS CLARIFICATION (you)  | 8 items above; confirm before implementation.                                                |
