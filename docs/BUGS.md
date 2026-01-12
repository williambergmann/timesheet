# Known Issues & Bugs

> **Purpose:** Track known bugs and issues requiring fixes.
>
> **Last Updated:** January 12, 2026

---

## 📋 Bug Index

| ID                                                              | Title                                        | Status      | Severity | Reported |
| --------------------------------------------------------------- | -------------------------------------------- | ----------- | -------- | -------- |
| [BUG-001](#bug-001-submitted-timesheets-allow-editing-)         | Submitted Timesheets Allow Editing           | ✅ Resolved | P0       | Jan 8    |
| [BUG-002](#bug-002-reimbursement-amounts-display-null)          | Reimbursement Amounts Display "$null"        | ✅ Resolved | P1       | Jan 8    |
| [BUG-003](#bug-003-dev-login-causes-duplicate-key-error)        | Dev Login Causes Duplicate Key Error         | ✅ Resolved | P0       | Jan 8    |
| [BUG-004](#bug-004-draft-timesheets-missing-savesubmit-buttons) | Draft Timesheets Missing Save/Submit Buttons | ✅ Resolved | P1       | Jan 8    |
| [BUG-005](#bug-005-leading-zero-not-removed-from-hour-inputs)   | Leading Zero Not Removed from Hour Inputs    | ✅ Resolved | P2       | Jan 11   |
| [BUG-006](#bug-006-upload-error-on-needs_upload-status)         | Upload Error on NEEDS_UPLOAD Status          | 🔴 Open     | P1       | Jan 12   |

---

## 🐛 Active Issues

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

### BUG-006: Upload Error on NEEDS_UPLOAD Status

**Status:** 🔴 Open
**Severity:** Medium (P1)
**Reported:** January 12, 2026
**Related:** REQ-014

**Description:**
When a timesheet has a status requiring an upload (e.g., trying to resolve a "Field Hours require attachment" warning), uploading the file triggers an error message prevents further editing or submission.

**Error Message:**

> "Only draft or rejected timesheets can be edited"

**Steps to Reproduce:**

1. Create a timesheet with Field Hours but NO attachment.
2. Try to submit -> Warning "Field Hours require attachment" appears.
3. Select "Submit Anyway" (or similar workflow that sets an intermediate status).
4. Later, open the timesheet to upload the missing file.
5. Upload a file.
6. **Expected:** File uploads, and user can now Submit.
7. **Actual:** Error banner appears: "Only draft or rejected timesheets can be edited."

**Root Cause (Hypothesis):**
The `isTimesheetEditable()` check in `static/js/timesheet.js` or the backend decorators likely default to `False` for any status that is not explicitly `NEW` or `NEEDS_APPROVAL`. The intermediate status (likely `NEEDS_UPLOAD` or similar) is being treated as read-only.

**Proposed Resolution:**

1. Verify the exact status code being used (e.g., `NEEDS_UPLOAD` or `PENDING`).
2. Update `isTimesheetEditable` to include this status.
3. Update backend validation in `app/routes/timesheets.py` to allow edits/uploads for this status.

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
_Last updated: January 11, 2026_
