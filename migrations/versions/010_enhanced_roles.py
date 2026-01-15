"""Add new role values for REQ-061 Enhanced Role System

Revision ID: 010_enhanced_roles
Revises: 009_add_teams_conversations
Create Date: 2026-01-15

REQ-061: Enhanced Five-Tier Role System
- Adds 'internal', 'engineer', 'approver' enum values
- Migrates 'staff' -> 'internal' (or user assignment)
- Migrates 'support' -> 'approver'
- Keeps old values for backwards compatibility during transition

Azure AD Group Mapping:
- NSTek-TimeTrainee  -> trainee
- NSTek-TimeInternal -> internal
- NSTek-TimeEngineer -> engineer
- NSTek-TimeApprover -> approver
- NSTek-TimeAdmins   -> admin
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '010_enhanced_roles'
down_revision = '009_add_teams_conversations'
branch_labels = None
depends_on = None


def upgrade():
    # Add new enum values to the existing userrole type
    # PostgreSQL requires ALTER TYPE to add new values
    
    # Add 'internal' value
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'internal'")
    
    # Add 'engineer' value  
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'engineer'")
    
    # Add 'approver' value
    op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'approver'")
    
    # Note: We keep 'staff' and 'support' as valid enum values for backwards
    # compatibility. The application code maps these to 'internal' and 'approver'
    # respectively. A separate manual migration or script should be run to 
    # update user roles based on Azure AD group membership.
    
    # Update server default to 'internal' (was 'staff')
    op.alter_column(
        'users',
        'role',
        server_default='internal'
    )


def downgrade():
    # PostgreSQL doesn't support removing enum values directly
    # The old values (staff, support) are still valid, just unused
    # Revert default to 'staff'
    op.alter_column(
        'users',
        'role', 
        server_default='staff'
    )
    
    # Note: Cannot remove enum values in PostgreSQL without recreating the type
    # This is acceptable as the old values work fine with the old code
