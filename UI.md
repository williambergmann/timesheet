# Timesheet UI Refactor

## Overview

This document describes the UI changes made to simplify the timesheet hour entry experience. The goal was to align the UI with the PowerApps version while maintaining all functionality.

## Current State

**Status:** ✅ Complete (Merged to Main)

All UI refactor changes have been merged to the `main` branch and are now in production.

---

## Changes Made

### 1. Time Entries Section (New "Add Row" UX)

**Before:**

- Static grid showing ALL hour types as rows simultaneously
- 8-column layout: Hour Type + 7 days
- Users could enter hours for any type in any row

**After:**

- Dynamic rows added via dropdown + **[+]** button
- Users select an hour type → click + → row appears
- Each row has 7-day inputs + action buttons (Done/Edit, Remove)
- Multiple hour types can be added as separate rows
- Cleaner, PowerApps-style interaction

### 2. Week Start Fix

- **Issue:** Week boundaries were calculated using UTC, causing off-by-one errors
- **Solution:** Use local timezone for week start calculations
- **Result:** Selecting any day correctly snaps to Sunday of that week

### 3. Field Hours Attachment Warning

- When submitting with Field Hours but no attachment, shows confirmation dialog
- If user cancels, scrolls to attachments section with highlight animation
- Toast notification reminds user to upload approval document

### 4. Files Modified

| File                        | Changes                                                                                                          |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `templates/index.html`      | Replaced static grid with dropdown + add button + dynamic row container                                          |
| `static/js/timesheet.js`    | Complete rewrite with new methods: `addHourTypeRow()`, `removeHourTypeRow()`, `toggleEditRow()`, `initForWeek()` |
| `static/css/components.css` | Added styles for `.add-hour-type-row`, `.hour-type-row`, `.hour-type-row-header`, button variants                |
| `static/js/app.js`          | Added attachment warning logic for Field Hours                                                                   |

---

## UX Flow

### Adding a New Hour Type Row

1. Select hour type from dropdown (e.g., "Field Hours")
2. Click the **[+]** button
3. A new row appears in the grid:

| Hour Type   | Sun | Mon | Tue | Wed | Thu | Fri | Sat | Actions  |
| ----------- | --- | --- | --- | --- | --- | --- | --- | -------- |
| Field Hours | `0` | `0` | `0` | `0` | `0` | `0` | `0` | ✓ Done ✕ |

4. Enter hours for each day → Click **✓ Done** (row becomes read-only)
5. Repeat for additional hour types (PTO, Training, etc.)
6. **Save Draft** or **Submit**

### Example: Completed Week

| Hour Type   | Sun | Mon | Tue | Wed | Thu | Fri | Sat | Actions   |
| ----------- | --- | --- | --- | --- | --- | --- | --- | --------- |
| Field Hours | 0   | 8   | 8   | 8   | 8   | 8   | 0   | ✏️ Edit ✕ |
| PTO         | 0   | 0   | 0   | 0   | 0   | 0   | 0   | ✏️ Edit ✕ |
| Training    | 0   | 0   | 0   | 0   | 0   | 0   | 4   | ✏️ Edit ✕ |

---

## Resolved Issues

### ✅ Static File Caching

- **Fixed:** Added version parameters to static file includes (`?v=8`)
- Files are now cache-busted on each release

### ✅ Week Start Timezone Bug

- **Fixed:** `getWeekStart()` now uses local time parsing and formatting
- No more off-by-one day errors due to UTC conversion

### ✅ Button Styling Inconsistencies

- **Fixed:** Normalized all `.btn-action` buttons with consistent height, borders, and padding

---

## Testing

### Manual Test Steps

1. Start Docker: `docker compose up -d`
2. Navigate to http://localhost/app
3. Click "+ New Timesheet"
4. Verify dropdown shows hour types
5. Select "Field Hours" → Click [+]
6. Verify row appears with 7-day inputs
7. Enter hours → Click "✓ Done"
8. Add another type (e.g., PTO)
9. Click "Save Draft"
10. Verify entries are saved correctly
11. Click "Submit" without attachment
12. Verify warning dialog appears

---

## Reference

- **PowerApps Version:** Uses dropdown-based hour type selection
- **Material Design:** Button styling follows MD guidelines
- **Dark Mode:** Planned for next phase (see DARKMODE.md)
