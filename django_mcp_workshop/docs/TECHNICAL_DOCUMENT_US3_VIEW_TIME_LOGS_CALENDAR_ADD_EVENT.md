# Technical Document: US3 — View Time Logs and Calendar; Add a Calendar Event

**User story (source):** As a user, I want to see my time logs in a list and on a monthly calendar, and to add a new event (name, start/end date and time, description, all-day) via a modal, so that I can see when I logged time and add calendar events.

**Source:** ClickUp task [US3: View time logs and calendar; add a calendar event](https://app.clickup.com/t/86d227tbq) (Epic: Time Tracker (Nexus), Dhruv's Space, workspace 90161493585).

**Requirement reference:** [COMBINED_REQUIREMENT_AND_UI_DOCUMENTATION.md](./COMBINED_REQUIREMENT_AND_UI_DOCUMENTATION.md)  
**Design reference:** [02.1 Time Tracker — Nexus (Figma)](https://www.figma.com/design/4Qf2rnpZ0qrOpR6vilPUQ3/02.1-Time-Tracker---Nexus?node-id=12568-210659&m=dev)

**Rules applied:** No invention of logic, APIs, fields, or validations. Existing UI components only. Missing story input or new components → NEEDS CLARIFICATION.

**Project rules used:** [.cursor/rules/django/](django_mcp_workshop/.cursor/rules/django/) — API response, URL routing, Django development, Django project setup, error handling. Where those rules define backend/API/data conventions, clarifications are resolved below.

---

## Scope Boundary

**In scope (from story + requirement doc only)**

- One screen that shows:
  - **TIME LOG list** (rows: Date, Time Range, Description, Duration) and
  - **Monthly calendar** (month/year label, weekday headers, numeric dates, optional colored event blocks).
- **Calendar navigation:** User can change the displayed month/year via navigation controls.
- **Add event:** Trigger (e.g. "+" on a date where designed) opens a modal with: Event Name, Start Date, End Date, Start Time, End Time, Description, All Day (checkbox); buttons Cancel and Save.
- **Cancel (event modal):** Close modal; no new event created.
- **Save (event modal):** Close modal; new event persisted; **NEEDS CLARIFICATION:** exact outcome and where the event appears on the calendar.
- **Date picker (time log or event form):** When a date field is focused/opened, a date picker opens (month grid, e.g. February 2024); user can select a date and apply it (e.g. Select Date or Apply).

**Out of scope for this document**

- How the user reaches the Time Log / calendar screen (navigation).
- Default view and which data is shown on first load (story marks NEEDS CLARIFICATION).
- Edit Event, Delete Event, event list view columns (Event Name, Project, Category, Date, Time) behavior.
- Task board, filters, search, empty state for events.
- Authentication, authorization, ownership rules, validation rules beyond what is explicitly in the design or story.
- Any API or field not required to support the above.

---

## Frontend Blueprint

**Stack:** React with **MUI** (Material-UI). Date picker and dropdowns: any component that is flexible and MUI-compatible (per US1 technical doc).

**Required UI (from story only)**

| Element | Source | Notes |
|--------|--------|--------|
| Screen | Story + Requirement §3.3 | Time Log screen: list (Date, Time Range, Description, Duration) + monthly calendar; layout per Figma (e.g. calendar left, list right). |
| TIME LOG list | Story AC + Requirement §3.4 | Rows showing Date, Time Range, Description, Duration. |
| Monthly calendar | Story AC + Requirement §3.3 | Month/year label, weekday headers, numeric dates, optional colored event blocks. |
| Calendar navigation | Story AC | Controls to change displayed month/year. |
| "+" (add event) | Story AC + Requirement §3.3 | Shown on a date where designed; triggers event creation modal. |
| Event creation modal | Story AC + Requirement §3.3, §3.4 | Title per design (e.g. "New Event" or as in Figma). Fields: Event Name, Start Date, End Date, Start Time, End Time, Description, All Day (checkbox); Cancel and Save. |
| Cancel button (event) | Story AC | Closes modal; no submit. |
| Save button (event) | Story AC | Submits form; modal closes. |
| Date picker | Story AC + Requirement §3.4 | Month grid (e.g. February 2024); select date and apply (Select Date / Apply or equivalent). |

**Behavior (from story only)**

- On load: Show TIME LOG list and monthly calendar (default view and initial data — NEEDS CLARIFICATION).
- Use calendar navigation to change month/year.
- Click "+" on a date (where shown) → open event creation modal.
- Click Cancel in event modal → close modal, no API call.
- Click Save in event modal → send event data to backend; on success, close modal (exact outcome/where event appears — NEEDS CLARIFICATION).
- Date field (time log or event): open date picker → select date → apply.

**Component choices (clarified)**

- **UI library:** MUI (Material-UI), consistent with US1.
- **Calendar:** FullCalendar or equivalent monthly grid with events (per Requirement §3.2).
- **Date picker / time inputs:** MUI-compatible components (per US1).

---

## Backend Blueprint

**Stack:** Django (existing: `core` app, health/ready views, responses; time-log and calendar/event apps may exist or be added per US1/US3 scope).

**Required behavior (from story only)**

1. **View time logs:** Return a list of time logs so the TIME LOG list and calendar can show when the user logged time (date, time range, description, duration).
2. **View calendar events:** Return events for the calendar (for a given month/range) so the monthly calendar can show colored event blocks.
3. **Add event:** Accept one request with: event name, start date, end date, start time, end time, description, all-day; persist one new calendar event.

**API contract (from project rules — resolved)**

- **URLs (plural resources):** Per [url-routing-rules](django_mcp_workshop/.cursor/rules/django/url-routing-rules.mdc): e.g. `GET /api/time-logs/`, `GET /api/events/`, `POST /api/events/` (or under app-specific prefix). Resource names plural, lowercase.
- **Methods:** GET for list time logs and list events; POST for create event (per RESTful design in django-development-rules).
- **Success response:** Use `core.responses.success_response(data=..., message="...", status_code=201)` for create; 200 for list. Per [api-response-rules](django_mcp_workshop/.cursor/rules/django/api-response-rules.mdc): body shape `{"status": <code>, "message": "...", "data": <payload>}`.
- **Error response:** Use `core.responses.error_response(...)` with optional `errors` and `error_code` (e.g. `VALIDATION_ERROR`, `NOT_FOUND`) per [error-handling-rules](django_mcp_workshop/.cursor/rules/django/error-handling-rules.mdc).
- **View layer:** Class-based view or ViewSet; DRF serializers for validation; business logic in models/managers/services, not in views.

**Endpoints (from story only)**

| Purpose | Method | Endpoint (example) | Notes |
|---------|--------|--------------------|--------|
| List time logs | GET | `/api/time-logs/` | For TIME LOG list and calendar (time log entries). Query params for date range not specified in story — NEEDS CLARIFICATION if required. |
| List events | GET | `/api/events/` | For monthly calendar event blocks. Query params for month/range not specified in story — NEEDS CLARIFICATION if required. |
| Create event | POST | `/api/events/` | Body: name, start_date, end_date, start_time, end_time, description, all_day. |

**Fields to accept for create event (from story only)**

- Event Name (text).
- Start Date, End Date (date values).
- Start Time, End Time (time values; story does not define format or all-day vs time behavior).
- Description (text).
- All Day (boolean).

**Validation (from story only)**

- Story does not define required fields, max lengths, or business rules for events. Without product input, no validation is assumed — list under NEEDS CLARIFICATION.

**Authentication (clarified)**

- **Required:** Yes (consistent with US1). User stored on the event via FK to User (e.g. `user` or `created_by` on Event model).

**Existing backend**

- `core`: `TimeStampedModel` (abstract), health/ready views, exception handler, responses. Time log and event models/APIs as implemented or planned per US1/US3.

---

## Data Schema

**Scope:** Only entities and attributes explicitly required for (1) viewing time logs in a list and on a calendar, and (2) adding one calendar event with the fields above. No extra tables or columns invented.

**From story and requirement doc**

- **Time log:** Already scoped in US1 (date, project, task, time spent, description, billable; list columns Date, Time Range, Description, Duration). Used here for “view” only; no new fields.
- **Calendar event:** Event Name, Start Date, End Date, Start Time, End Time, Description, All Day. Doc does not define storage format for start/end (single datetime vs separate date/time), nor uniqueness/constraints.

**Proposed PostgreSQL-backed schema (minimal, no invention)**

- **Time log:** As in US1 technical doc (no change for US3).
- **Event (new table for calendar events)**  
  - `name`: text (event name).  
  - `user`: FK to User (clarified).  
  - `start_date`: date.  
  - `end_date`: date.  
  - `start_time`: time (nullable if all_day).  
  - `end_time`: time (nullable if all_day).  
  - `description`: text.  
  - `all_day`: boolean.  
  - Inherit timestamps from `TimeStampedModel` if used.

**Not added**

- Unique constraints, indexes, triggers, default values, or validation rules beyond what is stated in the story or requirement doc.

---

## Resolved by project rules (no longer NEEDS CLARIFICATION)

- **API contract:** Endpoints, methods, and response shape from url-routing-rules, api-response-rules, and django-development-rules: e.g. `GET /api/time-logs/`, `GET /api/events/`, `POST /api/events/`, 201 Created for create, `core.responses.success_response` / `error_response`.
- **Response/error format:** Use existing `core.responses` and `core.exceptions.custom_exception_handler`; error codes per error-handling-rules.
- **Timestamps:** Allowed via `TimeStampedModel` per django-development-rules and django-project-setup-rules.

---

## NEEDS CLARIFICATION (for you)

These remain unresolved by the story or project rules. Please confirm so implementation can proceed.

**Product / UX**

1. **Default view and first-load data** — Story: “I see a TIME LOG list and a monthly calendar” with NEEDS CLARIFICATION for default view and which data is shown on first load. Needed to implement initial fetch and default month.
2. **After Save (event)** — Story: “the modal closes” with NEEDS CLARIFICATION for exact outcome and where the event appears on the calendar. Needed to define list/calendar refresh and scroll/position behavior.
3. **List time logs / list events** — Query parameters (e.g. date range, month) for GET time-logs and GET events are not specified. Needed for filtering by visible month/range.
4. **Event validation** — Required fields, max lengths, and rules (e.g. end_date ≥ start_date, all_day vs start/end time) are not defined. Without this, no validation is assumed.

**Frontend**

5. **React app and components** — As in US1: no React app in this repo. Use (a) an existing external app/design system you specify, or (b) new components (approved library)?
6. **Calendar and event components** — Requirement references “FullCalendar (or equivalent)” and event creation modal. No existing components found in repo. Clarify: Which existing components (and from which library or design system) must be used for the monthly calendar and event modal?

**Backend / security**

7. **Authentication** — Assumed required and user stored on event (FK to User), consistent with US1. Confirm if create/list endpoints are authenticated and how user is identified.

**Data**

8. **Event start/end storage** — Story has Start Date, End Date, Start Time, End Time, All Day. Confirm: Store as separate date + time columns, or single start/end datetime with all_day flag? Behavior when all_day is true (ignore time or set to 00:00)?

---

## Summary

| Section | Status |
|---------|--------|
| Scope Boundary | Defined from story + requirement doc only. |
| Frontend Blueprint | Required UI and behavior listed; calendar and event modal depend on component clarification. |
| Backend Blueprint | List time logs, list events, create event; fields and query params as above; validation and auth need clarification. |
| Data Schema | Time log unchanged; Event table proposed with name, user, start/end date/time, description, all_day; storage format for all_day needs clarification. |
| Resolved by project rules | API contract, response format, timestamps. |
| NEEDS CLARIFICATION (you) | 8 items above; please confirm before implementation. |
