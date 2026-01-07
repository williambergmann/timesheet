# Feature Requirements

> **Purpose:** Track new feature requirements identified from stakeholder decisions.
>
> **Source:** Design decisions captured in [DESIGN.md](DESIGN.md)
>
> **Last Updated:** January 7, 2026

---

## 🎯 Priority Legend

- **P0** - Must have for launch
- **P1** - Important, should have
- **P2** - Nice to have
- **P3** - Future consideration

---

## 👥 User Roles & Permissions

### REQ-001: Four-Tier Role System (P0)

Implement a 4-level role hierarchy with different permissions:

| Role        | Submit Own | Approve Trainee | Approve All | Hour Types Available |
| ----------- | ---------- | --------------- | ----------- | -------------------- |
| **Trainee** | ✅         | ❌              | ❌          | Training only        |
| **Support** | ✅         | ✅              | ❌          | All types            |
| **Staff**   | ✅         | ❌              | ❌          | All types            |
| **Admin**   | ✅         | ✅              | ✅          | All types            |

**Implementation Notes:**

- Add `role` field to User model (enum: `trainee`, `support`, `staff`, `admin`)
- Replace boolean `is_admin` with role-based checks
- Filter hour type dropdown based on user role
- Filter approval actions based on role permissions

---

### REQ-002: Dev Mode Test Accounts (P0)

Create test accounts on the login page for development:

| Role    | Username | Password |
| ------- | -------- | -------- |
| Trainee | trainee  | trainee  |
| Support | support  | support  |
| Staff   | staff    | staff    |
| Admin   | admin    | password |

**Implementation Notes:**

- Display login buttons/form on landing page
- These will be replaced by Azure AD credentials in production
- Each account should demonstrate its role's capabilities

---

## 📱 User Settings

### REQ-003: User Notification Preferences (P1)

Add a User Settings section where users can configure:

**Contact Information:**

- Phone number (for SMS notifications)
- Email address (for email notifications)

**Notification Preferences:**

- [ ] Email notifications (toggle)
- [ ] SMS notifications (toggle)
- [ ] Teams notifications (toggle)

**Implementation Notes:**

- Add settings page accessible from user menu
- Store preferences in User model
- Default all notifications to ON for new users
- SMS opt-out already partially implemented

---

## 📊 Admin Dashboard

### REQ-004: Pay Period Filter (P1)

Add ability to filter timesheets by current pay period (biweekly).

**Features:**

- "Current Pay Period" quick filter button
- Pay period date range display
- Group timesheets by pay period

**Implementation Notes:**

- Define pay period start dates (need business input on which weeks)
- Calculate current pay period dynamically
- Add to existing filter controls

---

### REQ-005: Current Week Filter (P1)

Add quick filter for current week's timesheets.

**Features:**

- "This Week" quick filter button
- Shows only timesheets with `week_start` = current Sunday

**Implementation Notes:**

- Calculate current week's Sunday
- Add to existing filter controls alongside pay period filter

---

### REQ-006: Biweekly Pay Period Confirmation (P2)

Add confirmation step at end of pay period.

**Features:**

- Admin view showing all timesheets in pay period
- "Confirm Pay Period" action to lock/finalize
- Export all confirmed timesheets for payroll

**Implementation Notes:**

- May need new status or flag for "pay period confirmed"
- Prevents further edits after confirmation

---

## ⏱️ Time Entry Grid

### REQ-007: Column Totals (All Grids) (P1)

Show total hours for each day (column) in all Time Entry grids.

**Applies to:**

- Employee timesheet form
- Admin detail view
- Any other grid appearances

**Display:**

```
           Sun  Mon  Tue  Wed  Thu  Fri  Sat  | Row Total
Field        -   8    8    8    8    8    -   |    40
Internal     -   -    -    -    -    -    -   |     0
─────────────────────────────────────────────────────────
Day Total    0   8    8    8    8    8    0   |    40
```

---

### REQ-008: Row Totals (All Grids) (P1)

Show total hours for each hour type (row) in all Time Entry grids.

**Already Implemented:** Partial (only on submission summary)

**Needs:** Add to all grid appearances, not just summary view

---

### REQ-009: Auto-Populate Any Hour Type (P1)

Extend auto-populate feature to work with any hour type selection.

**Current:** Auto-populates 8h/day for Field Hours only

**Required:**

- User selects hour type from dropdown
- User checks "Auto-fill 8h Mon-Fri" checkbox
- System fills 8 hours for Mon-Fri for selected type

**Implementation Notes:**

- Already implemented for Field Hours
- Generalize to accept any selected hour type

---

## 📎 Attachments

### REQ-010: SharePoint Sync (P2)

Sync uploaded attachments to SharePoint for permanent storage.

**Features:**

- Background job to upload files to SharePoint document library
- Maintain local copy for immediate access
- Track sync status per attachment

**Implementation Notes:**

- Use Microsoft Graph API for SharePoint access
- Define folder structure in SharePoint
- Handle sync failures gracefully

---

## 🔔 Notifications

### REQ-011: Email Notifications (P1)

Send email notifications for timesheet events.

**Events:**

- Timesheet approved
- Timesheet marked "Needs Approval"
- Weekly reminder to submit (Friday)
- Admin: New timesheet submitted

**Implementation Notes:**

- Use Microsoft Graph API (M365 email)
- Respect user notification preferences
- Template-based emails

---

### REQ-012: Teams Bot Notifications (P2)

Extend existing Timesheet Bot to send all notification types.

**Events:**

- All events from REQ-011
- Interactive cards for approve/reject

**Implementation Notes:**

- See [BOT.md](BOT.md) for Teams bot architecture
- Requires Teams app registration

---

## 📝 Workflow

### REQ-013: Trainee Hour Type Restriction (P0)

Trainees can only select "Training" from the hour type dropdown.

**Implementation Notes:**

- Filter dropdown options based on `user.role`
- Backend validation to reject non-Training entries from trainees
- Show helpful message explaining restriction

---

### REQ-014: Submit Without Attachment (Warning) (P1)

Allow users to submit timesheets with Field Hours but no attachment.

**Current Behavior:** Blocks submission

**Required Behavior:**

- Show warning: "Field Hours require attachment"
- User can choose to submit anyway
- Timesheet auto-flags as "Needs Approval"
- Flag remains visible until attachment uploaded

**Implementation Notes:**

- Change from blocking to warning
- Auto-set status to NEEDS_APPROVAL on submit
- Already partially implemented (warning shows)

---

## 🔒 Authentication

### REQ-015: Azure AD User Sync (P2)

Sync user data (names, emails, roles) from Azure AD.

**Implementation Notes:**

- Use Microsoft Graph API to fetch user profiles
- Map Azure AD groups to app roles
- Periodic sync or on-demand during login

---

## ✅ Implementation Status

| Requirement | Status     | Notes                                 |
| ----------- | ---------- | ------------------------------------- |
| REQ-001     | 📋 Planned | Requires model changes                |
| REQ-002     | ✅ Partial | Admin account exists                  |
| REQ-003     | 📋 Planned | New feature                           |
| REQ-004     | 📋 Planned | Admin dashboard enhancement           |
| REQ-005     | 📋 Planned | Admin dashboard enhancement           |
| REQ-006     | 📋 Planned | New workflow                          |
| REQ-007     | 📋 Planned | Grid enhancement                      |
| REQ-008     | ✅ Partial | Exists in some views                  |
| REQ-009     | ✅ Partial | Works for Field, needs generalization |
| REQ-010     | 📋 Planned | SharePoint integration                |
| REQ-011     | 📋 Planned | Email service                         |
| REQ-012     | 📋 Planned | Teams bot                             |
| REQ-013     | 📋 Planned | Role-based filtering                  |
| REQ-014     | ✅ Partial | Warning exists, needs flow change     |
| REQ-015     | 📋 Planned | Azure AD integration                  |

---

_Document created January 7, 2026_
