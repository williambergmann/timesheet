"""
Teams Conversation Model (REQ-012)

Stores conversation references for proactive Teams notifications.
"""

import uuid
from datetime import datetime
from ..extensions import db


class TeamsConversation(db.Model):
    """
    Conversation reference for a Teams user.
    """

    __tablename__ = "teams_conversations"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=True, unique=True
    )

    conversation_id = db.Column(db.String(255), nullable=False)
    service_url = db.Column(db.String(500), nullable=False)
    channel_id = db.Column(db.String(50), default="msteams")
    bot_id = db.Column(db.String(100), nullable=False)
    bot_name = db.Column(db.String(100), nullable=True)
    tenant_id = db.Column(db.String(100), nullable=True)

    teams_user_id = db.Column(db.String(255), unique=True, nullable=True)
    teams_user_name = db.Column(db.String(255), nullable=True)
    teams_user_principal = db.Column(db.String(255), index=True, nullable=True)

    last_activity = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="teams_conversation")

    def __repr__(self):
        return f"<TeamsConversation {self.user_id or self.teams_user_id}>"
