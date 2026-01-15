"""
User Model

Stores user information synced from Microsoft 365.
"""

import enum
import uuid
from datetime import datetime
from ..extensions import db


class UserRole(enum.Enum):
    """
    Five-tier role system for user permissions.

    Role Hierarchy (REQ-061):
        TRAINEE  - Can only submit Training hours, no approval rights
        INTERNAL - Can submit Internal, PTO, Holiday, Unpaid (not Field/Training)
        ENGINEER - Can submit Field, PTO, Holiday, Unpaid (not Internal/Training)
        APPROVER - Can submit all hour types, can approve TRAINEE + ENGINEER
        ADMIN    - Full access: all hour types, approve all timesheets

    Azure AD Group Mapping:
        NSTek-TimeTrainee  -> TRAINEE
        NSTek-TimeInternal -> INTERNAL
        NSTek-TimeEngineer -> ENGINEER
        NSTek-TimeApprover -> APPROVER
        NSTek-TimeAdmins   -> ADMIN

    See REQ-061 in docs/REQUIREMENTS.md for details.
    """

    TRAINEE = "trainee"
    INTERNAL = "internal"
    ENGINEER = "engineer"
    APPROVER = "approver"
    ADMIN = "admin"

    # Legacy values for migration compatibility
    STAFF = "staff"      # Maps to INTERNAL
    SUPPORT = "support"  # Maps to APPROVER

    @classmethod
    def from_string(cls, value):
        """Convert string to UserRole enum, handling legacy values."""
        if isinstance(value, cls):
            return value
        try:
            val = value.lower()
            # Map legacy values to new roles
            if val == "staff":
                return cls.INTERNAL
            if val == "support":
                return cls.APPROVER
            return cls(val)
        except (ValueError, AttributeError):
            return cls.INTERNAL  # Default to internal

    def can_approve_trainee(self):
        """Check if role can approve trainee timesheets."""
        return self in (UserRole.APPROVER, UserRole.ADMIN)

    def can_approve_engineer(self):
        """Check if role can approve engineer timesheets."""
        return self in (UserRole.APPROVER, UserRole.ADMIN)

    def can_approve_all(self):
        """Check if role can approve all timesheets."""
        return self == UserRole.ADMIN

    def is_admin(self):
        """Check if role has admin privileges."""
        return self == UserRole.ADMIN

    def is_approver(self):
        """Check if role has approver privileges."""
        return self in (UserRole.APPROVER, UserRole.ADMIN)

    def get_allowed_hour_types(self):
        """
        Get list of hour types this role can use.

        Hour Type Permissions:
        - TRAINEE:  Training only
        - INTERNAL: Internal, PTO, Holiday, Unpaid
        - ENGINEER: Field, PTO, Holiday, Unpaid
        - APPROVER: All types
        - ADMIN:    All types
        """
        if self == UserRole.TRAINEE:
            return ["Training"]
        if self == UserRole.INTERNAL or self == UserRole.STAFF:
            return ["Internal", "PTO", "Holiday", "Unpaid"]
        if self == UserRole.ENGINEER:
            return ["Field", "PTO", "Holiday", "Unpaid"]
        # APPROVER, ADMIN, SUPPORT get all types
        return ["Field", "Internal", "Training", "PTO", "Holiday", "Unpaid"]


class User(db.Model):
    """
    User model for employees.

    Users are synced from Microsoft 365/Azure AD. The azure_id links
    to their Microsoft identity for authentication.

    Attributes:
        id: Primary key (UUID)
        azure_id: Microsoft 365 user ID (unique)
        email: User's email address (unique)
        display_name: User's display name
        phone: Phone number for Twilio SMS notifications
        role: User's role (trainee, staff, support, admin)
        sms_opt_in: Whether user has opted into SMS notifications
        email_opt_in: Whether user has opted into email notifications
        teams_opt_in: Whether user has opted into Teams notifications
        notification_emails: List of email addresses for notifications
        notification_phones: List of phone numbers for notifications
        teams_account: Teams account email/identifier (if connected)
        created_at: When the user record was created
        updated_at: Last modification time
    """

    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    azure_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    # Role field - replaces is_admin boolean
    # Use values_callable to store the enum value (lowercase) not the name (uppercase)
    role = db.Column(
        db.Enum(
            UserRole, 
            values_callable=lambda x: [e.value for e in x],
            name='userrole',
            create_type=False  # Type already exists from migration
        ),
        default=UserRole.INTERNAL,
        nullable=False
    )
    # Keep is_admin for backwards compatibility during migration
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    sms_opt_in = db.Column(db.Boolean, default=True, nullable=False)
    email_opt_in = db.Column(db.Boolean, default=True, nullable=False)
    teams_opt_in = db.Column(db.Boolean, default=True, nullable=False)
    notification_emails = db.Column(db.JSON, nullable=True)
    notification_phones = db.Column(db.JSON, nullable=True)
    teams_account = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    timesheets = db.relationship(
        "Timesheet",
        back_populates="user",
        lazy="dynamic",
        foreign_keys="Timesheet.user_id",
    )
    notifications = db.relationship(
        "Notification", back_populates="user", lazy="dynamic"
    )
    notes = db.relationship("Note", back_populates="author", lazy="dynamic")
    teams_conversation = db.relationship(
        "TeamsConversation", back_populates="user", uselist=False
    )

    def __repr__(self):
        return f"<User {self.email}>"

    @property
    def is_admin_role(self):
        """Check if user has admin role."""
        return self.role == UserRole.ADMIN

    @property
    def is_approver_role(self):
        """Check if user has approver role."""
        return self.role in (UserRole.APPROVER, UserRole.SUPPORT, UserRole.ADMIN)

    def can_approve(self, target_user=None):
        """
        Check if this user can approve another user's timesheet.

        Approval Matrix (REQ-061):
        - ADMIN: Can approve all timesheets
        - APPROVER: Can approve TRAINEE and ENGINEER timesheets only
        - Others: Cannot approve any timesheets

        Args:
            target_user: The user whose timesheet is being approved

        Returns:
            bool: True if this user can approve the target's timesheet
        """
        if self.role == UserRole.ADMIN:
            return True
        if self.role in (UserRole.APPROVER, UserRole.SUPPORT) and target_user:
            # APPROVER can only approve TRAINEE and ENGINEER timesheets
            return target_user.role in (UserRole.TRAINEE, UserRole.ENGINEER)
        return False

    def get_allowed_hour_types(self):
        """Get list of hour types this user can submit."""
        return self.role.get_allowed_hour_types()

    def get_notification_emails(self):
        """Get list of notification emails with primary email fallback."""
        if self.notification_emails is not None:
            return list(self.notification_emails)
        return [self.email] if self.email else []

    def get_notification_phones(self):
        """Get list of notification phones with primary phone fallback."""
        if self.notification_phones is not None:
            return list(self.notification_phones)
        return [self.phone] if self.phone else []

    def to_dict(self):
        """Serialize user to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "display_name": self.display_name,
            "role": self.role.value if self.role else "staff",
            "is_admin": self.role == UserRole.ADMIN if self.role else self.is_admin,
            "allowed_hour_types": self.get_allowed_hour_types(),
            "sms_opt_in": self.sms_opt_in,
            "email_opt_in": self.email_opt_in,
            "teams_opt_in": self.teams_opt_in,
            "notification_emails": self.get_notification_emails(),
            "notification_phones": self.get_notification_phones(),
            "teams_account": self.teams_account,
        }
