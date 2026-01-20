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
down_revision = '009_teams_convos'
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
    # respectively.
    #
    # We do NOT change the server_default here because PostgreSQL requires that
    # new enum values be committed before they can be used. The old 'staff' 
    # default continues to work since we have backwards compatibility in the
    # application layer.


def downgrade():
    # PostgreSQL doesn't support removing enum values directly
    # The old values (staff, support) are still valid
    # Since we only added enum values and didn't change defaults, nothing to revert
    pass
