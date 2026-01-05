"""
Note Model

Notes/comments on timesheets from users or admins.
"""

import uuid
from datetime import datetime
from ..extensions import db


class Note(db.Model):
    """
    Note/comment on a timesheet.

    Both users and admins can add notes to timesheets.

    Attributes:
        id: Primary key (UUID)
        timesheet_id: Foreign key to Timesheet
        author_id: Foreign key to User who wrote the note
        content: Note text content
        created_at: When the note was created
    """

    __tablename__ = "notes"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timesheet_id = db.Column(
        db.String(36), db.ForeignKey("timesheets.id"), nullable=False, index=True
    )
    author_id = db.Column(
        db.String(36), db.ForeignKey("users.id"), nullable=False, index=True
    )
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    timesheet = db.relationship("Timesheet", back_populates="notes")
    author = db.relationship("User", back_populates="notes")

    def __repr__(self):
        return f"<Note {self.id}>"

    def to_dict(self):
        """Serialize note to dictionary."""
        return {
            "id": self.id,
            "author_id": self.author_id,
            "author_name": self.author.display_name if self.author else None,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }
