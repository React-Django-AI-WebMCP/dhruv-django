# Technical Document: US4 — Filter and Search Events/Entries

**User story (source):** As a user, I want to filter by project (and optionally category) and use the search/filter bar, so that I see only the events or entries I care about.

**Requirement reference:** [COMBINED_REQUIREMENT_AND_UI_DOCUMENTATION.md](./COMBINED_REQUIREMENT_AND_UI_DOCUMENTATION.md)  
**Design reference:** [02.1 Time Tracker — Nexus (Figma)](https://www.figma.com/design/4Qf2rnpZ0qrOpR6vilPUQ3/02.1-Time-Tracker---Nexus?node-id=12568-210659&m=dev)  
**ClickUp:** [US4: Filter and search events/entries](https://app.clickup.com/t/86d227td3) (Workspace: React Django AI powered development / Dhruv's Space)

**Rules applied:** No invention of logic, APIs, fields, or validations. Existing UI components only. Missing story input or new components → NEEDS CLARIFICATION.

**Project rules used:** [.cursor/rules/django/](django_mcp_workshop/.cursor/rules/django/) — API response, URL routing, Django development, error handling. Where those rules define backend/API/data conventions, clarifications are resolved below.

---

## Scope Boundary

**In scope (from story + requirement doc only)**

- A view that shows events or time log entries.
- **Project filter:** Dropdown that opens to show options such as "All Projects", "Project A", "Project B" (per doc); selecting an option updates displayed events/entries to match (only that project or all).
- **Calendar Query / filter bar:** Visible bar with "Search Events", "Filter by Project", "Filter by Category"; using these controls changes the displayed events according to the applied filters.
- **List view of events:** When shown, columns include Event Name, Project, Category, Date, Time (as in design).

**Out of scope for this document**

- How the user reaches the view (navigation).
- Create/Edit Time Log, Create/Edit Event, task board, drag-and-drop, delete, empty state behavior.
- Authentication, authorization, ownership rules, or validation rules beyond what is explicitly in the story or requirement doc.
- Any API or field not required to support the above.

---

## Frontend Blueprint

**Stack:** React with **MUI** (Material-UI), per existing project convention (see US1 technical doc).

**Required UI (from story + requirement doc only)**

| Element | Source | Notes |
| -------- | ------ | ----- |
| View showing events or entries | Story, Requirement §2.2, §3.3 | Context where filter and list apply (calendar view and/or list view). |
| Project filter dropdown | Story, Requirement §2.2, §3.4 | Options: "All Projects", "Project A", "Project B" (per doc). Opening and selecting updates displayed events/entries. |
| Filter bar (Calendar Query) | Requirement §2.2, §3.3, §3.4 | Contains: Search Events, Filter by Project, Filter by Category. Applying filters changes displayed events. |
| List view (events) | Story, Requirement §2.2, §3.3, §3.4 | Columns: Event Name, Project, Category, Date, Time. Shown when list view is shown (doc does not define when list view is visible). |

**Behavior (from story only)**

- Open project filter → see options (All Projects, Project A, Project B).
- Select project option → displayed events/entries update to match selection.
- Use Search Events / Filter by Project / Filter by Category on the filter bar → displayed events change according to applied filters.
- When list view is shown → user sees columns Event Name, Project, Category, Date, Time.

**Component choices (clarified)**

- **UI library:** MUI (Material-UI), consistent with US1.
- **Dropdown / filter bar / list:** Use existing MUI-compatible components (e.g. Select, TextField for search, or equivalent from existing design system). No new component types invented; if a new component is required, STOP and list under NEEDS CLARIFICATION.

---

## Backend Blueprint

**Stack:** Django (existing: `core` app; time-logs and events endpoints may exist from US1/US3 — this doc does not invent them).

**Required behavior (from story only)**

- Support filtering of events and/or time log entries by **project** (and optionally **category** per story).
- Support **search/filter bar** behavior so the frontend can request filtered data (search and filter by project/category).

**API contract (from project rules — resolved)**

- **URLs:** Plural resources per [url-routing-rules](django_mcp_workshop/.cursor/rules/django/url-routing-rules.mdc). Filtering and search via **query parameters** on list endpoints (e.g. `GET /api/time-logs/`, `GET /api/events/` or equivalent), not new endpoints. Exact path and param names must match what the existing list endpoints for time-logs and events expose; this doc does not invent query parameter names. If no list endpoints exist yet, define only that list endpoints will accept query params for project (and category if clarified).
- **Method:** GET for list + query params.
- **Success response:** Use `core.responses.success_response(data=..., message="...", status_code=200)` per [api-response-rules](django_mcp_workshop/.cursor/rules/django/api-response-rules.mdc). Body shape `{"status": 200, "message": "...", "data": <list/paginated result>}`.
- **Error response:** Use `core.responses.error_response(...)` with optional `errors` and `error_code` per [error-handling-rules](django_mcp_workshop/.cursor/rules/django/error-handling-rules.mdc).
- **View layer:** Class-based view or ViewSet (ListModelMixin); filter/search logic via query params; business logic in models/managers/services, not in views.

**Fields used for filtering (from requirement doc only)**

- **Project:** Referenced by dropdown selection (e.g. "Project A", "Project B"); implies project identifier (e.g. ID) used in filter.
- **Category:** Referenced in "Filter by Category" and list column "Category"; requirement doc does not define Category on time log or event entities → **NEEDS CLARIFICATION** (see below).
- **Search:** "Search Events" implies a search input; doc does not define which fields are searched (event name, description, etc.) → **NEEDS CLARIFICATION** (see below).

**No invention**

- No new endpoints, new field names, or new validation rules beyond what the story and requirement doc state. Backend only supports the filtering and search behavior that the frontend needs to satisfy the acceptance criteria.

---

## Data Schema

**Scope:** Only entities and attributes already required for time logs and events (from prior docs) and those **explicitly** referenced by US4. No new tables or columns invented.

**From requirement doc + story**

- **Time log entries** and **events** are the data being filtered and shown in list view.
- **Project** is a filter dimension; project options (e.g. "All Projects", "Project A", "Project B") imply a Project entity or list; schema for Project is defined in US1 technical doc (name, code, active).
- **Category** appears in the UI (Filter by Category, list column "Category"). The requirement doc does **not** define a Category entity or a category field on TimeLog or Event. **No schema change for Category is proposed** until clarified.

**Proposed PostgreSQL-backed schema (minimal, no invention)**

- **Time log:** As in US1 — date, user, project (FK to Project), task (FK to Task), time_spent, description, billable. No category field unless clarified.
- **Event:** As implied by requirement doc (US3) — name, start/end date and time, description, all-day; link to project if events are filtered by project. No category field unless clarified.
- **Project:** As in US1 — name, code, active (admin-managed).
- **Category:** Not added. If product requires "Filter by Category" and "Category" column, define Category entity and/or category FK on Event/TimeLog in a clarification; then add to schema.

**Not added**

- New tables, new columns, unique constraints, indexes, or validation rules beyond what is stated in the requirement doc or prior technical docs.

---

## NEEDS CLARIFICATION (for you)

These remain unresolved by the story or requirement doc. Please confirm so implementation can proceed.

**Product / UX**

1. **Search vs filter behavior** — Story and doc state that using "Search Events", "Filter by Project", and "Filter by Category" changes displayed events, but: *"NEEDS CLARIFICATION: Exact behavior of search vs filter and when list view is shown."* Until clarified, technical design cannot define whether search is free-text, which fields are searched, or when list view is visible vs calendar-only.
2. **Category** — "Filter by Category" and list column "Category" are in the design; the requirement doc does not define what Category is (entity, field on Event/TimeLog, or dropdown source). Clarify: Does Category exist as a model? Which resources (events, time logs, or both) have a category? What are the category options?
3. **Scope of filtering** — Confirm whether filters apply to (a) calendar events only, (b) time log entries only, (c) both, and whether one shared filter bar drives both or separate filters per view.
4. **List view visibility** — When is the events list view (Event Name, Project, Category, Date, Time) shown? Always beside calendar, only when switching view, or only when a filter is applied?

**Frontend**

5. **Existing components** — Confirm which existing MUI (or design system) components must be used for: project dropdown, "Search Events" input, "Filter by Project" / "Filter by Category" controls, and the events list table. If any new component is required, list it here and STOP.

**Backend**

6. **Query parameters** — Once Category and search behavior are clarified, confirm exact query parameter names for list endpoints (e.g. `project`, `category`, `search`) and which fields search applies to (event name, description, etc.).
7. **Events and time logs list endpoints** — If US1/US3 have not yet defined list endpoints for time-logs and events, confirm that list endpoints will support filter (and optional search) via query params as above.

**Data**

8. **Category schema** — If Category is required: add a Category model and/or category FK on Event and/or TimeLog; define columns and option source (admin, fixed list, etc.).

---

## Summary

| Section | Status |
| ------- | ------ |
| Scope Boundary | Defined from story + requirement doc only. |
| Frontend Blueprint | Required UI and behavior listed; components must be existing MUI/compatible. |
| Backend Blueprint | Filter/search via GET list + query params; no new endpoints; Category/search behavior not defined. |
| Data Schema | No new tables/columns; Category not added until clarified. |
| NEEDS CLARIFICATION (you) | 8 items above; please confirm before implementation. |
