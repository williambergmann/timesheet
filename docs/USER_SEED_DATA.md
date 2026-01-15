# User Seed Data Guide

This document explains how to seed the Timesheet application with user data exported from Azure AD.

## Overview

The application uses a four-tier role system:

| Role        | Permissions                                         |
| ----------- | --------------------------------------------------- |
| **ADMIN**   | Full access: all hour types, approve all timesheets |
| **SUPPORT** | All hour types, can approve trainee timesheets only |
| **STAFF**   | All hour types, no approval rights                  |
| **TRAINEE** | Training hours only, no approval rights             |

## Current Role Assignments

Based on organizational requirements:

| Role            | Users                                          |
| --------------- | ---------------------------------------------- |
| **ADMIN** (3)   | Deven Patterson, Melissa Skow, Megan Patterson |
| **SUPPORT** (1) | Dominic Simonetti                              |
| **STAFF** (104) | All other @northstar-tek.com users             |
| **TRAINEE** (0) | To be assigned later via Azure AD groups       |

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

## Monitoring for New Users

Azure AD groups should be used to manage user roles:

- Monitor [Azure AD Users](https://portal.azure.com/#view/Microsoft_AAD_UsersAndTenants/UserManagementMenuBlade/~/AllUsers)
- New trainees will be added to a "Trainees" group
- New staff will be added to a "Staff" group

### Future Enhancement: Azure AD Group Sync

Consider implementing automatic sync based on Azure AD group membership:

- `Timesheet-Admins` → ADMIN role
- `Timesheet-Support` → SUPPORT role
- `Timesheet-Trainees` → TRAINEE role
- Default → STAFF role

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
