#!/usr/bin/env python3
"""
User Seed Script for Northstar Timesheet App

This script reads the Azure AD exported users CSV and generates SQL INSERT statements
for seeding the users table with initial data.

Usage:
    python scripts/seed_users.py [csv_file] > seed_users.sql
    
    Or import and use programmatically:
    from scripts.seed_users import process_users_csv, generate_sql_inserts
    
Role Assignments (REQ-061):
    - ADMIN: Deven Patterson, Melissa Skow, Megan Patterson
    - APPROVER: Dominic Simonetti
    - ENGINEER: Assigned via NSTek-TimeEngineer group
    - INTERNAL: Default for all other @northstar-tek.com users
    - TRAINEE: Assigned via NSTek-TimeTrainee group

Azure AD Group Mapping:
    - NSTek-TimeAdmins   -> admin
    - NSTek-TimeApprover -> approver  
    - NSTek-TimeEngineer -> engineer
    - NSTek-TimeInternal -> internal
    - NSTek-TimeTrainee  -> trainee

Note: Only @northstar-tek.com emails are included to avoid duplicates.
"""

import csv
import sys
import uuid
from datetime import datetime

# Role assignments - normalized to lowercase for matching
ADMIN_USERS = {
    'deven patterson',
    'melissa skow',
    'megan patterson',
}

APPROVER_USERS = {
    'dominic simonetti',
}

ENGINEER_USERS = set()  # Populate from NSTek-TimeEngineer group membership

TRAINEE_USERS = set()  # Populate from NSTek-TimeTrainee group membership

# Service accounts and non-person entries to exclude
EXCLUDE_USERS = {
    'account manager',
    'northstar assistant',
    'northstar recruiter',
    'northstar technologies inc.',
    'packet tracer',
    'phone interviews',
    'timecards',
    'share account',
    'sl recruiting',
    'dmarc reports',
    'fred flinstone',  # Test account
    'joe kerr',  # Test account (Joker)
}


def get_role(display_name: str) -> str:
    """Determine user role based on display name (REQ-061)."""
    name_lower = display_name.lower().strip()
    
    if name_lower in ADMIN_USERS:
        return 'admin'
    elif name_lower in APPROVER_USERS:
        return 'approver'
    elif name_lower in ENGINEER_USERS:
        return 'engineer'
    elif name_lower in TRAINEE_USERS:
        return 'trainee'
    else:
        return 'internal'  # Default role


def should_include_user(display_name: str, email: str) -> bool:
    """Check if user should be included in the seed."""
    name_lower = display_name.lower().strip()
    
    # Exclude service accounts
    if name_lower in EXCLUDE_USERS:
        return False
    
    # Only include @northstar-tek.com emails
    if '@northstar-tek.com' not in email.lower():
        return False
    
    return True


def normalize_email(email: str) -> str:
    """Normalize email to lowercase."""
    return email.lower().strip()


def process_users_csv(csv_path: str) -> list:
    """
    Process the Azure AD export CSV and return unique users.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        List of user dictionaries with id, display_name, email, role
    """
    users = {}
    
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            azure_id = row.get('id', '').strip()
            display_name = row.get('displayName', '').strip()
            email = row.get('userPrincipalName', '').strip()
            
            if not all([azure_id, display_name, email]):
                continue
            
            if not should_include_user(display_name, email):
                continue
            
            # Use lowercase name as key to deduplicate
            name_key = display_name.lower().strip()
            
            # Keep the first entry for each user (or the shorter email)
            if name_key not in users:
                users[name_key] = {
                    'azure_id': azure_id,
                    'display_name': display_name,
                    'email': normalize_email(email),
                    'role': get_role(display_name),
                }
            else:
                # If this email is shorter/cleaner, use it instead
                current_email = users[name_key]['email']
                new_email = normalize_email(email)
                if len(new_email) < len(current_email):
                    users[name_key]['email'] = new_email
                    users[name_key]['azure_id'] = azure_id
    
    return list(users.values())


def generate_sql_inserts(users: list) -> str:
    """Generate SQL INSERT statements for users."""
    lines = [
        "-- Northstar Timesheet User Seed Data",
        f"-- Generated: {datetime.now().isoformat()}",
        f"-- Total users: {len(users)}",
        "",
        "-- Role distribution:",
    ]
    
    # Count roles
    role_counts = {}
    for user in users:
        role = user['role']
        role_counts[role] = role_counts.get(role, 0) + 1
    
    for role, count in sorted(role_counts.items()):
        lines.append(f"--   {role.upper()}: {count}")
    
    lines.append("")
    lines.append("-- Insert users (ON CONFLICT DO NOTHING to avoid duplicates)")
    lines.append("")
    
    for user in sorted(users, key=lambda x: x['display_name']):
        user_id = str(uuid.uuid4())
        sql = f"""INSERT INTO users (id, azure_id, email, display_name, role, is_admin, sms_opt_in, email_opt_in, teams_opt_in, created_at, updated_at)
VALUES ('{user_id}', '{user['azure_id']}', '{user['email']}', '{user['display_name'].replace("'", "''")}', '{user['role']}', {str(user['role'] == 'admin').lower()}, true, true, true, NOW(), NOW())
ON CONFLICT (email) DO NOTHING;"""
        lines.append(sql)
        lines.append("")
    
    return '\n'.join(lines)


def generate_python_fixtures(users: list) -> str:
    """Generate Python fixture data for testing."""
    lines = [
        "# Northstar Timesheet User Fixtures",
        f"# Generated: {datetime.now().isoformat()}",
        "",
        "USERS = [",
    ]
    
    for user in sorted(users, key=lambda x: x['display_name']):
        lines.append(f"    {{")
        lines.append(f"        'azure_id': '{user['azure_id']}',")
        lines.append(f"        'email': '{user['email']}',")
        lines.append(f"        'display_name': '{user['display_name']}',")
        lines.append(f"        'role': '{user['role']}',")
        lines.append(f"    }},")
    
    lines.append("]")
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        csv_path = 'exportUsers_2026-1-15.csv'
    else:
        csv_path = sys.argv[1]
    
    print(f"-- Processing: {csv_path}", file=sys.stderr)
    
    users = process_users_csv(csv_path)
    
    print(f"-- Found {len(users)} unique users", file=sys.stderr)
    
    # Print role summary
    role_counts = {}
    for user in users:
        role = user['role']
        role_counts[role] = role_counts.get(role, 0) + 1
    
    for role, count in sorted(role_counts.items()):
        print(f"--   {role.upper()}: {count}", file=sys.stderr)
    
    # Generate and print SQL
    sql = generate_sql_inserts(users)
    print(sql)


if __name__ == '__main__':
    main()
