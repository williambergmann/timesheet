"""
Model Tests

Unit tests for database models and business logic.
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal

from app.extensions import db
from app.models import User, Timesheet, TimesheetEntry, Attachment, Note
from app.models.timesheet import TimesheetStatus, HourType, ReimbursementType


class TestUserModel:
    """Tests for User model."""

    def test_create_user(self, app):
        """Test creating a user."""
        with app.app_context():
            user = User(
                azure_id="test-azure-id",
                email="test@example.com",
                display_name="Test User",
            )
            db.session.add(user)
            db.session.commit()

            assert user.id is not None
            assert user.email == "test@example.com"
            assert user.is_admin is False
            assert user.sms_opt_in is True  # Default

    def test_user_repr(self, app, sample_user):
        """Test user string representation."""
        with app.app_context():
            user = User.query.get(sample_user["id"])
            assert "user@northstar.com" in repr(user)

    def test_user_to_dict(self, app, sample_user):
        """Test user serialization."""
        with app.app_context():
            user = User.query.get(sample_user["id"])
            data = user.to_dict()

            assert data["id"] == sample_user["id"]
            assert data["email"] == "user@northstar.com"
            assert data["is_admin"] is False
            assert "phone" not in data  # Phone should not be serialized

    def test_unique_email_constraint(self, app, sample_user):
        """Test unique email constraint."""
        with app.app_context():
            duplicate = User(
                azure_id="different-azure-id",
                email="user@northstar.com",  # Same email
                display_name="Another User",
            )
            db.session.add(duplicate)
            
            with pytest.raises(Exception):  # IntegrityError
                db.session.commit()


class TestTimesheetModel:
    """Tests for Timesheet model."""

    def test_create_timesheet(self, app, sample_user, sample_week_start):
        """Test creating a timesheet."""
        with app.app_context():
            timesheet = Timesheet(
                user_id=sample_user["id"],
                week_start=sample_week_start,
            )
            db.session.add(timesheet)
            db.session.commit()

            assert timesheet.id is not None
            assert timesheet.status == TimesheetStatus.NEW
            assert timesheet.traveled is False
            assert timesheet.has_expenses is False

    def test_timesheet_repr(self, app, sample_timesheet):
        """Test timesheet string representation."""
        with app.app_context():
            timesheet = Timesheet.query.get(sample_timesheet["id"])
            assert sample_timesheet["id"] in repr(timesheet)

    def test_timesheet_to_dict(self, app, sample_timesheet):
        """Test timesheet serialization."""
        with app.app_context():
            timesheet = Timesheet.query.get(sample_timesheet["id"])
            data = timesheet.to_dict()

            assert data["id"] == sample_timesheet["id"]
            assert data["status"] == TimesheetStatus.NEW
            assert "totals" in data
            assert "entries" in data

    def test_unique_user_week_constraint(self, app, sample_user, sample_week_start, sample_timesheet):
        """Test unique user+week constraint."""
        with app.app_context():
            duplicate = Timesheet(
                user_id=sample_user["id"],
                week_start=sample_week_start,  # Same week
            )
            db.session.add(duplicate)
            
            with pytest.raises(Exception):  # IntegrityError
                db.session.commit()


class TestTimesheetCalculations:
    """Tests for timesheet calculation methods."""

    def test_calculate_totals_empty(self, app, sample_timesheet):
        """Test calculating totals for empty timesheet."""
        with app.app_context():
            timesheet = Timesheet.query.get(sample_timesheet["id"])
            totals = timesheet.calculate_totals()

            assert totals["total"] == Decimal("0")
            assert totals["payable"] == Decimal("0")
            assert totals["billable"] == Decimal("0")
            assert totals["unpaid"] == Decimal("0")

    def test_calculate_totals_with_entries(self, app, sample_timesheet_with_entries):
        """Test calculating totals with field hours."""
        with app.app_context():
            timesheet = Timesheet.query.get(sample_timesheet_with_entries["id"])
            totals = timesheet.calculate_totals()

            # 5 days * 8 hours = 40 hours
            assert totals["total"] == Decimal("40.0")
            assert totals["payable"] == Decimal("40.0")  # Field is payable
            assert totals["billable"] == Decimal("40.0")  # Field is billable

    def test_calculate_totals_mixed_hours(self, app, sample_user, sample_week_start):
        """Test calculating totals with mixed hour types."""
        with app.app_context():
            # Use different week to avoid conflict
            week_start = sample_week_start - timedelta(weeks=3)
            
            timesheet = Timesheet(
                user_id=sample_user["id"],
                week_start=week_start,
            )
            db.session.add(timesheet)
            db.session.flush()

            # Add mixed entries
            entries = [
                (HourType.FIELD, 16),      # Payable, Billable
                (HourType.INTERNAL, 8),    # Payable, Not Billable
                (HourType.TRAINING, 4),    # Not Payable, Not Billable (Unpaid)
                (HourType.PTO, 8),          # Payable, Not Billable
            ]
            
            entry_date = week_start + timedelta(days=1)
            for hour_type, hours in entries:
                entry = TimesheetEntry(
                    timesheet_id=timesheet.id,
                    entry_date=entry_date,
                    hour_type=hour_type,
                    hours=Decimal(str(hours)),
                )
                db.session.add(entry)
            
            db.session.commit()

            totals = timesheet.calculate_totals()

            assert totals["total"] == Decimal("36.0")      # 16 + 8 + 4 + 8
            assert totals["payable"] == Decimal("32.0")    # 16 + 8 + 8 (not training)
            assert totals["billable"] == Decimal("16.0")   # Only field
            assert totals["unpaid"] == Decimal("4.0")      # Only training

    def test_requires_attachment_with_field_hours(self, app, sample_timesheet_with_entries):
        """Test requires_attachment with field hours and no attachment."""
        with app.app_context():
            timesheet = Timesheet.query.get(sample_timesheet_with_entries["id"])
            
            assert timesheet.requires_attachment() is True

    def test_requires_attachment_with_attachment(self, app, sample_timesheet_with_entries):
        """Test requires_attachment when attachment exists."""
        with app.app_context():
            timesheet = Timesheet.query.get(sample_timesheet_with_entries["id"])
            
            # Add an attachment
            attachment = Attachment(
                timesheet_id=timesheet.id,
                filename="test.pdf",
                original_filename="test.pdf",
                mime_type="application/pdf",
                file_size=1024,
            )
            db.session.add(attachment)
            db.session.commit()
            
            assert timesheet.requires_attachment() is False

    def test_requires_attachment_no_field_hours(self, app, submitted_timesheet):
        """Test requires_attachment with no field hours."""
        with app.app_context():
            timesheet = Timesheet.query.get(submitted_timesheet["id"])
            
            # This timesheet has only internal hours
            assert timesheet.requires_attachment() is False


class TestTimesheetEntry:
    """Tests for TimesheetEntry model."""

    def test_create_entry(self, app, sample_timesheet, sample_week_start):
        """Test creating a timesheet entry."""
        with app.app_context():
            entry = TimesheetEntry(
                timesheet_id=sample_timesheet["id"],
                entry_date=sample_week_start + timedelta(days=1),
                hour_type=HourType.FIELD,
                hours=Decimal("8.0"),
            )
            db.session.add(entry)
            db.session.commit()

            assert entry.id is not None
            assert entry.hours == Decimal("8.0")

    def test_entry_to_dict(self, app, sample_timesheet, sample_week_start):
        """Test entry serialization."""
        with app.app_context():
            entry_date = sample_week_start + timedelta(days=1)
            entry = TimesheetEntry(
                timesheet_id=sample_timesheet["id"],
                entry_date=entry_date,
                hour_type=HourType.PTO,
                hours=Decimal("4.5"),
            )
            db.session.add(entry)
            db.session.commit()

            data = entry.to_dict()
            assert data["hour_type"] == HourType.PTO
            assert data["hours"] == 4.5


class TestHourTypeConfig:
    """Tests for hour type configuration."""

    def test_field_hours_config(self):
        """Test Field hours configuration."""
        config = HourType.CONFIG[HourType.FIELD]
        assert config["payable"] is True
        assert config["billable"] is True
        assert config["requires_attachment"] is True

    def test_internal_hours_config(self):
        """Test Internal hours configuration."""
        config = HourType.CONFIG[HourType.INTERNAL]
        assert config["payable"] is True
        assert config["billable"] is False
        assert config["requires_attachment"] is False

    def test_training_hours_config(self):
        """Test Training hours configuration."""
        config = HourType.CONFIG[HourType.TRAINING]
        assert config["payable"] is False
        assert config["billable"] is False
        assert config["requires_attachment"] is False

    def test_pto_hours_config(self):
        """Test PTO hours configuration."""
        config = HourType.CONFIG[HourType.PTO]
        assert config["payable"] is True
        assert config["billable"] is False
        assert config["requires_attachment"] is False

    def test_all_hour_types_defined(self):
        """Test all hour types have configuration."""
        for hour_type in HourType.ALL:
            assert hour_type in HourType.CONFIG


class TestTimesheetStatus:
    """Tests for timesheet statuses."""

    def test_all_statuses_defined(self):
        """Test all statuses are defined."""
        assert TimesheetStatus.NEW in TimesheetStatus.ALL
        assert TimesheetStatus.SUBMITTED in TimesheetStatus.ALL
        assert TimesheetStatus.APPROVED in TimesheetStatus.ALL
        assert TimesheetStatus.NEEDS_APPROVAL in TimesheetStatus.ALL

    def test_status_count(self):
        """Test expected number of statuses."""
        assert len(TimesheetStatus.ALL) == 4


class TestReimbursementType:
    """Tests for reimbursement types."""

    def test_all_reimbursement_types_defined(self):
        """Test all reimbursement types are defined."""
        assert ReimbursementType.CAR in ReimbursementType.ALL
        assert ReimbursementType.FLIGHT in ReimbursementType.ALL
        assert ReimbursementType.FOOD in ReimbursementType.ALL
        assert ReimbursementType.OTHER in ReimbursementType.ALL
