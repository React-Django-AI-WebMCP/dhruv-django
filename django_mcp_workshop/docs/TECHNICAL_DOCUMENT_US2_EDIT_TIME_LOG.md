# Technical Document: US2 — Edit an Existing Time Log

**User story (source):** As a user, I want to open the Edit Time Log modal with fields pre-filled, change them if needed, and choose Save or Cancel, so that I can correct or update a time log.

**Source:** [ClickUp US2](https://app.clickup.com/90161493585/v/s/90166394427) (task 86d227tab)  
**Requirement reference:** [COMBINED_REQUIREMENT_AND_UI_DOCUMENTATION.md](./COMBINED_REQUIREMENT_AND_UI_DOCUMENTATION.md)  
**Design reference:** Edit Time Log modal — [02.1 Time Tracker — Nexus (Figma)](https://www.figma.com/design/4Qf2rnpZ0qrOpR6vilPUQ3/02.1-Time-Tracker---Nexus?node-id=12568-210659&m=dev)

**Rules applied:** No invention of logic, APIs, fields, or validations. Existing UI components only. Missing story input or new components → NEEDS CLARIFICATION.

**Project rules used:** [.cursor/rules/django/](django_mcp_workshop/.cursor/rules/django/) — API response, URL routing, Django development, Django project setup, error handling.

---

## Scope Boundary

**In scope (from story + requirement doc only)**

- Opening a modal titled **"Edit Time Log"** from an existing time log entry (trigger not specified in doc).
- Modal contents: same fields as New Time Log — Date (with calendar icon), Project (dropdown), Task (dropdown), Time Spent (e.g. 00:00), Description (text area), Billable (checkbox); buttons Cancel and Save; **fields pre-filled** with the selected time log’s data.
- **Cancel:** close modal; no changes saved; no API call.
- **Save:** send updated data for the six fields to the backend; on success, modal closes. Exact outcome and where the updated entry is reflected are not specified in the story (NEEDS CLARIFICATION).

**Out of scope for this document**

- How the user reaches the Time Log screen or how the list/calendar is shown (navigation).
- Create Time Log, Delete Time Log, calendar view, task board, filters, search, empty state.
- Authentication/authorization rules beyond what is already defined for the app; **when** editing is allowed (e.g. roles, time windows) is not specified in the story (NEEDS CLARIFICATION).
- Any API or field not required to support the above.

---

## Frontend Blueprint

**Stack:** React with **MUI** (Material-UI), consistent with US1. Date picker and dropdowns: MUI-compatible components only.

**Required UI (from story only)**


| Element          | Source                 | Notes                                                                                 |
| ---------------- | ---------------------- | ------------------------------------------------------------------------------------- |
| Trigger          | Story / AC             | User “opens” Edit Time Log; exact trigger (e.g. row click, icon, menu) not specified. |
| Modal            | Requirement §2.2, §3.3 | Title: **"Edit Time Log"**. Same layout as New Time Log; fields pre-filled.           |
| Date input       | Requirement §3.4       | With calendar icon; pre-filled with existing time log date.                           |
| Project dropdown | Requirement §3.4       | Single selection; pre-filled with existing project.                                   |
| Task dropdown    | Requirement §3.4       | Single selection; pre-filled with existing task.                                      |
| Time Spent input | Requirement §3.4       | Pre-filled with existing time spent (e.g. 00:00).                                     |
| Description      | Requirement §3.4       | Text area; pre-filled.                                                                |
| Billable         | Requirement §3.4       | Checkbox; pre-filled.                                                                 |
| Cancel button    | Requirement §3.4       | Closes modal; no submit.                                                              |
| Save button      | Requirement §3.4       | Submits updated data; modal closes on success.                                        |


**Behavior (from story only)**

- User opens “Edit Time Log” (trigger TBD) → modal opens with the six fields pre-filled from the selected time log.
- Cancel → close modal, no API call.
- Save → send updated date, project, task, time spent, description, billable to backend for that time log; on success, close modal. Where the updated entry is reflected (e.g. list refresh, same row update) is not specified (NEEDS CLARIFICATION).

**Component choices (no new components)**

- Reuse the same UI as New Time Log (US1): MUI modal, same field types (date picker, dropdowns, time input, text area, checkbox). Only title and initial values differ (“Edit Time Log” + pre-filled). No new component required; if the trigger to open the modal requires a new control (e.g. edit icon, context menu), that control must be one that already exists in the design system or MUST be listed under NEEDS CLARIFICATION.

---

## Backend Blueprint

**Stack:** Django; assumes time-log app and `POST /api/time-logs/` (create) exist per US1.

**Required behavior (from story only)**

- **Read one time log:** Return a single time log by id so the frontend can pre-fill the Edit modal.
- **Update one time log:** Accept updated date, project, task, time spent, description, billable for a given time log id; persist changes.

**API contract (from project rules — resolved)**

- **List/retrieve base:** Plural resource per [url-routing-rules](django_mcp_workshop/.cursor/rules/django/url-routing-rules.mdc): `GET /api/time-logs/` (list), `GET /api/time-logs/{id}/` (retrieve one). Path parameter is the time log id.
- **Update:** `PATCH /api/time-logs/{id}/` (partial update) or `PUT /api/time-logs/{id}/` (full replace) per RESTful design in [django-development-rules](django_mcp_workshop/.cursor/rules/django/django-development-rules.mdc).
- **Success response (retrieve):** `core.responses.success_response(data=<time log>, message="...", status_code=200)`.
- **Success response (update):** `core.responses.success_response(data=<updated time log>, message="...", status_code=200)`.
- **Error response:** `core.responses.error_response(...)` with optional `errors` and `error_code`. Use `NOT_FOUND` for missing time log id; `VALIDATION_ERROR` (or equivalent) for invalid payload; 404 for missing resource, 400/422 for validation per [error-handling-rules](django_mcp_workshop/.cursor/rules/django/error-handling-rules.mdc).
- **View layer:** Class-based view or ViewSet (RetrieveModelMixin, UpdateModelMixin); DRF serializers for validation; business logic in models/managers/services, not in views.

**Fields to accept on update (from requirement doc only — same as create)**

- Date (date value).
- Project (reference; project id).
- Task (reference; task id).
- Time Spent: HH:MM format (per US1).
- Description (text).
- Billable (boolean).

**Validation (no invention)**

- Same validation rules as create (e.g. required: project, task, time spent) unless product clarifies otherwise. No additional validations invented for edit.

**Authentication**

- Same as US1: required; user context used for ownership/authorization if applicable. Story does not define who may edit or when (NEEDS CLARIFICATION).

**Existing backend**

- Assumes `core` and time-log app with create endpoint and TimeLog model exist per US1. Add retrieve and update for the same resource.

---

## Data Schema

**Scope:** No new entities or attributes. Edit uses the same Time Log (and Project/Task) schema as US1.

**From requirement doc**

- Time log has: date, project, task, time spent, description, billable (and user/timestamps per US1). Edit only updates those six fields for an existing row.

**PostgreSQL-backed schema (unchanged from US1)**

- **Time log:** id, user (FK), date, project (FK), task (FK), time_spent, description, billable, created_at, updated_at (or equivalent from TimeStampedModel).
- **Project / Task:** As in US1 (name, code, active). No new columns for edit.

**Not added**

- No new tables, unique constraints, indexes, or validation rules beyond what is already in scope for create/display.

---

## NEEDS CLARIFICATION (for you)

These remain unresolved by the story or requirement doc. Please confirm so implementation can proceed.

**Product / UX**

1. **Trigger to open Edit Time Log** — Story says user “opens” Edit Time Log but does not specify how (e.g. click on list row, edit icon on row, context menu, calendar event click). Needed to implement the correct UI control and behavior.
2. **Outcome after Save** — Story says “modal closes” only. Confirm: does the list refresh automatically, does the same row update in place, or is another behavior expected? Any success message?
3. **When editing is allowed** — Story notes: “When editing is allowed—e.g. roles, time windows.” Confirm: are there restrictions (e.g. only owner, only within 24 hours, only certain roles)? If none, state “no restrictions” so backend/frontend can avoid inventing rules.

**Frontend**

1. **Edit control** — If the trigger requires a specific control (e.g. edit icon, “Edit” link, row click), confirm it exists in the design system or approve the component; otherwise list under NEEDS CLARIFICATION per strict mode.

**Backend / security**

1. **Authorization for edit** — Confirm whether only the time log owner can edit, or if any authenticated user can edit any time log. No invention of rules without confirmation.

---

## Summary


| Section                   | Status                                                                                                     |
| ------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Scope Boundary            | Defined from story + requirement doc only.                                                                 |
| Frontend Blueprint        | Same components as US1; modal title “Edit Time Log”; pre-filled fields.                                    |
| Backend Blueprint         | GET /api/time-logs/{id}/, PATCH (or PUT) /api/time-logs/{id}/; same fields and responses as project rules. |
| Data Schema               | No change from US1; edit updates existing Time Log row only.                                               |
| NEEDS CLARIFICATION (you) | 5 items above; please confirm before implementation.                                                       |


