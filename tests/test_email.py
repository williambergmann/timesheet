"""
Email Utility Tests (REQ-011)

Tests for app/utils/email.py
"""

import pytest
from unittest.mock import patch, MagicMock, ANY
from app.utils.email import (
    send_email,
    send_template_email,
    is_smtp_configured,
    _normalize_recipients,
)


class TestNormalizeRecipients:
    """Tests for _normalize_recipients helper."""

    def test_single_email_string(self, app):
        """Test normalizing a single email string."""
        with app.app_context():
            result = _normalize_recipients("user@example.com")
            assert result == ["user@example.com"]

    def test_email_list(self, app):
        """Test normalizing a list of emails."""
        with app.app_context():
            result = _normalize_recipients(["a@x.com", "b@x.com"])
            assert result == ["a@x.com", "b@x.com"]

    def test_strips_whitespace(self, app):
        """Test whitespace is stripped from emails."""
        with app.app_context():
            result = _normalize_recipients(["  user@test.com  "])
            assert result == ["user@test.com"]

    def test_filters_invalid_emails(self, app):
        """Test invalid emails are filtered out."""
        with app.app_context():
            result = _normalize_recipients(["good@x.com", "no-at-sign", None, ""])
            assert result == ["good@x.com"]

    def test_empty_input(self, app):
        """Test empty input returns empty list."""
        with app.app_context():
            assert _normalize_recipients([]) == []
            assert _normalize_recipients(None) == []
            assert _normalize_recipients("") == []


class TestIsSmtpConfigured:
    """Tests for is_smtp_configured function."""

    def test_returns_false_when_no_host(self, app):
        """Test returns false when SMTP_HOST is missing."""
        with app.app_context():
            app.config["SMTP_HOST"] = ""
            app.config["SMTP_PORT"] = 587
            assert is_smtp_configured() is False

    def test_returns_false_when_no_port(self, app):
        """Test returns false when SMTP_PORT is missing."""
        with app.app_context():
            app.config["SMTP_HOST"] = "smtp.example.com"
            app.config["SMTP_PORT"] = 0
            assert is_smtp_configured() is False

    def test_returns_false_for_placeholder_host(self, app):
        """Test returns false for placeholder SMTP_HOST values."""
        with app.app_context():
            app.config["SMTP_HOST"] = "your-smtp-server"
            app.config["SMTP_PORT"] = 587
            assert is_smtp_configured() is False

    def test_returns_true_when_configured(self, app):
        """Test returns true when SMTP is properly configured."""
        with app.app_context():
            app.config["SMTP_HOST"] = "smtp.sendgrid.net"
            app.config["SMTP_PORT"] = 587
            assert is_smtp_configured() is True


class TestSendEmail:
    """Tests for send_email function."""

    def test_rejects_empty_recipients(self, app):
        """Test rejects empty recipient list."""
        with app.app_context():
            result = send_email([], "Subject", "<p>Content</p>")
            assert result["success"] is False
            assert "recipients" in result["error"].lower()

    def test_rejects_empty_subject(self, app):
        """Test rejects empty subject."""
        with app.app_context():
            result = send_email("user@test.com", "", "<p>Content</p>")
            assert result["success"] is False
            assert "subject" in result["error"].lower()

    def test_rejects_empty_content(self, app):
        """Test rejects empty content."""
        with app.app_context():
            result = send_email("user@test.com", "Subject", "")
            assert result["success"] is False
            assert "content" in result["error"].lower()

    def test_dev_mode_logs_email(self, app):
        """Test dev mode logs email instead of sending."""
        with app.app_context():
            app.config["SMTP_HOST"] = ""  # Ensure not configured
            result = send_email(
                "user@test.com",
                "Test Subject",
                "<p>Test content</p>",
            )
            assert result["success"] is True
            assert result.get("dev_mode") is True

    @patch("app.utils.email.smtplib.SMTP")
    def test_sends_email_when_configured(self, mock_smtp_class, app):
        """Test sends email when SMTP is configured."""
        with app.app_context():
            # Configure SMTP
            app.config["SMTP_HOST"] = "smtp.test.com"
            app.config["SMTP_PORT"] = 587
            app.config["SMTP_USER"] = "user"
            app.config["SMTP_PASSWORD"] = "pass"
            app.config["SMTP_FROM_EMAIL"] = "noreply@test.com"
            app.config["SMTP_USE_TLS"] = True
            app.config["SMTP_USE_SSL"] = False

            # Mock SMTP server
            mock_server = MagicMock()
            mock_smtp_class.return_value = mock_server

            result = send_email(
                "recipient@test.com",
                "Test Subject",
                "<p>Test HTML</p>",
            )

            assert result["success"] is True
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with("user", "pass")
            mock_server.sendmail.assert_called_once()
            mock_server.quit.assert_called_once()

    @patch("app.utils.email.smtplib.SMTP_SSL")
    def test_uses_ssl_when_configured(self, mock_smtp_ssl_class, app):
        """Test uses SSL connection when SMTP_USE_SSL is true."""
        with app.app_context():
            # Configure SMTP with SSL
            app.config["SMTP_HOST"] = "smtp.test.com"
            app.config["SMTP_PORT"] = 465
            app.config["SMTP_USER"] = ""
            app.config["SMTP_PASSWORD"] = ""
            app.config["SMTP_FROM_EMAIL"] = "noreply@test.com"
            app.config["SMTP_USE_TLS"] = False
            app.config["SMTP_USE_SSL"] = True

            mock_server = MagicMock()
            mock_smtp_ssl_class.return_value = mock_server

            result = send_email(
                "recipient@test.com",
                "Subject",
                "<p>Content</p>",
            )

            assert result["success"] is True
            mock_smtp_ssl_class.assert_called_once_with("smtp.test.com", 465)


class TestSendTemplateEmail:
    """Tests for send_template_email function."""

    def test_renders_template_and_sends(self, app):
        """Test renders template and sends email."""
        with app.app_context():
            app.config["SMTP_HOST"] = ""  # Dev mode

            result = send_template_email(
                "user@test.com",
                "Timesheet Approved",
                "approved",
                year=2026,
                app_url="http://localhost/app",
                week_start="Jan 05, 2026",
                total_hours=40.0,
                approved_by="Admin User",
            )

            assert result["success"] is True
            assert result.get("dev_mode") is True

    def test_handles_missing_template(self, app):
        """Test handles missing template gracefully."""
        with app.app_context():
            result = send_template_email(
                "user@test.com",
                "Subject",
                "nonexistent_template",
                year=2026,
            )

            assert result["success"] is False
            assert "error" in result


class TestEmailTemplates:
    """Tests for email template rendering."""

    def test_approved_template_renders(self, app):
        """Test approved template renders without error."""
        with app.app_context():
            from flask import render_template

            html = render_template(
                "email/approved.html",
                year=2026,
                app_url="http://localhost/app",
                week_start="Jan 05, 2026",
                total_hours=40.0,
                approved_by="Admin",
            )
            assert "approved" in html.lower() or "Approved" in html

    def test_needs_attention_template_renders(self, app):
        """Test needs_attention template renders without error."""
        with app.app_context():
            from flask import render_template

            html = render_template(
                "email/needs_attention.html",
                year=2026,
                app_url="http://localhost/app",
                week_start="Jan 05, 2026",
                reason="Missing attachment",
            )
            assert "attention" in html.lower() or "Missing" in html

    def test_reminder_template_renders(self, app):
        """Test reminder template renders without error."""
        with app.app_context():
            from flask import render_template

            html = render_template(
                "email/reminder.html",
                year=2026,
                app_url="http://localhost/app",
                week_start="Jan 05, 2026",
            )
            assert "reminder" in html.lower() or "Reminder" in html

    def test_unsubmitted_template_renders(self, app):
        """Test unsubmitted template renders without error."""
        with app.app_context():
            from flask import render_template

            html = render_template(
                "email/unsubmitted.html",
                year=2026,
                app_url="http://localhost/app",
                week_start="Jan 05, 2026",
            )
            assert "past due" in html.lower() or "timesheet" in html.lower()

    def test_admin_new_submission_template_renders(self, app):
        """Test admin_new_submission template renders without error."""
        with app.app_context():
            from flask import render_template

            html = render_template(
                "email/admin_new_submission.html",
                year=2026,
                app_url="http://localhost/app",
                user_name="Test User",
                user_email="user@test.com",
                week_start="Jan 05, 2026",
                total_hours=40.0,
                field_hours=32.0,
                has_field_hours=True,
                traveled=True,
                has_attachments=True,
                attachment_count=2,
            )
            assert "Test User" in html or "submitted" in html.lower()
