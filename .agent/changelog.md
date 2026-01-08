# Change Log

> **Purpose:** Track all changes made during development sessions.
>
> **Last Updated:** January 8, 2026

---

## January 8, 2026

### REQ-007 & REQ-008: Grid Totals Implementation

**Summary:** Added row totals and column totals to the admin timesheet detail grid.

#### Files Modified

| File                        | Type       | Changes                                                            |
| --------------------------- | ---------- | ------------------------------------------------------------------ |
| `static/js/admin.js`        | JavaScript | Rewrote `renderAdminEntriesGrid()` to calculate and display totals |
| `static/css/components.css` | CSS        | Added 9th column to grid, styled total cells                       |
| `templates/index.html`      | HTML       | Updated cache versions for CSS/JS                                  |
| `docs/REQUIREMENTS.md`      | Docs       | Marked REQ-007 and REQ-008 as Complete                             |

#### Detailed Changes

**`static/js/admin.js` (lines 302-356)**

- Added `dayTotals` array to track column sums
- Added "Total" header cell to header row
- Added row total calculation for each hour type
- Added "Day Total" footer row with column totals
- Added grand total cell in bottom-right corner

**`static/css/components.css` (lines 1002-1037)**

- Changed grid from 8 columns to 9 columns: `140px repeat(7, minmax(70px, 1fr)) 80px`
- Added `.total-column` styling with green tint
- Added `.total-row` styling with border-top
- Added `.grand-total` styling with enhanced green

---

### REQ-005: Current Week Filter

**Summary:** Added "This Week" quick filter button to admin dashboard.

#### Files Modified

| File                   | Type       | Changes                                         |
| ---------------------- | ---------- | ----------------------------------------------- |
| `templates/index.html` | HTML       | Added "📅 This Week" button next to week filter |
| `static/js/admin.js`   | JavaScript | Added click handler with week calculation       |
| `static/css/main.css`  | CSS        | Added `.btn-ghost` with `.active` state         |
| `templates/base.html`  | HTML       | Updated main.css cache version                  |
| `docs/REQUIREMENTS.md` | Docs       | Marked REQ-005 as Complete                      |

#### Detailed Changes

**`static/js/admin.js` (lines 474-509)**

- Added "This Week" button click handler
- Calculates current week's Sunday using `Date` methods
- Sets week filter input value
- Clears other filters for focused view
- Adds `.active` class to button
- Shows toast notification with formatted date range

**`static/css/main.css` (lines 428-443)**

- Added `.btn-ghost` base style (transparent with subtle hover)
- Added `.btn-ghost.active` with green background

---

### REQ-020: Travel Flag Visibility

**Summary:** Added travel and expense badges to timesheet cards on admin dashboard.

#### Files Modified

| File                        | Type       | Changes                                               |
| --------------------------- | ---------- | ----------------------------------------------------- |
| `static/js/admin.js`        | JavaScript | Added travel/expense badge rendering in card template |
| `static/css/components.css` | CSS        | Added `.travel-badge` and `.expense-badge` styles     |
| `docs/REQUIREMENTS.md`      | Docs       | Marked REQ-020 as Complete                            |

#### Detailed Changes

**`static/js/admin.js` (line 58-59)**

- Added conditional rendering: `${ts.traveled ? '<span class="travel-badge">✈️</span>' : ''}`
- Added conditional rendering: `${ts.has_expenses ? '<span class="expense-badge">💰</span>' : ''}`

**`static/css/components.css` (lines 331-351)**

- Added `.travel-badge` with cyan color
- Added `.expense-badge` with warning/yellow color
- Both have `cursor: help` for tooltip indication

---

### REQ-018: Hour Type Filter

**Summary:** Added hour type filter dropdown to admin dashboard for filtering timesheets by entry type.

#### Files Modified

| File                   | Type       | Changes                                        |
| ---------------------- | ---------- | ---------------------------------------------- |
| `templates/index.html` | HTML       | Added "Hours:" dropdown with hour type options |
| `static/js/admin.js`   | JavaScript | Added filter value to params, event handler    |
| `app/routes/admin.py`  | Python     | Added hour_type subquery filter                |
| `docs/REQUIREMENTS.md` | Docs       | Marked REQ-018 as Complete                     |

#### Detailed Changes

**`app/routes/admin.py` (lines 57-78)**

- Added `hour_type` query parameter handling
- Uses `TimesheetEntry` subquery to filter timesheets
- Special case "has_field" filters for any Field hours
- Efficient `.in_()` subquery for performance

**`static/js/admin.js`**

- Added `hourTypeEl` to filter value collection
- Added `hour_type` to API params
- Added change event listener for hour type dropdown
- Included in clear filters reset

---

### BUG-001: Submitted Timesheets Allow Editing

**Summary:** Documented bug where submitted timesheets still show edit controls.

#### Files Created

| File                   | Type | Changes                             |
| ---------------------- | ---- | ----------------------------------- |
| `docs/BUGS.md`         | Docs | NEW - Created bug tracking document |
| `docs/REQUIREMENTS.md` | Docs | Added REQ-023 for bug fix           |

#### Bug Details

- Submitted timesheets show "Add hour type" dropdown
- Hour inputs are editable when they should be disabled
- Edit button visible in Actions column
- Form buttons (Save/Submit) visible

**Fix Plan:**

- Check `timesheet.status` when loading form
- Only `NEW` and `NEEDS_APPROVAL` should be editable
- Hide/disable controls for `SUBMITTED` and `APPROVED`

---

## Previous Sessions

_See IMPLEMENTATION.md and POWERAPPS.md for history of earlier changes._

---

_Log started: January 8, 2026_
