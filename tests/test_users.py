"""
User Routes Tests

Tests for user settings and profile preferences (REQ-003).
"""

import pytest
from app.models import User, TeamsConversation
from app.extensions import db


class TestGetUserSettings:
    """Tests for GET /api/users/me/settings endpoint."""

    def test_get_settings_unauthenticated(self, client):
        """Test that unauthenticated users cannot access settings."""
        response = client.get("/api/users/me/settings")
        assert response.status_code == 401

    def test_get_settings_returns_user_preferences(self, auth_client, sample_user, app):
        """Test that authenticated users can get their settings."""
        response = auth_client.get("/api/users/me/settings")
        assert response.status_code == 200

        data = response.get_json()
        assert data["email"] == "user@northstar.com"
        assert data["phone"] == "+15551234567"
        assert data["sms_opt_in"] is True
        assert "email_opt_in" in data
        assert "teams_opt_in" in data
        assert "notification_emails" in data
        assert "notification_phones" in data

    def test_get_settings_includes_teams_account(self, auth_client, sample_user, app):
        """Test that Teams account is included in settings."""
        with app.app_context():
            user = User.query.get(sample_user["id"])
            user.teams_account = "user@company.onmicrosoft.com"
            db.session.commit()

        response = auth_client.get("/api/users/me/settings")
        assert response.status_code == 200

        data = response.get_json()
        assert data["teams_account"] == "user@company.onmicrosoft.com"

    def test_get_settings_user_not_found(self, client, app):
        """Test that 404 is returned when user doesn't exist in database."""
        # Create session with non-existent user ID
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 99999,
                "email": "ghost@example.com",
                "is_admin": False,
            }

        response = client.get("/api/users/me/settings")
        assert response.status_code == 404
        assert "User not found" in response.get_json()["error"]


class TestUpdateUserSettings:
    """Tests for PUT /api/users/me/settings endpoint."""

    def test_update_settings_unauthenticated(self, client):
        """Test that unauthenticated users cannot update settings."""
        response = client.put(
            "/api/users/me/settings",
            json={"sms_opt_in": False},
        )
        assert response.status_code == 401

    def test_update_settings_sms_opt_in(self, auth_client, sample_user, app):
        """Test updating SMS opt-in with valid phone number."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "sms_opt_in": True,
                "notification_phones": ["+15551234567"],
                "email_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 200

        # Verify in database
        with app.app_context():
            user = User.query.get(sample_user["id"])
            assert user.sms_opt_in is True
            assert "+15551234567" in user.get_notification_phones()

    def test_update_settings_email_opt_in(self, auth_client, sample_user, app):
        """Test updating email opt-in with valid email."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "email_opt_in": True,
                "notification_emails": ["user@northstar.com"],
                "sms_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 200

        with app.app_context():
            user = User.query.get(sample_user["id"])
            assert user.email_opt_in is True
            assert "user@northstar.com" in user.get_notification_emails()

    def test_update_settings_requires_email_when_opted_in(self, auth_client):
        """Test that email opt-in requires at least one email address."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "email_opt_in": True,
                "notification_emails": [],
                "sms_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 400
        assert "Email notifications require at least one email address" in response.get_json()["error"]

    def test_update_settings_requires_phone_when_sms_opted_in(self, auth_client):
        """Test that SMS opt-in requires at least one phone number."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "sms_opt_in": True,
                "notification_phones": [],
                "email_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 400
        assert "SMS notifications require at least one phone number" in response.get_json()["error"]

    def test_update_settings_requires_teams_account_when_opted_in(self, auth_client):
        """Test that Teams opt-in requires a connected account."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "teams_opt_in": True,
                "teams_account": "",
                "email_opt_in": False,
                "sms_opt_in": False,
            },
        )
        assert response.status_code == 400
        assert "Teams notifications require a connected account" in response.get_json()["error"]

    def test_update_settings_invalid_email_format(self, auth_client):
        """Test that invalid email format is rejected."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "email_opt_in": True,
                "notification_emails": ["not-an-email"],
                "sms_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 400
        assert "Invalid email" in response.get_json()["error"]

    def test_update_settings_invalid_phone_format(self, auth_client):
        """Test that invalid phone format is rejected."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "sms_opt_in": True,
                "notification_phones": ["123"],  # Too short
                "email_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 400
        assert "Invalid phone number" in response.get_json()["error"]

    def test_update_settings_multiple_emails(self, auth_client, sample_user, app):
        """Test updating with multiple email addresses."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "email_opt_in": True,
                "notification_emails": ["primary@example.com", "backup@example.com"],
                "sms_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 200

        with app.app_context():
            user = User.query.get(sample_user["id"])
            emails = user.get_notification_emails()
            assert len(emails) == 2
            assert "primary@example.com" in emails
            assert "backup@example.com" in emails

    def test_update_settings_multiple_phones(self, auth_client, sample_user, app):
        """Test updating with multiple phone numbers."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "sms_opt_in": True,
                "notification_phones": ["+15551234567", "+15559876543"],
                "email_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 200

        with app.app_context():
            user = User.query.get(sample_user["id"])
            phones = user.get_notification_phones()
            assert len(phones) == 2
            # First phone becomes primary
            assert user.phone == "+15551234567"

    def test_update_settings_normalizes_email_case(self, auth_client, sample_user, app):
        """Test that email addresses are normalized to lowercase."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "email_opt_in": True,
                "notification_emails": ["User@EXAMPLE.COM"],
                "sms_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 200

        with app.app_context():
            user = User.query.get(sample_user["id"])
            emails = user.get_notification_emails()
            assert "user@example.com" in emails
            assert "User@EXAMPLE.COM" not in emails

    def test_update_settings_dedupes_emails(self, auth_client, sample_user, app):
        """Test that duplicate emails are removed."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "email_opt_in": True,
                "notification_emails": ["user@example.com", "user@example.com", "USER@EXAMPLE.COM"],
                "sms_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 200

        with app.app_context():
            user = User.query.get(sample_user["id"])
            emails = user.get_notification_emails()
            assert len(emails) == 1

    def test_update_settings_dedupes_phones(self, auth_client, sample_user, app):
        """Test that duplicate phone numbers are removed."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "sms_opt_in": True,
                "notification_phones": ["+15551234567", "+15551234567"],
                "email_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 200

        with app.app_context():
            user = User.query.get(sample_user["id"])
            phones = user.get_notification_phones()
            assert len(phones) == 1

    def test_update_settings_all_notifications_disabled(self, auth_client, sample_user, app):
        """Test disabling all notification channels."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "email_opt_in": False,
                "sms_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 200

        with app.app_context():
            user = User.query.get(sample_user["id"])
            assert user.email_opt_in is False
            assert user.sms_opt_in is False
            assert user.teams_opt_in is False

    def test_update_settings_teams_account_normalized(self, auth_client, sample_user, app):
        """Test that Teams account is normalized to lowercase."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "teams_opt_in": True,
                "teams_account": "User@Company.OnMicrosoft.COM",
                "email_opt_in": False,
                "sms_opt_in": False,
            },
        )
        assert response.status_code == 200

        with app.app_context():
            user = User.query.get(sample_user["id"])
            assert user.teams_account == "user@company.onmicrosoft.com"

    def test_update_settings_updates_session(self, auth_client, sample_user, app):
        """Test that session is updated after settings change."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "email_opt_in": True,
                "notification_emails": ["new@example.com"],
                "sms_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 200

        # Make another request to verify session was updated
        response = auth_client.get("/api/users/me/settings")
        assert response.status_code == 200

    def test_update_settings_user_not_found(self, client, app):
        """Test that 404 is returned when user doesn't exist in database."""
        with client.session_transaction() as sess:
            sess["user"] = {
                "id": 99999,
                "email": "ghost@example.com",
                "is_admin": False,
            }

        response = client.put(
            "/api/users/me/settings",
            json={"sms_opt_in": False},
        )
        assert response.status_code == 404
        assert "User not found" in response.get_json()["error"]

    def test_update_settings_empty_body(self, auth_client, sample_user, app):
        """Test updating with empty request body uses defaults."""
        response = auth_client.put("/api/users/me/settings", json={})
        # Should fail validation since email_opt_in defaults to True but no emails provided
        assert response.status_code == 400

    def test_update_settings_links_teams_conversation(self, auth_client, sample_user, app):
        """Test that existing Teams conversation is linked to user."""
        # Create a pre-existing Teams conversation
        with app.app_context():
            conversation = TeamsConversation(
                teams_user_principal="user@company.onmicrosoft.com",
                conversation_id="conv-123",
                service_url="https://smba.trafficmanager.net/amer/",
                bot_id="bot-123",  # Required field
                bot_name="Northstar Bot",
                user_id=None,  # Not yet linked
            )
            db.session.add(conversation)
            db.session.commit()
            conv_id = conversation.id

        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "teams_opt_in": True,
                "teams_account": "user@company.onmicrosoft.com",
                "email_opt_in": False,
                "sms_opt_in": False,
            },
        )
        assert response.status_code == 200

        # Verify conversation was linked
        with app.app_context():
            conversation = TeamsConversation.query.get(conv_id)
            assert conversation.user_id == sample_user["id"]


class TestNormalizeEmails:
    """Tests for email normalization helper."""

    def test_strips_whitespace(self, auth_client):
        """Test that whitespace is stripped from emails."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "email_opt_in": True,
                "notification_emails": ["  user@example.com  "],
                "sms_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 200

    def test_rejects_non_list(self, auth_client):
        """Test that non-list notification_emails is rejected."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "email_opt_in": True,
                "notification_emails": "user@example.com",  # Should be a list
                "sms_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 400
        assert "must be a list" in response.get_json()["error"]

    def test_rejects_non_string_emails(self, auth_client):
        """Test that non-string email entries are rejected."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "email_opt_in": True,
                "notification_emails": [123],  # Should be strings
                "sms_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 400
        assert "must be strings" in response.get_json()["error"]

    def test_filters_empty_strings(self, auth_client, sample_user, app):
        """Test that empty strings are filtered out."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "email_opt_in": True,
                "notification_emails": ["user@example.com", "", "  "],
                "sms_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 200

        with app.app_context():
            user = User.query.get(sample_user["id"])
            emails = user.get_notification_emails()
            assert len(emails) == 1


class TestNormalizePhones:
    """Tests for phone normalization helper."""

    def test_rejects_non_list(self, auth_client):
        """Test that non-list notification_phones is rejected."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "sms_opt_in": True,
                "notification_phones": "+15551234567",  # Should be a list
                "email_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 400
        assert "must be a list" in response.get_json()["error"]

    def test_rejects_non_string_phones(self, auth_client):
        """Test that non-string phone entries are rejected."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "sms_opt_in": True,
                "notification_phones": [5551234567],  # Should be strings
                "email_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 400
        assert "must be strings" in response.get_json()["error"]

    def test_accepts_various_phone_formats(self, auth_client, sample_user, app):
        """Test that various US phone formats are accepted."""
        # Test with formatted phone number
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "sms_opt_in": True,
                "notification_phones": ["(555) 123-4567"],
                "email_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 200

    def test_rejects_too_long_phone(self, auth_client):
        """Test that phone numbers with too many digits are rejected."""
        response = auth_client.put(
            "/api/users/me/settings",
            json={
                "sms_opt_in": True,
                "notification_phones": ["+11234567890123456789"],  # Too long
                "email_opt_in": False,
                "teams_opt_in": False,
            },
        )
        assert response.status_code == 400
        assert "Invalid phone number" in response.get_json()["error"]
