"""Add role column to users table

Revision ID: 002_add_user_role
Revises: 13fe1c13ccd1
Create Date: 2026-01-07

REQ-001: Four-Tier Role System
- Adds 'role' enum column (trainee, staff, support, admin)
- Migrates existing is_admin=True users to 'admin' role
- Migrates existing is_admin=False users to 'staff' role
- Keeps is_admin column for backwards compatibility
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_user_role'
down_revision = '13fe1c13ccd1'
branch_labels = None
depends_on = None


def upgrade():
    # Drop any existing enum type first to ensure clean state
    op.execute("DROP TYPE IF EXISTS userrole CASCADE")
    # Create the enum type with lowercase values matching Python UserRole enum
    op.execute("CREATE TYPE userrole AS ENUM ('trainee', 'staff', 'support', 'admin')")
    
    # Add the role column with default 'staff'
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.Enum('trainee', 'staff', 'support', 'admin', name='userrole', create_type=False),
            nullable=True  # Temporarily nullable for migration
        )
    )
    
    # Migrate existing data: is_admin=True -> 'admin', else -> 'staff'
    op.execute("""
        UPDATE users 
        SET role = CASE 
            WHEN is_admin = true THEN 'admin'::userrole
            ELSE 'staff'::userrole
        END
    """)
    
    # Now make the column non-nullable with default
    op.alter_column(
        'users',
        'role',
        nullable=False,
        server_default='staff'
    )


def downgrade():
    # Remove the role column
    op.drop_column('users', 'role')
    
    # Drop the enum type
    op.execute("DROP TYPE IF EXISTS userrole")

