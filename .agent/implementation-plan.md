# P1 Requirements Implementation Plan

> **Purpose:** Track implementation plan for P1 priority requirements.
>
> **Last Updated:** January 8, 2026 @ 2:02 PM CST

---

## 🎯 Overview

This document tracks the implementation of P1 (Important, should have) requirements from REQUIREMENTS.md.

---

## ✅ Completed (January 8, 2026)

### REQ-007: Column Totals (All Grids) ✅

- **Completed:** January 8, 2026
- **Files Modified:** `admin.js`, `components.css`
- **Description:** Added "Day Total" footer row showing sum of hours per day

### REQ-008: Row Totals (All Grids) ✅

- **Completed:** January 8, 2026
- **Files Modified:** `admin.js`, `components.css`, `index.html`
- **Description:** Added "Total" column showing sum of hours per hour type

### REQ-005: Current Week Filter ✅

- **Completed:** January 8, 2026
- **Files Modified:** `index.html`, `admin.js`, `main.css`
- **Description:** "This Week" quick filter button on admin dashboard

### REQ-020: Travel Flag Visibility ✅

- **Completed:** January 8, 2026
- **Files Modified:** `admin.js`, `components.css`
- **Description:** ✈️ travel and 💰 expense badges on timesheet cards

### REQ-018: Hour Type Filter ✅

- **Completed:** January 8, 2026
- **Files Modified:** `index.html`, `admin.js`, `admin.py`
- **Description:** Hour type dropdown filter on admin dashboard

### REQ-014: Submit Without Attachment (Warning) ✅

- **Completed:** January 7, 2026
- **Description:** Allow submit with warning when Field Hours lack attachment

### REQ-022: Holiday Awareness & Warning ✅

- **Completed:** January 7, 2026
- **Description:** Visual holiday indicators and confirmation dialog

---

## 🐛 Bugs to Fix

### BUG-001 / REQ-023: Read-Only Submitted Timesheets

- **Priority:** P0 (High)
- **Effort:** Medium (~45 min)
- **Issue:** Submitted timesheets still show edit controls
- **See:** `docs/BUGS.md` for implementation plan

---

## 🔜 Up Next

### REQ-004: Pay Period Filter

**Priority:** Medium
**Effort:** Medium (~1 hour)

**Implementation:**

1. Define pay period logic (biweekly schedule)
2. Add "Current Pay Period" filter button
3. Calculate start/end dates for current pay period
4. Show date range in filter UI

**Files to Modify:**

- `templates/index.html` - Add pay period filter button
- `static/js/admin.js` - Add pay period calculation
- May need config for pay period start dates

---

### REQ-019: Export Format Options

**Priority:** Medium
**Effort:** Medium (~1 hour)

**Implementation:**

1. Add export format dropdown (CSV, PDF, Excel)
2. Create PDF generation endpoint
3. Create Excel generation endpoint
4. Use existing CSV as base

**Files to Modify:**

- `templates/index.html` - Modify export button/dropdown
- `app/routes/admin.py` - Add export endpoints
- May need new dependencies (reportlab for PDF, openpyxl for Excel)

---

## 📋 Remaining P1 Requirements

| REQ     | Description                          | Status     | Est. Effort |
| ------- | ------------------------------------ | ---------- | ----------- |
| REQ-003 | User Notification Preferences        | 📋 Planned | High        |
| REQ-004 | Pay Period Filter                    | 📋 Planned | Medium      |
| REQ-009 | Auto-Populate Any Hour Type          | ✅ Partial | Low         |
| REQ-011 | Email Notifications                  | 📋 Planned | High        |
| REQ-019 | Export Format Options                | 📋 Planned | Medium      |
| REQ-021 | Per-Option Reimbursement Attachments | 📋 Planned | Medium      |
| REQ-023 | Read-Only Submitted Timesheets       | 🐛 Bug     | Medium      |

---

## 📈 Progress Summary

| Category                  | Count |
| ------------------------- | ----- |
| **Total P1 Requirements** | 14    |
| **Completed**             | 7     |
| **Partial**               | 1     |
| **Bugs**                  | 1     |
| **Remaining**             | 5     |

**Completion Rate:** ~57%

---

## 📝 Notes

- REQ-023 (BUG-001) should be fixed before other P1 items
- REQ-004 may need business input for pay period schedule
- REQ-011 and REQ-003 are larger features requiring more planning
- Consider implementing REQ-019 with just CSV initially if time-constrained

---

_Plan created: January 8, 2026_
_Last updated: January 8, 2026 @ 2:02 PM CST_
