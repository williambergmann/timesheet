"""
Pytest Fixtures

Shared test fixtures for the timesheet application.
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal

from app import create_app
from app.config import TestingConfig
from app.extensions import db
from app.models import User, Timesheet, TimesheetEntry, Attachment, Note, Notification
from app.models.timesheet import TimesheetStatus, HourType


@pytest.fixture(scope="function")
def app():
    """Create application for testing."""
    application = create_app(TestingConfig)
    
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    """Create database session for testing."""
    with app.app_context():
        yield db.session


@pytest.fixture
def sample_user(app):
    """Create a sample regular user."""
    with app.app_context():
        user = User(
            azure_id="azure-user-123",
            email="user@northstar.com",
            display_name="Test User",
            phone="+15551234567",
            is_admin=False,
            sms_opt_in=True,
        )
        db.session.add(user)
        db.session.commit()
        
        # Return a dict with user data since the session may expire
        return {
            "id": user.id,
            "azure_id": user.azure_id,
            "email": user.email,
            "display_name": user.display_name,
            "is_admin": user.is_admin,
            "role": "staff",
        }


@pytest.fixture
def sample_admin(app):
    """Create a sample admin user."""
    with app.app_context():
        admin = User(
            azure_id="azure-admin-456",
            email="admin@northstar.com",
            display_name="Test Admin",
            phone="+15559876543",
            is_admin=True,
            sms_opt_in=True,
        )
        db.session.add(admin)
        db.session.commit()
        
        return {
            "id": admin.id,
            "azure_id": admin.azure_id,
            "email": admin.email,
            "display_name": admin.display_name,
            "is_admin": admin.is_admin,
            "role": "admin",
        }


@pytest.fixture
def auth_client(client, sample_user):
    """Create authenticated test client for regular user."""
    with client.session_transaction() as sess:
        sess["user"] = sample_user
    return client


@pytest.fixture
def admin_client(client, sample_admin):
    """Create authenticated test client for admin user."""
    with client.session_transaction() as sess:
        sess["user"] = sample_admin
    return client


@pytest.fixture
def sample_week_start():
    """Get a sample week start date (Sunday)."""
    today = date.today()
    # Get Sunday of current week
    days_since_sunday = (today.weekday() + 1) % 7
    return today - timedelta(days=days_since_sunday)


@pytest.fixture
def sample_timesheet(app, sample_user, sample_week_start):
    """Create a sample draft timesheet."""
    with app.app_context():
        timesheet = Timesheet(
            user_id=sample_user["id"],
            week_start=sample_week_start,
            status=TimesheetStatus.NEW,
        )
        db.session.add(timesheet)
        db.session.commit()
        
        return {
            "id": timesheet.id,
            "user_id": timesheet.user_id,
            "week_start": timesheet.week_start.isoformat(),
            "status": timesheet.status,
        }


@pytest.fixture
def sample_timesheet_with_entries(app, sample_user, sample_week_start):
    """Create a sample timesheet with entries."""
    with app.app_context():
        timesheet = Timesheet(
            user_id=sample_user["id"],
            week_start=sample_week_start,
            status=TimesheetStatus.NEW,
        )
        db.session.add(timesheet)
        db.session.flush()
        
        # Add entries for Mon-Fri
        for day_offset in range(1, 6):
            entry_date = sample_week_start + timedelta(days=day_offset)
            entry = TimesheetEntry(
                timesheet_id=timesheet.id,
                entry_date=entry_date,
                hour_type=HourType.FIELD,
                hours=Decimal("8.0"),
            )
            db.session.add(entry)
        
        db.session.commit()
        
        return {
            "id": timesheet.id,
            "user_id": timesheet.user_id,
            "week_start": timesheet.week_start.isoformat(),
            "status": timesheet.status,
        }


@pytest.fixture
def submitted_timesheet(app, sample_user, sample_week_start):
    """Create a submitted timesheet."""
    with app.app_context():
        # Use a different week to avoid conflicts
        week_start = sample_week_start - timedelta(weeks=1)
        
        timesheet = Timesheet(
            user_id=sample_user["id"],
            week_start=week_start,
            status=TimesheetStatus.SUBMITTED,
        )
        db.session.add(timesheet)
        db.session.flush()
        
        # Add 40 hours of internal work (no attachment required)
        for day_offset in range(1, 6):
            entry_date = week_start + timedelta(days=day_offset)
            entry = TimesheetEntry(
                timesheet_id=timesheet.id,
                entry_date=entry_date,
                hour_type=HourType.INTERNAL,
                hours=Decimal("8.0"),
            )
            db.session.add(entry)
        
        db.session.commit()
        
        return {
            "id": timesheet.id,
            "user_id": timesheet.user_id,
            "week_start": week_start.isoformat(),
            "status": timesheet.status,
        }


@pytest.fixture
def approved_timesheet(app, sample_user, sample_admin, sample_week_start):
    """Create an approved timesheet."""
    with app.app_context():
        # Use a different week to avoid conflicts
        week_start = sample_week_start - timedelta(weeks=2)
        
        timesheet = Timesheet(
            user_id=sample_user["id"],
            week_start=week_start,
            status=TimesheetStatus.APPROVED,
            approved_by=sample_admin["id"],
        )
        db.session.add(timesheet)
        db.session.commit()
        
        return {
            "id": timesheet.id,
            "user_id": timesheet.user_id,
            "week_start": week_start.isoformat(),
            "status": timesheet.status,
        }


@pytest.fixture
def needs_approval_timesheet(app, sample_user, sample_week_start):
    """Create a NEEDS_APPROVAL timesheet (field hours without attachment)."""
    with app.app_context():
        # Use a different week to avoid conflicts
        week_start = sample_week_start - timedelta(weeks=3)
        
        timesheet = Timesheet(
            user_id=sample_user["id"],
            week_start=week_start,
            status=TimesheetStatus.NEEDS_APPROVAL,
        )
        db.session.add(timesheet)
        db.session.flush()
        
        # Add 40 hours of field work (requires attachment)
        for day_offset in range(1, 6):
            entry_date = week_start + timedelta(days=day_offset)
            entry = TimesheetEntry(
                timesheet_id=timesheet.id,
                entry_date=entry_date,
                hour_type=HourType.FIELD,
                hours=Decimal("8.0"),
            )
            db.session.add(entry)
        
        db.session.commit()
        
        return {
            "id": timesheet.id,
            "user_id": timesheet.user_id,
            "week_start": week_start.isoformat(),
            "status": timesheet.status,
        }
