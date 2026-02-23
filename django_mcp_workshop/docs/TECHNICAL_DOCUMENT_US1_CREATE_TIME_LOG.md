# Technical Document: US1 — Create a New Time Log

**User story (source):** As a user, I want to open the New Time Log modal, fill Date, Project, Task, Time Spent, Description, and Billable, and choose Save or Cancel, so that I can log time against a project and task.

**Requirement reference:** [COMBINED_REQUIREMENT_AND_UI_DOCUMENTATION.md](./COMBINED_REQUIREMENT_AND_UI_DOCUMENTATION.md)  
**Design reference:** [02.1 Time Tracker — Nexus (Figma)](https://www.figma.com/design/4Qf2rnpZ0qrOpR6vilPUQ3/02.1-Time-Tracker---Nexus?node-id=12568-210659&m=dev)

**Rules applied:** No invention of logic, APIs, fields, or validations. Existing UI components only. Missing story input or new components → NEEDS CLARIFICATION.

**Project rules used:** [.cursor/rules/django/](django_mcp_workshop/.cursor/rules/django/) — API response, URL routing, Django development, Django project setup, error handling. Where those rules define backend/API/data conventions, clarifications are resolved below.

---

## Scope Boundary

**In scope (from story + requirement doc only)**

- One screen that shows a TIME LOG list and a "New Time Log" button.
- Opening a modal titled "New Time Log" when the user clicks that button.
- Modal contents: Date (with calendar icon), Project (dropdown), Task (dropdown), Time Spent (e.g. 00:00), Description (text area), Billable (checkbox); buttons Cancel and Save.
- Cancel: close modal; no new entry created.
- Save: close modal; new time log persisted; **list refreshes automatically** so the new entry appears (clarified).

**Out of scope for this document**

- How the user reaches the Time Log screen (navigation).
- Edit Time Log, Delete, calendar view, task board, filters, search, empty state.
- Authentication, authorization, ownership rules, validation rules beyond what is explicitly shown in the design.
- Any API or field not required to support the above.

---

## Frontend Blueprint

**Stack:** React with **MUI** (Material-UI). Date picker and dropdowns: any component that is flexible and MUI-compatible (clarified).

**Required UI (from story only)**


| Element          | Source                 | Notes                                                                                                         |
| ---------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------- |
| Screen           | Requirement §3.3       | Time Log screen: list + "New Time Log" button (e.g. top-right).                                               |
| Button           | Requirement §3.4       | Label: "New Time Log".                                                                                        |
| Modal            | Requirement §2.2, §3.3 | Title: "New Time Log". Centered; vertical layout; Cancel and Save at bottom.                                  |
| Date input       | Requirement §3.4       | With calendar icon. Opens date picker (month grid); user selects date and applies (e.g. Select Date / Apply). |
| Project dropdown | Requirement §3.4       | Single selection. Options not defined in doc (e.g. "Project A", "Project B" are examples only).               |
| Task dropdown    | Requirement §3.4       | Single selection. Options not defined in doc.                                                                 |
| Time Spent input | Requirement §3.4       | Example format 00:00. Doc does not specify min/max or step.                                                   |
| Description      | Requirement §3.4       | Text area.                                                                                                    |
| Billable         | Requirement §3.4       | Checkbox.                                                                                                     |
| Cancel button    | Requirement §3.4       | Closes modal; no submit.                                                                                      |
| Save button      | Requirement §3.4       | Submits form; modal closes.                                                                                   |


**Behavior (from story only)**

- Click "New Time Log" → open modal.
- Click Cancel → close modal, no API call.
- Click Save → send data for the six fields to backend; on success, close modal and **refresh the list automatically** so the new entry appears (clarified).

**Component choices (clarified)**

- **UI library:** MUI (Material-UI).
- **Date picker / dropdowns:** Any flexible, MUI-compatible component (e.g. MUI DatePicker, Select, or compatible third-party).

---

## Backend Blueprint

**Stack:** Django (existing: `core` app, health/ready views; no time-log or project/task apps yet).

**Required behavior (from story only)**

- Accept a single request that carries: date, project, task, time spent, description, billable.
- Persist one new time log record.

**API contract (from project rules — resolved)**

- **URL:** Plural resource per [url-routing-rules](django_mcp_workshop/.cursor/rules/django/url-routing-rules.mdc): `POST /api/time-logs/` (or include under app, e.g. `path("api/", include("apps.time_log.urls"))` if using an `api/` prefix). Resource name plural, lowercase.
- **Method:** POST (create) per RESTful design in [django-development-rules](django_mcp_workshop/.cursor/rules/django/django-development-rules.mdc).
- **Success response:** Use `core.responses.success_response(data=..., message="...", status_code=201)`. Per [api-response-rules](django_mcp_workshop/.cursor/rules/django/api-response-rules.mdc): 201 Created for resource created; body shape `{"status": 201, "message": "...", "data": <created resource>}` (matches [core/responses.py](django_mcp_workshop/core/responses.py)).
- **Error response:** Use `core.responses.error_response(...)` with optional `errors` (field-level) and `error_code`. Per [error-handling-rules](django_mcp_workshop/.cursor/rules/django/error-handling-rules.mdc): use specific error codes (e.g. `VALIDATION_ERROR`, `NOT_FOUND`). 400/422 for validation, 404 for missing project/task, etc.
- **View layer:** Class-based view or ViewSet (CreateModelMixin), DRF serializers for validation per [django-development-rules](django_mcp_workshop/.cursor/rules/django/django-development-rules.mdc). Business logic in models/managers/services, not in views.

**Fields to accept (from requirement doc only)**

- Date (date value).
- Project (reference — dropdown implies a chosen project; doc does not define Project model or ID format).
- Task (reference — dropdown implies a chosen task; doc does not define Task model or ID format).
- Time Spent: **HH:MM** format (clarified).
- Description (text).
- Billable (boolean).

**Validation (clarified)**

- **Required fields:** Project, Task, Time spent. Other fields (date, description, billable) per product; serializer enforces required fields.

**Authentication (clarified)**

- **Required:** Yes. User stored on the time log via **FK to User** (e.g. `user` or `created_by` on TimeLog model).

**Existing backend**

- `core`: `TimeStampedModel` (abstract), health/ready views, exception handler, responses. No serializers, no time-log or project/task models.

---

## Data Schema

**Scope:** Only entities and attributes explicitly required for “create one time log” with the six fields above. No extra tables or columns invented.

**From requirement doc**

- Time log has: date, project (choice from dropdown), task (choice from dropdown), time spent, description, billable.
- Doc does not define Project or Task structure (only labels “Project A”, “Project B” as examples).

**Proposed PostgreSQL-backed schema (minimal, no invention)**

- **Time log (single table for the “time log” entity)**  
  - `date`: date (day of the log).  
  - `user`: FK to User (clarified).
  - `project`: FK to Project.  
  - `task`: FK to Task.  
  - `time_spent`: TIME / HH:MM (clarified) — doc shows “00:00”; exact type (interval, integer minutes, etc.) not specified.  
  - `description`: text.  
  - `billable`: boolean.
- **Project:** Admin-managed; existing data may exist. Columns: **name, code, active** (all three; clarified).
- **Task:** Admin-managed; existing data may exist. Columns: **name, code, active** (all three; clarified).

**Not added**

- Unique constraints, indexes, triggers, default values, or validation rules beyond what is stated in the requirement doc.

---

## Resolved by project rules (no longer NEEDS CLARIFICATION)

- **API contract:** Endpoint, method, and response shape from url-routing-rules, api-response-rules, and django-development-rules: `POST /api/time-logs/`, 201 Created, `core.responses.success_response` / `error_response`.
- **Response/error format:** Use existing `core.responses` and `core.exceptions.custom_exception_handler`; error codes per error-handling-rules.
- **Timestamps:** Allowed via `TimeStampedModel` per django-development-rules and django-project-setup-rules.

---

## Resolved clarifications (product)

All 8 items below have been confirmed.

| # | Topic | Decision |
|---|--------|----------|
| 1 | Where the new entry appears after Save | List refreshes automatically. |
| 2 | Project and Task | Admin can create; some existing data exists. |
| 3 | Time Spent format | HH:MM. |
| 4 | Required fields (validation) | Project, Task, time spent. |
| 5 | React / UI library | MUI. |
| 6 | Date picker and dropdowns | Any flexible, MUI-compatible component. |
| 7 | Authentication | Yes; user stored as FK on time log. |
| 8 | Project and Task table columns | All three: name, code, active. |

---

## Summary


| Section | Status |
|---------|--------|
| Scope Boundary | Defined; list refresh on Save clarified. |
| Frontend Blueprint | React + MUI; flexible, MUI-compatible date picker/dropdowns. |
| Backend Blueprint | API contract, required fields (project, task, time_spent), auth (FK to User). |
| Data Schema | Time log (user FK, date, project, task, time_spent HH:MM, description, billable); Project & Task (name, code, active). |
| Resolved by project rules | API contract, response format, timestamps. |
| Resolved clarifications | All 8 product/UX/frontend/backend/data items confirmed. |


