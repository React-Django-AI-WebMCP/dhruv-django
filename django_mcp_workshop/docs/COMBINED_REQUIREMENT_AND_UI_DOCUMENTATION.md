# COMBINED REQUIREMENT & UI DOCUMENTATION

**Design source (reference):** [02.1 Time Tracker — Nexus — Figma](https://www.figma.com/design/4Qf2rnpZ0qrOpR6vilPUQ3/02.1-Time-Tracker---Nexus?node-id=12568-210659&m=dev)

This document strictly reflects the above Figma source. Any behavior or UI not visible or inferable from this source is flagged under **NEED CLARIFICATION**.

---

## 1. Overview

- **What:** Time Tracker (Nexus) — a module for logging time, viewing entries on a calendar, and moving entries through project task stages.
- **Purpose (user):** Users can create and edit time logs (date, project, task, time spent, description, billable); view time logs in a list and on a calendar; create and edit calendar events (name, start/end date and time, all-day, description); filter by project (and possibly category); move entries between columns (e.g. To do, In Progress, Done, Review, Backlog); and use date/time selection and confirmations where shown.
- **Language:** Plain language only; no technical or implementation detail.

---

## 2. Functional Requirements (WHAT the System Must Do)

### 2.1 Entry Behavior

- **How the user reaches the screen(s):** Not specified in the Figma — **NEED CLARIFICATION**.
- **First load:** Time Log list is visible (date, time range, description, duration) with a "New Time Log" button; calendar shows a month (e.g. January 2024) with navigation; task board shows columns (To do, In Progress, Done, Review, Backlog) with entry cards. **NEED CLARIFICATION:** Default view (list vs calendar vs board), default date/month, and which data is shown on first load.

### 2.2 Core User Actions


| User action                         | System response (user-visible)                                                                                                                                                                                                                                |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Click "New Time Log"                | Modal "New Time Log" opens with fields: Date, Project, Task, Time Spent (00:00), Description, Billable; Cancel and Save.                                                                                                                                      |
| Click Save in New Time Log          | Modal closes; new entry appears in list/calendar (assumed). **NEED CLARIFICATION:** Exact outcome and where it appears.                                                                                                                                       |
| Click Cancel in New Time Log        | Modal closes; no new entry.                                                                                                                                                                                                                                   |
| Open "Edit Time Log"                | Modal "Edit Time Log" opens with same fields pre-filled; Cancel and Save.                                                                                                                                                                                     |
| Save in Edit Time Log               | Modal closes; updated entry reflected (assumed). **NEED CLARIFICATION:** Exact outcome.                                                                                                                                                                       |
| Open date field (Time Log or Event) | Date picker opens (e.g. February 2024 grid); user can select date; "Select Date" or "Apply" (or equivalent) applies choice.                                                                                                                                   |
| Add event (e.g. "+" on calendar)    | Event creation modal opens: Event Name, Start Date, End Date, Start Time, End Time, Description, All Day; Cancel and Save.                                                                                                                                    |
| Save event                          | Modal closes; event appears on calendar (assumed). **NEED CLARIFICATION:** Exact outcome.                                                                                                                                                                     |
| Filter by project                   | Dropdown (e.g. "All Projects", "Project A", "Project B"); selection changes which events/entries are shown on calendar.                                                                                                                                       |
| Search/filter (Calendar Query)      | "Search Events", "Filter by Project", "Filter by Category" bar; applying filters changes displayed events; list view can show Event Name, Project, Category, Date, Time. **NEED CLARIFICATION:** Exact behavior of search vs filter and list view visibility. |
| Drag entry card to another column   | Card moves from source column to target column; columns may highlight as drop targets during drag. **NEED CLARIFICATION:** Whether this changes "status" or only reorders; any confirmation.                                                                  |
| Add entry to column                 | "+" at bottom of column (shown in design). **NEED CLARIFICATION:** Whether this creates a new entry or adds existing one.                                                                                                                                     |
| Confirm deletion                    | "Confirm Deletion" dialog: "Are you sure you want to delete this item?" with confirm/cancel. **NEED CLARIFICATION:** What is deleted (time log, event, or task card) and from where it's triggered.                                                           |
| Empty state                         | "No items found." with "Add New" button. **NEED CLARIFICATION:** Which screen(s) show this and what "Add New" does.                                                                                                                                           |


### 2.3 Ownership Rules

- Not specified in Figma. **NEED CLARIFICATION:** Who owns created time logs/events/entries; how ownership affects visibility and actions.

### 2.4 Edit Rules

- **What:** Time log fields (date, project, task, time spent, description, billable); event fields (name, start/end date and time, description, all-day).
- **When:** Edit modals are shown in design; exact conditions (e.g. who can edit, time limits) not specified. **NEED CLARIFICATION.**
- **Result:** User sees "Edit Time Log" or "Edit Event" modal; after Save, modal closes (visible outcome only).

### 2.5 Delete Rules

- **What:** Design shows "Confirm Deletion" and "Are you sure you want to delete this item?" — object type not specified. **NEED CLARIFICATION.**
- **Confirmation:** Yes — confirmation dialog shown.
- **After deletion:** Not shown. **NEED CLARIFICATION.**

### 2.6 Conversion Rules

- Not shown (e.g. no Draft → Final, or status transitions). **NEED CLARIFICATION** if any conversions are required.

### 2.7 Visibility Rules

- Not specified (who sees which projects, tasks, or entries). **NEED CLARIFICATION.**

### 2.8 Constraints and Limitations

- Only what is explicit in the design: date picker shows one month; time shown as 00:00 in Time Spent; filter options include "All Projects", "Project A", "Project B". No other constraints assumed.

---

## 3. UI Documentation — Visual and Interaction

### 3.1 Screen Identification

- **Figma node name:** Section (multiple frames under one section).
- **Figma node ID:** 12568-210659.
- **Frames covered:** "Dragging entries through project tasks" (task board); "Calendar flow I v.0.3" (time log list, new/edit time log modals, calendar monthly view, event creation, overlapping events, project/task filter, calendar query, entry with unfilled details, edit modals, monthly calendar variations); plus isolated date pickers, dropdowns, time input, confirmation dialogs, empty state.

### 3.2 UI Behavior References (Visual Only)

- **Calendar UI:** FullCalendar (or equivalent monthly grid with events).
- **Date selection:** React DatePicker (or equivalent month grid with navigation and date selection).
- **Time input:** Numeric/time selector (e.g. 00:00).
- **Drag and drop:** Entries as cards; columns as drop targets with visual highlight.

### 3.3 Layout Description

- **Time Log screen:** Left — monthly calendar (e.g. January 2024, day 15 highlighted); top-right — "New Time Log" button; right — "TIME LOG" list (rows: Date, Time Range, Description, Duration).
- **New/Edit Time Log modal:** Centered modal; title "New Time Log" or "Edit Time Log"; fields in vertical layout; Cancel and Save at bottom.
- **Calendar (monthly):** Full month grid; some cells show colored block events; navigation for month/year; "+" for add on some dates; optional list view below with columns (Event Name, Project, Category, Date, Time).
- **Task board:** Vertical columns (To do, In Progress, Done, Review, Backlog); entry cards inside columns; "+" at bottom of columns; drag ghost and column highlight when dragging.
- **Event creation modal:** Event Name, Start/End Date, Start/End Time, Description, All Day; Cancel and Save.
- **Filter bar (Calendar Query):** Search Events, Filter by Project, Filter by Category.
- **Confirmation dialog:** Title "Confirm Deletion"; body "Are you sure you want to delete this item?"; confirm/cancel actions.
- **Empty state:** "No items found." and "Add New" button.

### 3.4 Visible UI Elements (From Figma Only)

- **Copy:** "TIME LOG", "New Time Log", "Edit Time Log", "Date", "Project", "Task", "Time Spent", "Description", "Billable", "Cancel", "Save", "01/15/2024", "09:00 - 10:00", "Project A - Task B", "01:00", "Event Name", "Start Date", "End Date", "Start Time", "End Time", "All Day", "To do", "In Progress", "Done", "Review", "Backlog", "Search Events", "Filter by Project", "Filter by Category", "All Projects", "Project A", "Project B", "Confirm Deletion", "Are you sure you want to delete this item?", "No items found.", "Add New", "Select Date"/"Apply" (or equivalent on date picker).
- **Calendar:** Month/year label (e.g. "January 2024", "February 2024"); weekday headers; numeric dates; highlighted date (e.g. 15, Fri 16); colored event blocks; "+" on dates where shown.
- **Icons:** Calendar icon on date field; "+" for add; possible warning (e.g. yellow triangle) for "Entry with unfilled details".
- **Inputs:** Date (with picker), Project dropdown, Task dropdown, Time Spent (00:00), Description text area, Billable checkbox; Event Name, Start/End date and time, All Day checkbox; search and filter controls.

### 3.5 UI Interactions

- **Clearly visible or standard:** Open/close modals (New Time Log, Edit Time Log, New/Edit Event); open date picker from date field; select date in picker; choose project/task from dropdowns; type in description/search; toggle Billable/All Day; Cancel/Save; drag entry between columns with drop target highlight; filter by project (and category where shown); switch to list view in calendar flow.
- **Not shown / assumed:** Keyboard behavior, exact hover states (beyond "Fri 16" highlight), validation messages, loading states. **NEED CLARIFICATION** for any further interaction requirements.

### 3.6 Component Mapping

- No design system or codebase components were referenced in the Figma source. **NEED CLARIFICATION:** Map Figma elements to existing design system components (buttons, inputs, modals, dropdowns, calendar, cards). Where no match exists, list under NEED CLARIFICATION.

---

## 4. NEED CLARIFICATION (Mandatory)

- How the user reaches the Time Log / Calendar / Task board screens (navigation, default view).
- Default state on first load (which view, default date/month, initial data).
- Exact outcome after Save in New Time Log and Edit Time Log (where the entry appears, any message).
- Exact outcome after Save in New/Edit Event.
- Whether dragging an entry between columns changes "status" or only order; any confirmation or undo.
- What "+" on a column does (new entry vs add existing).
- What "Add New" in empty state does and on which screen(s).
- What "Confirm Deletion" applies to (time log, event, or task card) and from where it is triggered; what the user sees after confirming.
- Ownership of time logs/events/entries and how it affects visibility and actions.
- When editing is allowed (roles, time windows, etc.).
- Any conversion rules (e.g. draft to final).
- Visibility rules (who sees which projects/tasks/entries).
- Component mapping to existing design system; components that have no match.
- Any search vs filter vs list-view behavior not clearly shown.
- Behavior of "Entry with unfilled details" (warning icon) — what user must do and what happens if they don't.

---

## 5. Scope Declaration

This document defines:

- Functional behavior (user-facing)
- UI visibility and interaction as shown in the Figma source

It explicitly excludes:

- Backend logic
- APIs
- Data storage
- Validation rules
- Technical architecture

