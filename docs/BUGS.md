# Known Issues & Bugs

> **Purpose:** Track known bugs and issues requiring fixes.
>
> **Last Updated:** January 8, 2026

---

## 🐛 Active Issues

### BUG-001: Submitted Timesheets Allow Editing

**Status:** 🔴 Open  
**Severity:** High (P0)  
**Reported:** January 8, 2026

**Description:**
When a user views a timesheet they've submitted, the form still shows editable controls:

- "Select hour type to add..." dropdown (should be hidden)
- Editable hour input fields (should be disabled)
- "Edit" button in Actions column (should be hidden)
- Save Draft / Submit buttons (should be hidden)

**Business Logic:**

| Status           | Can Edit Hours | Can Add Attachments | Can Re-submit |
| ---------------- | -------------- | ------------------- | ------------- |
| `NEW` (Draft)    | ✅ Yes         | ✅ Yes              | ✅ Yes        |
| `SUBMITTED`      | ❌ No          | ❌ No               | ❌ No         |
| `APPROVED`       | ❌ No          | ❌ No               | ❌ No         |
| `NEEDS_APPROVAL` | ✅ Yes\*       | ✅ Yes              | ✅ Yes        |

> **\*Clarification needed:** When admin rejects (sets to `NEEDS_APPROVAL`), should the user be able to:
>
> - A) Only add attachments (hours are locked)
> - B) Fully edit hours AND add attachments (like a draft)
>
> **Current assumption:** Option B - full edit access on rejected timesheets

**Current Behavior:**

- All timesheets show edit controls regardless of status
- Users can attempt to modify hours on submitted timesheets (backend may reject)

**Affected Files:**

- `static/js/timesheet.js` - Form population and UI rendering
- `templates/index.html` - Hour type table structure

**Implementation Plan:**

1. **Determine editable status:**

   ```javascript
   // In loadTimesheet() or populateForm()
   function isTimesheetEditable(status) {
     // Draft and rejected (needs approval) timesheets are editable
     return status === "NEW" || status === "NEEDS_APPROVAL";
   }
   ```

2. **Hide "Add hour type" dropdown when not editable:**

   ```javascript
   const addHourTypeRow = document.querySelector(".add-hour-type-row");
   if (addHourTypeRow) {
     addHourTypeRow.style.display = isEditable ? "flex" : "none";
   }
   ```

3. **Disable hour inputs when not editable:**

   ```javascript
   document.querySelectorAll(".hour-type-row input").forEach((input) => {
     input.disabled = !isEditable;
   });
   ```

4. **Hide edit/delete buttons when not editable:**

   ```javascript
   document.querySelectorAll(".hour-type-row .btn-action").forEach((btn) => {
     btn.style.display = isEditable ? "inline-flex" : "none";
   });
   ```

5. **Hide form action buttons when not editable:**

   ```javascript
   const saveDraftBtn = document.getElementById("save-draft-btn");
   const submitBtn = document.getElementById("submit-btn");
   const deleteBtn = document.getElementById("delete-btn");

   if (saveDraftBtn)
     saveDraftBtn.style.display = isEditable ? "inline-flex" : "none";
   if (submitBtn) submitBtn.style.display = isEditable ? "inline-flex" : "none";
   if (deleteBtn) deleteBtn.style.display = isEditable ? "inline-flex" : "none";
   ```

6. **Show read-only notice for non-editable timesheets:**

   ```html
   <div id="readonly-notice" class="readonly-notice hidden">
     ℹ️ This timesheet has been submitted and cannot be edited.
   </div>
   ```

7. **Verify backend validation:**
   - Check `app/routes/timesheets.py` rejects edits to `SUBMITTED` and `APPROVED` timesheets
   - Ensure `NEEDS_APPROVAL` timesheets CAN be edited

**Acceptance Criteria:**

- [ ] `NEW` (Draft) timesheets are fully editable
- [ ] `SUBMITTED` timesheets are read-only (no hour editing, no form buttons)
- [ ] `APPROVED` timesheets are read-only
- [ ] `NEEDS_APPROVAL` (rejected) timesheets are editable
- [ ] Read-only notice displayed for non-editable timesheets
- [ ] Attachment section still visible for `NEEDS_APPROVAL` status
- [ ] Backend properly validates edit permissions by status

---

### BUG-002: Reimbursement Amounts Display "$null"

**Status:** 🔴 Open  
**Severity:** Medium (P1)  
**Reported:** January 8, 2026  
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

- [ ] Amount field cannot be submitted empty when reimbursement type is selected
- [ ] Existing null amounts display as "$0.00"
- [ ] New submissions always have valid decimal amounts
- [ ] Client-side validation shows error for invalid amounts
- [ ] Server-side validation rejects null/empty amounts

---

### BUG-003: Dev Login Causes Duplicate Key Error

**Status:** 🔴 Open  
**Severity:** High (P0)  
**Reported:** January 8, 2026  
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
5. **Error:** Internal Server Error

**Root Cause:**

The dev authentication bypass in `app/routes/auth.py` always tries to INSERT a new user instead of checking if the user already exists. The code should use a "get or create" pattern.

**Affected Files:**

- `app/routes/auth.py` - Dev authentication bypass logic

**Current Code (Problematic):**

```python
# Creates a new user every time, causing duplicate key error
user = User(
    azure_id='dev-user-001',
    email='dev@localhost',
    display_name='Development User',
    ...
)
db.session.add(user)
db.session.commit()
```

**Fix Required:**

```python
# Check if user exists first, only create if missing
user = User.query.filter_by(azure_id='dev-user-001').first()
if not user:
    user = User(
        azure_id='dev-user-001',
        email='dev@localhost',
        display_name='Development User',
        ...
    )
    db.session.add(user)
    db.session.commit()
```

**Workaround (until fixed):**

Reset the database to clear duplicate users:

```bash
cd docker
docker compose down -v
docker compose up --build -d
```

**Acceptance Criteria:**

- [ ] Dev users can log in multiple times without error
- [ ] Existing dev users are retrieved, not duplicated
- [ ] Same fix applied to MSAL callback for Azure users
- [ ] No unique constraint violations on repeated logins

---

## ✅ Resolved Issues

_None yet._

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
