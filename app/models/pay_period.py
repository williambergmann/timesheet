"""
Pay Period Model

Tracks confirmed biweekly pay periods (REQ-006).
"""

import uuid
from datetime import datetime
from ..extensions import db


class PayPeriod(db.Model):
    """
    Confirmed pay period record.

    Attributes:
        id: Primary key (UUID)
        start_date: Sunday start date of the pay period
        end_date: End date of the pay period (Saturday, 13 days later)
        confirmed_at: When the pay period was confirmed
        confirmed_by: User ID of confirming admin
    """

    __tablename__ = "pay_periods"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    start_date = db.Column(db.Date, nullable=False, unique=True, index=True)
    end_date = db.Column(db.Date, nullable=False, index=True)
    confirmed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    confirmed_by = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    confirmer = db.relationship("User")

    def to_dict(self):
        """Serialize pay period to dictionary."""
        return {
            "id": self.id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "confirmed_at": self.confirmed_at.isoformat() if self.confirmed_at else None,
            "confirmed_by": self.confirmed_by,
            "confirmed_by_name": self.confirmer.display_name if self.confirmer else None,
        }
