# Known Issues & Bugs

> **Purpose:** Track known bugs and issues requiring fixes.
>
> **Last Updated:** January 14, 2026

---

## 📋 Bug Index

| ID                                                              | Title                                        | Status      | Severity | Reported |
| --------------------------------------------------------------- | -------------------------------------------- | ----------- | -------- | -------- |
| [BUG-001](#bug-001-submitted-timesheets-allow-editing-)         | Submitted Timesheets Allow Editing           | ✅ Resolved | P0       | Jan 8    |
| [BUG-002](#bug-002-reimbursement-amounts-display-null)          | Reimbursement Amounts Display "$null"        | ✅ Resolved | P1       | Jan 8    |
| [BUG-003](#bug-003-dev-login-causes-duplicate-key-error)        | Dev Login Causes Duplicate Key Error         | ✅ Resolved | P0       | Jan 8    |
| [BUG-004](#bug-004-draft-timesheets-missing-savesubmit-buttons) | Draft Timesheets Missing Save/Submit Buttons | ✅ Resolved | P1       | Jan 8    |
| [BUG-005](#bug-005-leading-zero-not-removed-from-hour-inputs)   | Leading Zero Not Removed from Hour Inputs    | ✅ Resolved | P2       | Jan 11   |
| [BUG-006](#bug-006-upload-error-on-needs_approval-status)       | Upload Error on NEEDS_APPROVAL Status        | ✅ Resolved | P1       | Jan 12   |
| [BUG-007](#bug-007-hamburger-menu-persists-on-resize)           | Hamburger Menu Persists on Window Resize     | 🔴 Open     | P2       | Jan 13   |
| [BUG-008](#bug-008-non-field-hour-types-reset-to-field)         | Non-Field Hour Types Reset to Field          | ✅ Resolved | P0       | Jan 14   |
| [BUG-009](#bug-009-delete-button-not-working)                   | Delete Button Not Working                    | ✅ Resolved | P1       | Jan 14   |

---

## 🐛 Active Issues

### BUG-007: Hamburger Menu Persists on Window Resize

**Status:** 🔴 Open  
**Severity:** Low (P2)  
**Reported:** January 13, 2026  
**Related:** Mobile UI

**Description:**
When the hamburger menu is open on mobile width and the user resizes the window to desktop width, the menu does not automatically close. It continues to widen with the viewport and lacks an X button to close it, leaving the UI in a broken state.

**Steps to Reproduce:**

1. Open the app at desktop width
2. Resize the browser window to mobile width (≤768px)
3. Click the hamburger menu button to open the mobile navigation
4. While the menu is open, resize the window back to desktop width (>768px)
5. **Expected:** Menu should automatically close
6. **Actual:** Menu remains open, stretches full width, no way to close it

**Screenshot:**
![Hamburger menu stuck open on resize](../assets/bug-007-hamburger-resize.png)

**Root Cause:**
The JavaScript hamburger toggle only toggles a CSS class on click. There is no `resize` event listener to automatically close the menu when the viewport exceeds mobile breakpoint.

**Fix Plan:**

**Option A (JavaScript - Recommended):**
Add a resize event listener to close the mobile menu when viewport exceeds 768px:

```javascript
// In app.js or main.js
window.addEventListener("resize", () => {
  if (window.innerWidth > 768) {
    const mobileNav = document.getElementById("mobile-nav");
    const hamburgerBtn = document.getElementById("hamburger-btn");
    if (mobileNav) mobileNav.classList.add("hidden");
    if (hamburgerBtn) hamburgerBtn.classList.remove("active");
  }
});
```

**Option B (CSS Only):**
Force hide the mobile nav above 768px using `!important`:

```css
@media (min-width: 769px) {
  .mobile-nav {
    display: none !important;
  }
}
```

**Recommendation:** Option A is preferred as it properly resets component state.

**Acceptance Criteria:**

- [ ] Mobile menu auto-closes when window is resized above 768px
- [ ] Hamburger button state resets (not showing X anymore)
- [ ] No visual artifacts when transitioning between breakpoints

---

### BUG-008: Non-Field Hour Types Reset to Field ✅

**Status:** 🟢 Resolved  
**Severity:** High (P0)  
**Reported:** January 14, 2026  
**Resolved:** January 14, 2026  
**Related:** REQ-044, Hour Type Management

**Description:**
When creating a new timesheet and selecting non-Field hour types (e.g., PTO, Internal, Training), the entries are incorrectly reset to "Field Hours" upon save/submit. This causes timesheets with only PTO or Internal hours to be rejected for missing attachments (which are only required for Field Hours).

**Steps to Reproduce:**

1. Log in to the app
2. Click "New Timesheet"
3. Select a week
4. Add a row with hour type "PTO" (or Internal, Training, Unpaid, Holiday)
5. Enter 8 hours on a day
6. Click "Submit"
7. **Expected:** Timesheet saved with PTO hours, no attachment required
8. **Actual:** Hours are saved as "Field Hours", attachment warning appears, timesheet gets NEEDS_APPROVAL status

**Affected Hour Types:**

- PTO → incorrectly becomes Field
- Internal → incorrectly becomes Field
- Training → may work (exists in both modules)
- Unpaid → incorrectly becomes Field
- Holiday → may work (exists in both modules)

**Root Cause (Suspected):**
Mismatch between hour type definitions in different modules:

| Module         | Hour Types Available                            |
| -------------- | ----------------------------------------------- |
| `timesheet.js` | Field, Internal, Training, PTO, Unpaid, Holiday |
| `entries.js`   | Work, Training, Field, Holiday                  |

`entries.js` only defines 4 hour types and uses `Work` instead of `Internal`. When a type like `PTO` or `Internal` is used, it may not be properly recognized and defaults to `Field`.

**Affected Files:**

- `static/js/timesheet/entries.js` - Line 9-18: HOUR_TYPES and ALL_HOUR_TYPES are incomplete
- `static/js/timesheet.js` - Line 29-36: Has correct HOUR_TYPES definition

**Fix Plan:**

1. **Synchronize hour type definitions** - Update `entries.js` to match `timesheet.js`
2. **Remove duplicate definitions** - Consider a single source of truth for hour types
3. **Add validation** - Log warning if unknown hour type is passed to prevent silent failures

**Acceptance Criteria:**

- [ ] PTO hours submit correctly without attachment requirement
- [ ] Internal hours submit correctly without attachment requirement
- [ ] Training, Unpaid, Holiday hours work correctly
- [ ] Only Field Hours trigger the attachment requirement
- [ ] Hour type is preserved through save/submit cycle

---

### BUG-009: Delete Button Not Working ✅

**Status:** 🟢 Resolved  
**Severity:** Medium (P1)  
**Reported:** January 14, 2026  
**Resolved:** January 14, 2026

**Description:**
The Delete button on the timesheet editor was not working due to the browser's native `confirm()` dialog disappearing immediately (same root cause as the submit confirmation issue).

**Root Cause:**
Browser `confirm()` dialogs can be auto-dismissed in certain conditions, preventing user interaction.

**Fix:**
Replaced `confirm()` with custom `showConfirmDialog()` modal that:

- Shows a styled confirmation dialog with 🗑️ icon
- Waits for user to click "Delete" or "Cancel"
- Won't auto-dismiss like browser dialogs

**Affected Files:**

- `static/js/app.js` - `deleteTimesheet()` function

**Acceptance Criteria:**

- [x] Delete button shows confirmation modal
- [x] Clicking "Delete" removes the timesheet
- [x] Clicking "Cancel" keeps the timesheet

---

### BUG-001: Submitted Timesheets Allow Editing ✅

**Status:** 🟢 Resolved  
**Severity:** High (P0)  
**Reported:** January 8, 2026  
**Resolved:** January 8, 2026

**Description:**
When a user views a timesheet they've submitted, the form should be read-only.

**Business Logic (Implemented):**

| Status           | Can Edit Hours | Can Add Attachments | Can Re-submit |
| ---------------- | -------------- | ------------------- | ------------- |
| `NEW` (Draft)    | ✅ Yes         | ✅ Yes              | ✅ Yes        |
| `SUBMITTED`      | ❌ No          | ❌ No               | ❌ No         |
| `APPROVED`       | ❌ No          | ❌ No               | ❌ No         |
| `NEEDS_APPROVAL` | ✅ Yes         | ✅ Yes              | ✅ Yes        |

**Resolution:** Option B - full edit access on rejected (`NEEDS_APPROVAL`) timesheets so users can fix and resubmit.

**Implementation (January 8, 2026):**

1. ✅ Added `isTimesheetEditable(status)` helper function in `timesheet.js`
2. ✅ Updated `setFormReadOnly()` to hide all edit controls:
   - Add hour type dropdown + button
   - Auto-populate checkbox
   - Hour inputs (disabled)
   - Done/Edit/Remove buttons on rows
   - Save Draft / Submit buttons
   - Upload zone for attachments
   - Reimbursement add/remove buttons
3. ✅ Added read-only notice banner with status-specific message
4. ✅ Updated backend routes to allow `NEEDS_APPROVAL` status editing:
   - `update_timesheet()` - allows NEW and NEEDS_APPROVAL
   - `update_entries()` - allows NEW and NEEDS_APPROVAL
   - `submit_timesheet()` - allows NEW and NEEDS_APPROVAL
5. ✅ Added CSS styling for `.readonly-notice` banner

**Files Changed:**

- `static/js/timesheet.js` - Read-only mode logic
- `templates/index.html` - Read-only notice HTML
- `static/css/components.css` - Notice styling
- `app/routes/timesheets.py` - Backend validation

**Acceptance Criteria (All Met):**

- [x] `NEW` (Draft) timesheets are fully editable
- [x] `SUBMITTED` timesheets are read-only (no hour editing, no form buttons)
- [x] `APPROVED` timesheets are read-only
- [x] `NEEDS_APPROVAL` (rejected) timesheets are editable
- [x] Read-only notice displayed for non-editable timesheets
- [x] Attachment section hidden for submitted/approved timesheets
- [x] Backend properly validates edit permissions by status

---

### BUG-004: Draft Timesheets Missing Save/Submit Buttons

**Status:** ✅ Resolved  
**Severity:** Medium (P1)  
**Reported:** January 8, 2026  
**Resolved:** January 9, 2026  
**Related:** REQ-023

**Description:**
When viewing an existing draft timesheet (`NEW` status), the Save Draft and Submit buttons were not visible.

**Root Cause:**
Missing closing `</div>` tag for `.form-row` in the travel section (line 359 of index.html). This caused all subsequent HTML elements (expense section, attachments, notes, and action buttons) to be incorrectly nested inside `#travel-section`, making them invisible when "Traveled this week" checkbox was unchecked.

**Fix Applied:**
Added missing `</div>` to properly close the form-row, restoring correct HTML nesting.

**Expected Behavior:**

- Draft timesheets (`status: 'NEW'`) should have:
  - ✅ Save Draft button visible
  - ✅ Submit button visible
  - ✅ All hour inputs editable
  - ✅ Add hour type dropdown visible
  - ✅ Attachment upload zone visible

**Root Cause (if confirmed):**

The `setFormReadOnly(false)` call should reset all buttons to visible, but the button display styles may not be set correctly when transitioning from read-only to editable mode.

**How to Verify:**

1. Log in to the app
2. Create a new timesheet and save as draft
3. Navigate away, then click on the draft from "My Timesheets"
4. Verify that Save Draft and Submit buttons are visible at the bottom

**Implementation Fix (if needed):**

**File: `static/js/timesheet.js`**

In the `setFormReadOnly(readOnly)` function, ensure button visibility is explicitly restored:

```javascript
// Line ~970-980: Ensure buttons are restored when not read-only
const saveBtn = document.getElementById("save-draft-btn");
const submitBtn = document.getElementById("submit-btn");
if (saveBtn) saveBtn.style.display = readOnly ? "none" : "inline-flex";
if (submitBtn) submitBtn.style.display = readOnly ? "none" : "inline-flex";
```

Also ensure the parent `.form-actions` container is visible:

```javascript
// Add this to setFormReadOnly():
const formActions = document.querySelector(".form-actions");
if (formActions) {
  formActions.style.display = readOnly ? "none" : "flex";
}
```

**File: `templates/index.html`**

Verify the form-actions section exists and has correct structure:

```html
<!-- Around line 555-590 -->
<div class="form-actions">
  <button type="button" id="save-draft-btn" class="btn btn-secondary">
    💾 Save Draft
  </button>
  <button type="button" id="submit-btn" class="btn btn-primary">
    🚀 Submit
  </button>
</div>
```

**Acceptance Criteria:**

- [x] Draft timesheets show Save Draft and Submit buttons _(Verified Jan 11, 2026)_
- [x] Buttons work correctly when clicked _(Verified Jan 11, 2026)_
- [x] Submitted/Approved timesheets still hide the buttons _(Verified Jan 11, 2026)_

---

### BUG-002: Reimbursement Amounts Display "$null"

**Status:** ✅ Resolved  
**Severity:** Medium (P1)  
**Reported:** January 8, 2026  
**Resolved:** January 10, 2026  
**Related:** REQ-026

**Description:**
When a timesheet with reimbursement is saved without a proper amount value, the expense displays as "Car: $null" or similar instead of a formatted currency value.

**Steps to Reproduce:**

1. Create a new timesheet
2. Check "Reimbursement needed" checkbox
3. Select an expense type (e.g., "Car")
4. Leave the Amount field empty or unclear
5. Save/submit the timesheet
6. View the timesheet in the admin dashboard

**Expected Behavior:**

- Amount should default to $0.00 if left empty
- Display should always show properly formatted currency: "$45.00"

**Actual Behavior:**

- Amount stores as `null` in database
- Display renders as "Car: $null"

**Root Cause:**

1. **Frontend:** No validation requiring amount field to be filled
2. **Backend:** `reimbursement_amount` column allows NULL values
3. **Display:** Template/JS does not handle null values gracefully

**Affected Files:**

- `templates/index.html` - Reimbursement display in form
- `static/js/timesheet.js` - Form submission logic
- `app/models.py` - Timesheet model (reimbursement_amount field)
- `app/routes/timesheets.py` - API validation

**Fix Plan:**

1. Add `required` attribute to reimbursement amount input
2. Add client-side validation: amount must be a valid number ≥ 0
3. Add server-side validation: reject null/empty amounts
4. Database migration: set DEFAULT 0.00 on reimbursement_amount
5. Display fix: if amount is null, display "$0.00" instead of "$null"

**Acceptance Criteria:**

- [x] Amount field cannot be submitted empty when reimbursement type is selected _(Implemented Jan 11, 2026)_
- [x] Existing null amounts display as "$0.00"
- [x] New submissions always have valid decimal amounts
- [x] Client-side validation shows error for invalid amounts _(Implemented Jan 11, 2026)_
- [x] Server-side validation rejects null/empty amounts

**Resolution (January 10, 2026):**

1. ✅ Added `formatCurrency()` helper function in `static/js/admin.js`
   - Safely handles null, undefined, and NaN values
   - Returns "$0.00" for invalid amounts
2. ✅ Updated admin detail view to use `formatCurrency()` instead of `.toFixed(2)`
3. ✅ Backend `to_dict()` already returns `0.0` for null amounts (line 228-230)
4. ✅ Frontend `populateForm()` already handles null → "0.00" (line 605)

**Additional Implementation (January 11, 2026):**

5. ✅ Added `validateReimbursementItems()` function in `static/js/timesheet.js`
   - Validates all items with a type selected have a valid amount > 0
   - Returns validation result with error messages and invalid item IDs
6. ✅ Added `highlightInvalidReimbursementItems()` for visual error feedback
   - Highlights invalid items with red border and shake animation
   - Highlights specific amount input fields
7. ✅ Updated `submitTimesheet()` in `static/js/app.js` to validate before submit
   - Shows error toast with specific validation message
   - Scrolls to reimbursement section and highlights invalid fields
8. ✅ Added CSS validation error styles in `static/css/components.css`
   - `.validation-error` class for item container
   - `.input-error` class for input fields
   - Shake animation for attention

**Files Changed:**

- `static/js/admin.js` - Added formatCurrency helper, fixed display

---

### BUG-003: Dev Login Causes Duplicate Key Error

**Status:** ✅ Resolved  
**Severity:** High (P0)  
**Reported:** January 8, 2026  
**Resolved:** January 10, 2026 (verified - fix was already in place)  
**Related:** REQ-015, REQ-030

**Description:**
Clicking the dev login buttons (or Microsoft Login without proper Azure credentials) results in an Internal Server Error due to a database unique constraint violation.

**Error Message:**

```
sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation)
duplicate key value violates unique constraint "users_azure_id_key"
DETAIL: Key (azure_id)=(dev-user-001) already exists.
```

**Steps to Reproduce:**

1. Start the application with Docker
2. Log in as any dev user (Admin, Support, etc.)
3. Log out
4. Try to log in again with any dev user
5. **Expected (now fixed):** Login succeeds without error

**Root Cause:**

The dev authentication bypass in `app/routes/auth.py` originally always tried to INSERT a new user instead of checking if the user already exists.

**Fix Applied:**

All three authentication routes now use the "get-or-create" pattern:

1. `/auth/login` (lines 66-78): Checks `azure_id` then `email` before creating
2. `/auth/dev-login` (lines 248-261): Checks `email` before creating
3. `/auth/callback` (lines 142-161): Checks `azure_id` before creating

**Acceptance Criteria:**

- [x] Dev users can log in multiple times without error
- [x] Existing dev users are retrieved, not duplicated
- [x] Same fix applied to MSAL callback for Azure users
- [x] No unique constraint violations on repeated logins

**Verification (January 10, 2026):**

Browser testing confirmed:

1. First login as Admin → Success
2. Logout → Success
3. Second login as Admin → Success (no duplicate key error)
4. App dashboard loads correctly with "Admin User" displayed

---

### BUG-005: Leading Zero Not Removed from Hour Inputs

**Status:** ✅ Resolved
**Severity:** Low (P2)
**Reported:** January 11, 2026
**Resolved:** January 12, 2026
**Related:** N/A

**Description:**
When typing hours into an hour input field that displays "0", the leading zero is not removed. For example, typing "8" results in "08" being displayed instead of just "8".

**Steps to Reproduce:**

1. Log in to the app
2. Create or open a timesheet
3. Add an hour type row (e.g., Internal Hours)
4. Click on a day's input field (which shows "0")
5. Type "8"
6. **Expected:** Field shows "8"
7. **Actual:** Field shows "08"

**Root Cause:**
HTML number inputs preserve leading zeros when users type without first clearing the field. The browser appends new digits to the existing "0" value rather than replacing it.

**Implementation:**

1. Added `normalizeHourInput` to `static/js/timesheet.js`
2. Updated input `oninput` handler to call normalization before updating totals

**Acceptance Criteria:**

- [x] Typing into an hour field with "0" displays only the typed number
- [x] Values like "08" are normalized to "8"
- [x] Decimal values still work correctly (e.g., "0.5")
- [x] Empty field still shows "0" (placeholder) or empty string

---

---

### BUG-006: Upload Error on NEEDS_APPROVAL Status

**Status:** ✅ Resolved
**Severity:** Medium (P1)
**Reported:** January 12, 2026
**Investigated:** January 12, 2026
**Resolved:** January 12, 2026
**Related:** REQ-014

**Description:**
When a timesheet with `NEEDS_APPROVAL` status (field hours submitted without attachment) has a file uploaded, subsequent edit/submit attempts fail with an error.

**Error Message:**

> "Only draft or rejected timesheets can be edited"

**Steps to Reproduce:**

1. Create a timesheet with Field Hours but NO attachment.
2. Submit → Warning "Field Hours require attachment" appears.
3. Select "Submit Anyway" → Status becomes `NEEDS_APPROVAL`.
4. Later, open the timesheet to upload the missing file.
5. Upload a file → **Upload succeeds**.
6. Try to edit anything or re-submit.
7. **Actual:** Error "Only draft or rejected timesheets can be edited."

**Root Cause (Confirmed):**

Located in `app/routes/timesheets.py` lines 516-518:

```python
# If timesheet was NEEDS_APPROVAL, update to SUBMITTED
if timesheet.status == TimesheetStatus.NEEDS_APPROVAL:
    timesheet.status = TimesheetStatus.SUBMITTED
```

**The bug flow:**

1. User submits with field hours but no attachment → Status: `NEEDS_APPROVAL`
2. User uploads an attachment → `upload_attachment()` succeeds
3. **Line 517-518**: Backend auto-changes status `NEEDS_APPROVAL` → `SUBMITTED`
4. User tries to edit/submit → Status is now `SUBMITTED` (read-only) → **FAIL**

The upload succeeded, but the auto-status-change locked the timesheet prematurely.

**Why the frontend shows the error:**

- After upload, frontend has stale state (`status: NEEDS_APPROVAL`)
- User clicks "Submit" or edits a field
- `submitTimesheet()` calls `API.updateTimesheet()` first (line 297 in app.js)
- Backend rejects because status is now `SUBMITTED`
- Error displayed to user

**Fix Options:**

**Option A (Backend - Recommended):**
Remove the auto-status-change on upload. Let the user explicitly re-submit:

```python
# In upload_attachment():
# REMOVE lines 516-518
# User must click "Submit" again to change status
```

**Option B (Frontend - Alternative):**
Refresh timesheet state after upload to get new status:

```javascript
// In handleFileUpload():
const timesheet = await API.getTimesheet(timesheetId);
TimesheetModule.populateForm(timesheet); // Refresh entire form
```

**Option C (Backend - Advanced):**
Auto-submit only if ALL requirements are now met:

```python
# After upload, check if timesheet is now complete
if (timesheet.status == TimesheetStatus.NEEDS_APPROVAL
    and not timesheet.requires_attachment()
    and not timesheet.get_missing_reimbursement_attachments()):
    timesheet.status = TimesheetStatus.SUBMITTED
```

**Recommendation:** Option A is simplest and maintains user control.

**Implementation (January 12, 2026):**

1. ✅ Removed auto-status-change in `upload_attachment()` (lines 516-518)
2. ✅ Added comment explaining the fix
3. ✅ Added `needs_approval_timesheet` fixture in `tests/conftest.py`
4. ✅ Added 3 tests in `TestBug006UploadOnNeedsApproval` class

**Files Changed:**

- `app/routes/timesheets.py` — Removed auto-status-change on upload
- `tests/conftest.py` — Added `needs_approval_timesheet` fixture
- `tests/test_timesheets.py` — Added `TestBug006UploadOnNeedsApproval` test class

**Acceptance Criteria:**

- [x] Upload on `NEEDS_APPROVAL` timesheet does NOT auto-change status
- [x] User can edit form after uploading attachment
- [x] User can successfully re-submit after uploading attachment
- [x] Test coverage for this scenario (3 tests)

---

## ✅ Resolved Issues

### BUG-001: Submitted Timesheets Allow Editing

Resolved January 8, 2026. See [BUG-001](#bug-001-submitted-timesheets-allow-editing-) above for details.

### BUG-002: Reimbursement Amounts Display "$null"

Resolved January 10, 2026. See [BUG-002](#bug-002-reimbursement-amounts-display-null) above for details.

### BUG-003: Dev Login Causes Duplicate Key Error

Resolved January 10, 2026 (verified - fix was already in place). See [BUG-003](#bug-003-dev-login-causes-duplicate-key-error) above for details.

### BUG-004: Draft Timesheets Missing Save/Submit Buttons

Resolved January 9, 2026. See [BUG-004](#bug-004-draft-timesheets-missing-savesubmit-buttons) above for details.

---

## 📝 Status Reference

| Status           | Description                 | User Action                          |
| ---------------- | --------------------------- | ------------------------------------ |
| `NEW`            | Draft, not yet submitted    | Full edit access                     |
| `SUBMITTED`      | Pending admin review        | Read-only, waiting                   |
| `APPROVED`       | Admin approved              | Read-only, complete                  |
| `NEEDS_APPROVAL` | Admin rejected, needs fixes | Full edit access to fix and resubmit |

---

_Document created: January 8, 2026_  
_Last updated: January 13, 2026_
