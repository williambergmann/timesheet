"""Add Teams conversations table (REQ-012)

Revision ID: 009_add_teams_conversations
Revises: 008_add_sharepoint_sync_fields
Create Date: 2026-01-09
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "009_add_teams_conversations"
down_revision = "008_add_sharepoint_sync_fields"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "teams_conversations",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), unique=True, nullable=True),
        sa.Column("conversation_id", sa.String(length=255), nullable=False),
        sa.Column("service_url", sa.String(length=500), nullable=False),
        sa.Column("channel_id", sa.String(length=50), nullable=True),
        sa.Column("bot_id", sa.String(length=100), nullable=False),
        sa.Column("bot_name", sa.String(length=100), nullable=True),
        sa.Column("tenant_id", sa.String(length=100), nullable=True),
        sa.Column("teams_user_id", sa.String(length=255), nullable=True, unique=True),
        sa.Column("teams_user_name", sa.String(length=255), nullable=True),
        sa.Column("teams_user_principal", sa.String(length=255), nullable=True),
        sa.Column("last_activity", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index(
        "ix_teams_conversations_teams_user_principal",
        "teams_conversations",
        ["teams_user_principal"],
        unique=False,
    )


def downgrade():
    op.drop_index("ix_teams_conversations_teams_user_principal", table_name="teams_conversations")
    op.drop_table("teams_conversations")
