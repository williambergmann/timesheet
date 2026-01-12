"""
Timesheet Route Tests

API tests for timesheet CRUD operations.
"""

import pytest
from datetime import date, timedelta
from decimal import Decimal

from app.extensions import db
from app.models import Timesheet, TimesheetEntry
from app.models.timesheet import TimesheetStatus, HourType


class TestTimesheetList:
    """Tests for GET /api/timesheets."""

    def test_list_timesheets_unauthenticated(self, client):
        """Test that unauthenticated users cannot list timesheets."""
        response = client.get("/api/timesheets")
        assert response.status_code == 401

    def test_list_timesheets_empty(self, auth_client):
        """Test listing timesheets when none exist."""
        response = auth_client.get("/api/timesheets")
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["timesheets"] == []
        assert data["total"] == 0

    def test_list_timesheets_with_data(self, auth_client, sample_timesheet):
        """Test listing timesheets with existing data."""
        response = auth_client.get("/api/timesheets")
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["total"] == 1
        assert len(data["timesheets"]) == 1

    def test_list_timesheets_filter_by_status(self, auth_client, sample_timesheet, submitted_timesheet):
        """Test filtering timesheets by status."""
        response = auth_client.get("/api/timesheets?status=SUBMITTED")
        assert response.status_code == 200
        
        data = response.get_json()
        assert all(t["status"] == "SUBMITTED" for t in data["timesheets"])

    def test_list_timesheets_pagination(self, auth_client, app, sample_user):
        """Test timesheet pagination."""
        # Create multiple timesheets
        with app.app_context():
            base_date = date(2025, 1, 5)  # A Sunday
            for i in range(5):
                week_start = base_date - timedelta(weeks=i)
                ts = Timesheet(
                    user_id=sample_user["id"],
                    week_start=week_start,
                )
                db.session.add(ts)
            db.session.commit()

        response = auth_client.get("/api/timesheets?page=1&per_page=2")
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data["timesheets"]) == 2
        assert data["total"] == 5
        assert data["pages"] == 3


class TestTimesheetCreate:
    """Tests for POST /api/timesheets."""

    def test_create_timesheet_unauthenticated(self, client):
        """Test that unauthenticated users cannot create timesheets."""
        response = client.post("/api/timesheets", json={})
        assert response.status_code == 401

    def test_create_timesheet_default_week(self, auth_client):
        """Test creating a timesheet for current week."""
        response = auth_client.post("/api/timesheets", json={})
        assert response.status_code == 201
        
        data = response.get_json()
        assert data["status"] == TimesheetStatus.NEW
        assert "id" in data

    def test_create_timesheet_specific_week(self, auth_client):
        """Test creating a timesheet for a specific week."""
        response = auth_client.post("/api/timesheets", json={
            "week_start": "2025-01-05"  # A Sunday
        })
        assert response.status_code == 201
        
        data = response.get_json()
        assert data["week_start"] == "2025-01-05"

    def test_create_timesheet_auto_populate(self, auth_client):
        """Test creating a timesheet with auto-populated entries."""
        response = auth_client.post("/api/timesheets", json={
            "week_start": "2025-01-05",
            "auto_populate": True
        })
        assert response.status_code == 201
        
        data = response.get_json()
        # Should have 5 entries (Mon-Fri)
        assert len(data["entries"]) == 5
        # Each should be 8 hours Field
        for entry in data["entries"]:
            assert entry["hour_type"] == HourType.FIELD
            assert entry["hours"] == 8.0

    def test_create_duplicate_timesheet(self, auth_client, sample_timesheet):
        """Test creating a duplicate timesheet for same week."""
        response = auth_client.post("/api/timesheets", json={
            "week_start": sample_timesheet["week_start"]
        })
        assert response.status_code == 400
        
        data = response.get_json()
        assert "already exists" in data["error"]


class TestTimesheetGet:
    """Tests for GET /api/timesheets/<id>."""

    def test_get_timesheet_unauthenticated(self, client, sample_timesheet):
        """Test that unauthenticated users cannot get timesheets."""
        response = client.get(f"/api/timesheets/{sample_timesheet['id']}")
        assert response.status_code == 401

    def test_get_timesheet(self, auth_client, sample_timesheet):
        """Test getting a specific timesheet."""
        response = auth_client.get(f"/api/timesheets/{sample_timesheet['id']}")
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["id"] == sample_timesheet["id"]

    def test_get_timesheet_not_found(self, auth_client):
        """Test getting a non-existent timesheet."""
        response = auth_client.get("/api/timesheets/fake-uuid-123")
        assert response.status_code == 404

    def test_get_other_users_timesheet(self, auth_client, app, sample_admin, sample_week_start):
        """Test that users cannot access other users' timesheets."""
        # Create a timesheet for the admin user
        with app.app_context():
            other_ts = Timesheet(
                user_id=sample_admin["id"],
                week_start=sample_week_start - timedelta(weeks=5),
            )
            db.session.add(other_ts)
            db.session.commit()
            other_id = other_ts.id

        response = auth_client.get(f"/api/timesheets/{other_id}")
        assert response.status_code == 404


class TestTimesheetUpdate:
    """Tests for PUT /api/timesheets/<id>."""

    def test_update_timesheet(self, auth_client, sample_timesheet):
        """Test updating a draft timesheet."""
        response = auth_client.put(
            f"/api/timesheets/{sample_timesheet['id']}",
            json={
                "traveled": True,
                "has_expenses": True,
                "reimbursement_needed": True,
                "reimbursement_type": "Car",
                "reimbursement_amount": 150.50,
            }
        )
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["traveled"] is True
        assert data["has_expenses"] is True
        assert data["reimbursement_needed"] is True
        assert data["reimbursement_type"] == "Car"
        assert data["reimbursement_amount"] == 150.50

    def test_update_submitted_timesheet(self, auth_client, submitted_timesheet):
        """Test that submitted timesheets cannot be updated."""
        response = auth_client.put(
            f"/api/timesheets/{submitted_timesheet['id']}",
            json={"traveled": True}
        )
        assert response.status_code == 400
        
        data = response.get_json()
        assert "draft" in data["error"].lower()


class TestTimesheetDelete:
    """Tests for DELETE /api/timesheets/<id>."""

    def test_delete_timesheet(self, auth_client, sample_timesheet, app):
        """Test deleting a draft timesheet."""
        response = auth_client.delete(f"/api/timesheets/{sample_timesheet['id']}")
        assert response.status_code == 200
        
        # Verify it's gone
        with app.app_context():
            ts = Timesheet.query.get(sample_timesheet["id"])
            assert ts is None

    def test_delete_submitted_timesheet(self, auth_client, submitted_timesheet):
        """Test that submitted timesheets cannot be deleted."""
        response = auth_client.delete(f"/api/timesheets/{submitted_timesheet['id']}")
        assert response.status_code == 400


class TestTimesheetSubmit:
    """Tests for POST /api/timesheets/<id>/submit."""

    def test_submit_timesheet(self, auth_client, sample_timesheet):
        """Test submitting a draft timesheet."""
        response = auth_client.post(f"/api/timesheets/{sample_timesheet['id']}/submit")
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["status"] == TimesheetStatus.SUBMITTED
        assert data["submitted_at"] is not None

    def test_submit_timesheet_needs_attachment(self, auth_client, sample_timesheet_with_entries):
        """Test submitting timesheet with field hours but no attachment."""
        response = auth_client.post(f"/api/timesheets/{sample_timesheet_with_entries['id']}/submit")
        assert response.status_code == 200
        
        data = response.get_json()
        # Should be NEEDS_APPROVAL since field hours require attachment
        assert data["status"] == TimesheetStatus.NEEDS_APPROVAL

    def test_submit_already_submitted_timesheet(self, auth_client, submitted_timesheet):
        """Test submitting an already submitted timesheet."""
        response = auth_client.post(f"/api/timesheets/{submitted_timesheet['id']}/submit")
        assert response.status_code == 400


class TestTimesheetEntries:
    """Tests for POST /api/timesheets/<id>/entries."""

    def test_update_entries(self, auth_client, sample_timesheet, sample_week_start):
        """Test adding/updating time entries."""
        entries = [
            {
                "entry_date": (sample_week_start + timedelta(days=1)).isoformat(),
                "hour_type": HourType.FIELD,
                "hours": 8
            },
            {
                "entry_date": (sample_week_start + timedelta(days=2)).isoformat(),
                "hour_type": HourType.INTERNAL,
                "hours": 8
            },
        ]
        
        response = auth_client.post(
            f"/api/timesheets/{sample_timesheet['id']}/entries",
            json={"entries": entries}
        )
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data["entries"]) == 2
        assert data["totals"]["total"] == 16.0

    def test_update_entries_replaces_existing(self, auth_client, sample_timesheet_with_entries, sample_week_start):
        """Test that updating entries replaces existing ones."""
        # Get current count
        response = auth_client.get(f"/api/timesheets/{sample_timesheet_with_entries['id']}")
        original_entries = response.get_json()["entries"]
        assert len(original_entries) == 5  # Mon-Fri
        
        # Replace with just one entry
        entries = [{
            "entry_date": (sample_week_start + timedelta(days=1)).isoformat(),
            "hour_type": HourType.PTO,
            "hours": 4
        }]
        
        response = auth_client.post(
            f"/api/timesheets/{sample_timesheet_with_entries['id']}/entries",
            json={"entries": entries}
        )
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data["entries"]) == 1

    def test_update_entries_zero_hours_ignored(self, auth_client, sample_timesheet, sample_week_start):
        """Test that entries with zero hours are ignored."""
        entries = [
            {
                "entry_date": (sample_week_start + timedelta(days=1)).isoformat(),
                "hour_type": HourType.FIELD,
                "hours": 8
            },
            {
                "entry_date": (sample_week_start + timedelta(days=2)).isoformat(),
                "hour_type": HourType.FIELD,
                "hours": 0  # Should be ignored
            },
        ]
        
        response = auth_client.post(
            f"/api/timesheets/{sample_timesheet['id']}/entries",
            json={"entries": entries}
        )
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data["entries"]) == 1  # Only the 8-hour entry


class TestTimesheetNotes:
    """Tests for POST /api/timesheets/<id>/notes."""

    def test_add_note(self, auth_client, sample_timesheet):
        """Test adding a note to a timesheet."""
        response = auth_client.post(
            f"/api/timesheets/{sample_timesheet['id']}/notes",
            json={"content": "This is a test note"}
        )
        assert response.status_code == 201
        
        data = response.get_json()
        assert data["content"] == "This is a test note"

    def test_add_empty_note(self, auth_client, sample_timesheet):
        """Test that empty notes are rejected."""
        response = auth_client.post(
            f"/api/timesheets/{sample_timesheet['id']}/notes",
            json={"content": "  "}
        )
        assert response.status_code == 400


class TestBug006UploadOnNeedsApproval:
    """Tests for BUG-006: Upload on NEEDS_APPROVAL should not lock timesheet."""

    def test_upload_does_not_change_status(self, auth_client, app, needs_approval_timesheet, tmp_path):
        """BUG-006: Uploading to NEEDS_APPROVAL should NOT auto-change to SUBMITTED."""
        import io
        
        # Verify initial status
        response = auth_client.get(f"/api/timesheets/{needs_approval_timesheet['id']}")
        assert response.get_json()["status"] == "NEEDS_APPROVAL"
        
        # Upload a file
        data = {
            "file": (io.BytesIO(b"%PDF-1.4 fake pdf content"), "receipt.pdf")
        }
        response = auth_client.post(
            f"/api/timesheets/{needs_approval_timesheet['id']}/attachments",
            data=data,
            content_type="multipart/form-data"
        )
        assert response.status_code == 201
        
        # Verify status is STILL NEEDS_APPROVAL (not auto-changed to SUBMITTED)
        response = auth_client.get(f"/api/timesheets/{needs_approval_timesheet['id']}")
        data = response.get_json()
        assert data["status"] == "NEEDS_APPROVAL", \
            "BUG-006: Upload should NOT auto-change status from NEEDS_APPROVAL to SUBMITTED"

    def test_can_edit_after_upload(self, auth_client, app, needs_approval_timesheet, tmp_path):
        """BUG-006: User can still edit timesheet after uploading attachment."""
        import io
        
        # Upload a file first
        data = {
            "file": (io.BytesIO(b"%PDF-1.4 fake pdf"), "doc.pdf")
        }
        auth_client.post(
            f"/api/timesheets/{needs_approval_timesheet['id']}/attachments",
            data=data,
            content_type="multipart/form-data"
        )
        
        # Now try to edit the timesheet (this was failing before the fix)
        response = auth_client.put(
            f"/api/timesheets/{needs_approval_timesheet['id']}",
            json={"user_notes": "Updated after upload"}
        )
        assert response.status_code == 200, \
            "BUG-006: Should be able to edit timesheet after upload"
        assert response.get_json()["user_notes"] == "Updated after upload"

    def test_can_resubmit_after_upload(self, auth_client, app, needs_approval_timesheet, tmp_path):
        """BUG-006: User can re-submit timesheet after uploading missing attachment."""
        import io
        
        # Upload a file
        data = {
            "file": (io.BytesIO(b"%PDF-1.4 fake pdf"), "approval.pdf")
        }
        auth_client.post(
            f"/api/timesheets/{needs_approval_timesheet['id']}/attachments",
            data=data,
            content_type="multipart/form-data"
        )
        
        # Re-submit the timesheet
        response = auth_client.post(f"/api/timesheets/{needs_approval_timesheet['id']}/submit")
        assert response.status_code == 200, \
            "BUG-006: Should be able to re-submit after uploading attachment"
        
        # Now it should be SUBMITTED (user explicitly submitted)
        data = response.get_json()
        assert data["status"] == "SUBMITTED"
