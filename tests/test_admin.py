"""
Admin Route Tests

API tests for admin-only endpoints.
"""

import pytest
from datetime import date, timedelta

from app.extensions import db
from app.models import Timesheet, User, Note
from app.models.timesheet import TimesheetStatus


class TestAdminListTimesheets:
    """Tests for GET /api/admin/timesheets."""

    def test_list_timesheets_unauthenticated(self, client):
        """Test that unauthenticated users cannot access admin endpoints."""
        response = client.get("/api/admin/timesheets")
        assert response.status_code == 401

    def test_list_timesheets_non_admin(self, auth_client):
        """Test that regular users cannot access admin endpoints."""
        response = auth_client.get("/api/admin/timesheets")
        assert response.status_code == 403

    def test_list_timesheets_admin(self, admin_client, submitted_timesheet):
        """Test that admins can list submitted timesheets."""
        response = admin_client.get("/api/admin/timesheets")
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["total"] >= 1
        # Check that user info is included
        for ts in data["timesheets"]:
            assert "user" in ts

    def test_list_timesheets_excludes_drafts(self, admin_client, sample_timesheet, submitted_timesheet):
        """Test that draft timesheets are not visible to admins."""
        response = admin_client.get("/api/admin/timesheets")
        data = response.get_json()
        
        # Should only see submitted, not drafts
        for ts in data["timesheets"]:
            assert ts["status"] != TimesheetStatus.NEW

    def test_list_timesheets_filter_by_status(self, admin_client, submitted_timesheet, approved_timesheet):
        """Test filtering admin timesheet list by status."""
        response = admin_client.get("/api/admin/timesheets?status=APPROVED")
        data = response.get_json()
        
        for ts in data["timesheets"]:
            assert ts["status"] == TimesheetStatus.APPROVED

    def test_list_timesheets_filter_by_user(self, admin_client, submitted_timesheet):
        """Test filtering admin timesheet list by user."""
        user_id = submitted_timesheet["user_id"]
        response = admin_client.get(f"/api/admin/timesheets?user_id={user_id}")
        data = response.get_json()
        
        for ts in data["timesheets"]:
            assert ts["user_id"] == user_id


class TestAdminGetTimesheet:
    """Tests for GET /api/admin/timesheets/<id>."""

    def test_get_timesheet_non_admin(self, auth_client, submitted_timesheet):
        """Test that regular users cannot get admin view of timesheet."""
        response = auth_client.get(f"/api/admin/timesheets/{submitted_timesheet['id']}")
        assert response.status_code == 403

    def test_get_timesheet_admin(self, admin_client, submitted_timesheet):
        """Test admin can get timesheet details."""
        response = admin_client.get(f"/api/admin/timesheets/{submitted_timesheet['id']}")
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["id"] == submitted_timesheet["id"]
        assert "user" in data
        assert "notes" in data

    def test_get_draft_timesheet_admin(self, admin_client, sample_timesheet):
        """Test admin cannot view draft timesheets."""
        response = admin_client.get(f"/api/admin/timesheets/{sample_timesheet['id']}")
        assert response.status_code == 404


class TestAdminApproveTimesheet:
    """Tests for POST /api/admin/timesheets/<id>/approve."""

    def test_approve_timesheet_non_admin(self, auth_client, submitted_timesheet):
        """Test that regular users cannot approve timesheets."""
        response = auth_client.post(f"/api/admin/timesheets/{submitted_timesheet['id']}/approve")
        assert response.status_code == 403

    def test_approve_submitted_timesheet(self, admin_client, submitted_timesheet, app):
        """Test approving a submitted timesheet."""
        response = admin_client.post(f"/api/admin/timesheets/{submitted_timesheet['id']}/approve")
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["status"] == TimesheetStatus.APPROVED
        assert data["approved_at"] is not None

    def test_approve_needs_approval_timesheet(self, admin_client, app, sample_user, sample_week_start):
        """Test approving a NEEDS_APPROVAL timesheet."""
        with app.app_context():
            ts = Timesheet(
                user_id=sample_user["id"],
                week_start=sample_week_start - timedelta(weeks=6),
                status=TimesheetStatus.NEEDS_APPROVAL,
            )
            db.session.add(ts)
            db.session.commit()
            ts_id = ts.id

        response = admin_client.post(f"/api/admin/timesheets/{ts_id}/approve")
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["status"] == TimesheetStatus.APPROVED

    def test_approve_draft_timesheet(self, admin_client, sample_timesheet):
        """Test that draft timesheets cannot be approved."""
        response = admin_client.post(f"/api/admin/timesheets/{sample_timesheet['id']}/approve")
        # Should be 404 (draft not visible) or 400 (invalid state)
        assert response.status_code in [400, 404]

    def test_approve_already_approved_timesheet(self, admin_client, approved_timesheet):
        """Test that already approved timesheets cannot be re-approved."""
        response = admin_client.post(f"/api/admin/timesheets/{approved_timesheet['id']}/approve")
        assert response.status_code == 400


class TestAdminRejectTimesheet:
    """Tests for POST /api/admin/timesheets/<id>/reject."""

    def test_reject_timesheet_non_admin(self, auth_client, submitted_timesheet):
        """Test that regular users cannot reject timesheets."""
        response = auth_client.post(f"/api/admin/timesheets/{submitted_timesheet['id']}/reject")
        assert response.status_code == 403

    def test_reject_submitted_timesheet(self, admin_client, submitted_timesheet):
        """Test rejecting (marking as needs approval) a submitted timesheet."""
        response = admin_client.post(
            f"/api/admin/timesheets/{submitted_timesheet['id']}/reject",
            json={"reason": "Missing sign-off sheet"}
        )
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["status"] == TimesheetStatus.NEEDS_APPROVAL

    def test_reject_creates_note(self, admin_client, submitted_timesheet, app):
        """Test that rejecting with reason creates a note."""
        response = admin_client.post(
            f"/api/admin/timesheets/{submitted_timesheet['id']}/reject",
            json={"reason": "Please attach approval document"}
        )
        assert response.status_code == 200
        
        # Verify note was created
        with app.app_context():
            notes = Note.query.filter_by(timesheet_id=submitted_timesheet["id"]).all()
            assert len(notes) == 1
            assert "Please attach approval document" in notes[0].content

    def test_reject_approved_timesheet(self, admin_client, approved_timesheet):
        """Test that approved timesheets cannot be rejected."""
        response = admin_client.post(f"/api/admin/timesheets/{approved_timesheet['id']}/reject")
        assert response.status_code == 400


class TestAdminUnapproveTimesheet:
    """Tests for POST /api/admin/timesheets/<id>/unapprove."""

    def test_unapprove_timesheet_non_admin(self, auth_client, approved_timesheet):
        """Test that regular users cannot unapprove timesheets."""
        response = auth_client.post(f"/api/admin/timesheets/{approved_timesheet['id']}/unapprove")
        assert response.status_code == 403

    def test_unapprove_approved_timesheet(self, admin_client, approved_timesheet):
        """Test unapproving an approved timesheet."""
        response = admin_client.post(f"/api/admin/timesheets/{approved_timesheet['id']}/unapprove")
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["status"] == TimesheetStatus.SUBMITTED
        assert data["approved_at"] is None

    def test_unapprove_non_approved_timesheet(self, admin_client, submitted_timesheet):
        """Test that non-approved timesheets cannot be unapproved."""
        response = admin_client.post(f"/api/admin/timesheets/{submitted_timesheet['id']}/unapprove")
        assert response.status_code == 400


class TestAdminNotes:
    """Tests for POST /api/admin/timesheets/<id>/notes."""

    def test_add_note_non_admin(self, auth_client, submitted_timesheet):
        """Test that regular users cannot add admin notes."""
        response = auth_client.post(
            f"/api/admin/timesheets/{submitted_timesheet['id']}/notes",
            json={"content": "Test note"}
        )
        assert response.status_code == 403

    def test_add_note_admin(self, admin_client, submitted_timesheet):
        """Test admin can add notes to timesheets."""
        response = admin_client.post(
            f"/api/admin/timesheets/{submitted_timesheet['id']}/notes",
            json={"content": "Reviewed and looks good"}
        )
        assert response.status_code == 201
        
        data = response.get_json()
        assert data["content"] == "Reviewed and looks good"

    def test_add_note_to_draft(self, admin_client, sample_timesheet):
        """Test admin cannot add notes to draft timesheets."""
        response = admin_client.post(
            f"/api/admin/timesheets/{sample_timesheet['id']}/notes",
            json={"content": "Test note"}
        )
        assert response.status_code == 404

    def test_add_empty_note(self, admin_client, submitted_timesheet):
        """Test that empty notes are rejected."""
        response = admin_client.post(
            f"/api/admin/timesheets/{submitted_timesheet['id']}/notes",
            json={"content": ""}
        )
        assert response.status_code == 400


class TestAdminListUsers:
    """Tests for GET /api/admin/users."""

    def test_list_users_non_admin(self, auth_client):
        """Test that regular users cannot list users."""
        response = auth_client.get("/api/admin/users")
        assert response.status_code == 403

    def test_list_users_admin(self, admin_client, sample_user, sample_admin):
        """Test admin can list all users."""
        response = admin_client.get("/api/admin/users")
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data["users"]) >= 2  # At least user and admin
        
        emails = [u["email"] for u in data["users"]]
        assert "user@northstar.com" in emails
        assert "admin@northstar.com" in emails
