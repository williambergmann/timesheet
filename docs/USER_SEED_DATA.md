# User Seed Data Guide

This document explains how to seed the Timesheet application with user data exported from Azure AD.

## Overview

The application uses a **five-tier role system** mapped to Azure AD security groups:

| Role         | Azure AD Group     | Allowed Hour Types             | Approval Rights                 |
| ------------ | ------------------ | ------------------------------ | ------------------------------- |
| **ADMIN**    | NSTek-TimeAdmins   | All types                      | Approve ALL timesheets          |
| **APPROVER** | NSTek-TimeApprover | All types                      | Approve TRAINEE + ENGINEER only |
| **ENGINEER** | NSTek-TimeEngineer | Field, PTO, Holiday, Unpaid    | None                            |
| **INTERNAL** | NSTek-TimeInternal | Internal, PTO, Holiday, Unpaid | None                            |
| **TRAINEE**  | NSTek-TimeTrainee  | Training only                  | None                            |

**Hour Type Restrictions:**

- **ENGINEER**: Cannot log Internal or Training hours
- **INTERNAL**: Cannot log Field or Training hours
- **TRAINEE**: Can only log Training hours

## Current Role Assignments

Based on organizational requirements (pending migration to new system):

| Role         | Count | Users                                          |
| ------------ | ----- | ---------------------------------------------- |
| **ADMIN**    | 3     | Deven Patterson, Melissa Skow, Megan Patterson |
| **APPROVER** | 1     | Dominic Simonetti                              |
| **ENGINEER** | TBD   | Members of NSTek-TimeEngineer group            |
| **INTERNAL** | TBD   | Members of NSTek-TimeInternal group            |
| **TRAINEE**  | TBD   | Members of NSTek-TimeTrainee group             |

## Files

| File                        | Description                                   |
| --------------------------- | --------------------------------------------- |
| `exportUsers_2026-1-15.csv` | Azure AD user export (source data)            |
| `scripts/seed_users.py`     | Python script to process CSV and generate SQL |
| `scripts/seed_users.sql`    | Generated SQL INSERT statements               |

## Generating Seed Data

### 1. Export Users from Azure AD

1. Go to [Azure AD Users](https://portal.azure.com/#view/Microsoft_AAD_UsersAndTenants/UserManagementMenuBlade/~/AllUsers)
2. Click "Download users" or "Bulk operations" → "Download users"
3. Save the CSV file to the project root

### 2. Generate SQL from CSV

```bash
# Generate SQL file
python3 scripts/seed_users.py exportUsers_2026-1-15.csv > scripts/seed_users.sql

# Preview output
head -50 scripts/seed_users.sql
```

### 3. Apply to Database

#### Local Development

```bash
# Using Flask shell
flask shell
>>> from scripts.seed_users import process_users_csv
>>> users = process_users_csv('exportUsers_2026-1-15.csv')
>>> # Then insert using SQLAlchemy
```

#### Production Server (Docker)

```bash
# SSH to server
ssh nstadmin@172.17.2.27

# Copy SQL file to server
scp scripts/seed_users.sql nstadmin@172.17.2.27:~/timesheet/

# Run SQL in PostgreSQL container
cd ~/timesheet
docker exec -i timesheet-prod-db-1 psql -U timesheet -d timesheet < seed_users.sql
```

#### Alternative: Flask CLI Command

```bash
# If you add a custom CLI command
flask seed-users exportUsers_2026-1-15.csv
```

## Updating Role Assignments

### Modify Role Mappings

Edit `scripts/seed_users.py` to change role assignments:

```python
# Role assignments - normalized to lowercase for matching
ADMIN_USERS = {
    'deven patterson',
    'melissa skow',
    'megan patterson',
}

SUPPORT_USERS = {
    'dominic simonetti',
}
```

### Add Trainees

When trainee group is established:

```python
TRAINEE_USERS = {
    'new trainee name',
    'another trainee',
}
```

Then update `get_role()` function:

```python
def get_role(display_name: str) -> str:
    name_lower = display_name.lower().strip()

    if name_lower in ADMIN_USERS:
        return 'admin'
    elif name_lower in SUPPORT_USERS:
        return 'support'
    elif name_lower in TRAINEE_USERS:
        return 'trainee'
    else:
        return 'staff'
```

## Azure AD Security Groups

The following Azure AD security groups control user roles in the Timesheet app:

| Azure AD Group         | Timesheet Role | Description                                            |
| ---------------------- | -------------- | ------------------------------------------------------ |
| **NSTek-TimeAdmins**   | ADMIN          | Full access: all hour types, approve all timesheets    |
| **NSTek-TimeEngineer** | STAFF          | Professional staff: all hour types, no approval rights |
| **NSTek-TimeInternal** | STAFF          | Internal staff: all hour types, no approval rights     |
| **NSTek-TimeTrainee**  | TRAINEE        | Trainees: Training hours only, no approval rights      |

### Group Management URLs

- **All Groups**: https://portal.azure.com/#view/Microsoft_AAD_IAM/GroupsManagementMenuBlade/~/AllGroups
- **All Users**: https://portal.azure.com/#view/Microsoft_AAD_UsersAndTenants/UserManagementMenuBlade/~/AllUsers

### Monitoring for New Users

1. **Watch for new trainees** added to `NSTek-TimeTrainee`
2. **Watch for promotions** from trainee to staff (move to `NSTek-TimeEngineer` or `NSTek-TimeInternal`)
3. **Watch for new admins** added to `NSTek-TimeAdmins`

### Future Enhancement: Azure AD Group Sync

Consider implementing automatic sync based on Azure AD group membership:

```python
# Proposed group-to-role mapping
AZURE_GROUP_ROLES = {
    'NSTek-TimeAdmins': 'admin',
    'NSTek-TimeEngineer': 'staff',
    'NSTek-TimeInternal': 'staff',
    'NSTek-TimeTrainee': 'trainee',
}
```

This would require:

1. Microsoft Graph API access to query group memberships
2. A scheduled job to sync group memberships to user roles
3. API permissions: `GroupMember.Read.All` or `Group.Read.All`

## Excluded Accounts

Service accounts and test accounts are automatically excluded:

- Account Manager
- Northstar Assistant / Recruiter
- Packet Tracer
- Phone Interviews
- Timecards
- Share Account
- DMARC Reports
- Test accounts (Fred Flinstone, Joe Kerr)

## Notes

1. **Deduplication**: Users with multiple email aliases (e.g., `dsimonetti@` and `dominic.simonetti@`) are deduplicated, keeping the shorter email.

2. **ON CONFLICT**: SQL uses `ON CONFLICT (email) DO NOTHING` to prevent duplicate insertion errors.

3. **Azure ID**: The Azure AD object ID is stored to link back to Microsoft 365 identity.

4. **Notifications**: All users default to `sms_opt_in=true`, `email_opt_in=true`, `teams_opt_in=true`.
