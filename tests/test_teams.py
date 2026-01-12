"""
Teams Notification Utility Tests (REQ-012)

Tests for Teams Bot Framework integration with mocking.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestIsTeamsConfigured:
    """Tests for is_teams_configured function."""

    def test_returns_false_when_disabled(self, app):
        """Test that it returns False when TEAMS_NOTIFICATIONS_ENABLED is False."""
        from app.utils.teams import is_teams_configured

        app.config["TEAMS_NOTIFICATIONS_ENABLED"] = False

        with app.app_context():
            assert is_teams_configured() is False

    def test_returns_false_when_app_id_missing(self, app):
        """Test that it returns False when TEAMS_APP_ID is missing."""
        from app.utils.teams import is_teams_configured

        app.config["TEAMS_NOTIFICATIONS_ENABLED"] = True
        app.config["TEAMS_APP_ID"] = None
        app.config["TEAMS_APP_PASSWORD"] = "real-password"

        with app.app_context():
            assert is_teams_configured() is False

    def test_returns_false_when_password_placeholder(self, app):
        """Test that it returns False when password is a placeholder."""
        from app.utils.teams import is_teams_configured

        app.config["TEAMS_NOTIFICATIONS_ENABLED"] = True
        app.config["TEAMS_APP_ID"] = "real-app-id"
        app.config["TEAMS_APP_PASSWORD"] = "your-teams-app-password"

        with app.app_context():
            assert is_teams_configured() is False

    def test_returns_true_when_configured(self, app):
        """Test that it returns True when fully configured."""
        from app.utils.teams import is_teams_configured

        app.config["TEAMS_NOTIFICATIONS_ENABLED"] = True
        app.config["TEAMS_APP_ID"] = "real-app-id"
        app.config["TEAMS_APP_PASSWORD"] = "real-password"

        with app.app_context():
            assert is_teams_configured() is True


class TestIsPlaceholder:
    """Tests for _is_placeholder helper function."""

    def test_empty_string_is_placeholder(self, app):
        """Test that empty string is a placeholder."""
        from app.utils.teams import _is_placeholder

        assert _is_placeholder("") is True
        assert _is_placeholder(None) is True

    def test_your_prefix_is_placeholder(self, app):
        """Test that 'your-' prefix is detected as placeholder."""
        from app.utils.teams import _is_placeholder

        assert _is_placeholder("your-app-id") is True
        assert _is_placeholder("YOUR-SECRET") is True

    def test_example_is_placeholder(self, app):
        """Test that 'example' is detected as placeholder."""
        from app.utils.teams import _is_placeholder

        assert _is_placeholder("example-app-id") is True
        assert _is_placeholder("EXAMPLE") is True

    def test_real_value_is_not_placeholder(self, app):
        """Test that real values are not placeholders."""
        from app.utils.teams import _is_placeholder

        assert _is_placeholder("abc123-real-id") is False
        assert _is_placeholder("b7d2f3a8-1234-5678-abcd-ef1234567890") is False


class TestBuildMessagePayload:
    """Tests for _build_message_payload function."""

    def test_basic_message(self, app):
        """Test building a basic message payload."""
        from app.utils.teams import _build_message_payload

        with app.app_context():
            payload = _build_message_payload(
                text="Hello, world!",
                card=None,
                bot_id="bot-123",
                bot_name="Test Bot",
            )

            assert payload["type"] == "message"
            assert payload["text"] == "Hello, world!"
            assert payload["from"]["id"] == "bot-123"
            assert payload["from"]["name"] == "Test Bot"
            assert "attachments" not in payload

    def test_message_with_card(self, app):
        """Test building a message with adaptive card."""
        from app.utils.teams import _build_message_payload

        card = {"type": "AdaptiveCard", "body": []}

        with app.app_context():
            payload = _build_message_payload(
                text="Card message",
                card=card,
                bot_id="bot-123",
                bot_name=None,
            )

            assert "attachments" in payload
            assert len(payload["attachments"]) == 1
            assert payload["attachments"][0]["contentType"] == "application/vnd.microsoft.card.adaptive"
            assert payload["attachments"][0]["content"] == card


class TestBuildCards:
    """Tests for card-building functions."""

    def test_build_action_open_url(self, app):
        """Test building an OpenUrl action."""
        from app.utils.teams import build_action_open_url

        with app.app_context():
            action = build_action_open_url("View Details", "https://example.com")

            assert action["type"] == "Action.OpenUrl"
            assert action["title"] == "View Details"
            assert action["url"] == "https://example.com"

    def test_build_action_submit(self, app):
        """Test building a Submit action."""
        from app.utils.teams import build_action_submit

        with app.app_context():
            action = build_action_submit("Approve", {"action": "approve", "id": 123})

            assert action["type"] == "Action.Submit"
            assert action["title"] == "Approve"
            assert action["data"]["action"] == "approve"

    def test_build_basic_card(self, app):
        """Test building a basic adaptive card."""
        from app.utils.teams import build_basic_card

        with app.app_context():
            card = build_basic_card(
                title="Test Card",
                lines=["Line 1", "Line 2"],
                actions=None,
            )

            assert card["type"] == "AdaptiveCard"
            assert card["version"] == "1.4"
            assert len(card["body"]) == 3  # Title + 2 lines
            assert card["body"][0]["text"] == "Test Card"
            assert card["actions"] == []

    def test_build_help_card(self, app):
        """Test building the help card."""
        from app.utils.teams import build_help_card

        with app.app_context():
            card = build_help_card("https://app.example.com")

            assert card["type"] == "AdaptiveCard"
            assert len(card["actions"]) == 3  # Open, Create, Settings

    def test_build_timesheet_card(self, app):
        """Test building a timesheet notification card."""
        from app.utils.teams import build_timesheet_card

        with app.app_context():
            card = build_timesheet_card(
                title="Timesheet Approved",
                week_label="Jan 5, 2026",
                body_lines=["Total: 40 hours"],
                app_url="https://app.example.com",
            )

            assert card["type"] == "AdaptiveCard"
            assert len(card["actions"]) == 1


class TestGetConversationForUser:
    """Tests for get_conversation_for_user function."""

    def test_returns_none_if_user_not_opted_in(self, app, sample_user):
        """Test that it returns None if user hasn't opted in."""
        from app.utils.teams import get_conversation_for_user
        from app.models import User

        with app.app_context():
            user = User.query.get(sample_user["id"])
            user.teams_opt_in = False

            result = get_conversation_for_user(user)
            assert result is None

    def test_returns_none_if_no_teams_account(self, app, sample_user):
        """Test that it returns None if user has no teams_account."""
        from app.utils.teams import get_conversation_for_user
        from app.models import User

        with app.app_context():
            user = User.query.get(sample_user["id"])
            user.teams_opt_in = True
            user.teams_account = None

            result = get_conversation_for_user(user)
            assert result is None

    def test_returns_none_if_no_user(self, app):
        """Test that it returns None if user is None."""
        from app.utils.teams import get_conversation_for_user

        with app.app_context():
            result = get_conversation_for_user(None)
            assert result is None


class TestSendTeamsMessage:
    """Tests for send_teams_message function."""

    def test_skips_when_not_configured(self, app):
        """Test that message is skipped when Teams is not configured."""
        from app.utils.teams import send_teams_message

        app.config["TEAMS_NOTIFICATIONS_ENABLED"] = False

        mock_conversation = MagicMock()
        mock_conversation.service_url = "https://smba.trafficmanager.net/amer/"
        mock_conversation.conversation_id = "conv-123"

        with app.app_context():
            result = send_teams_message(mock_conversation, "Test message")
            assert result is False


class TestSendCardToUser:
    """Tests for send_card_to_user function."""

    def test_skips_when_no_conversation(self, app, sample_user):
        """Test that it skips when user has no conversation."""
        from app.utils.teams import send_card_to_user
        from app.models import User

        with app.app_context():
            user = User.query.get(sample_user["id"])
            user.teams_opt_in = False

            result = send_card_to_user(user, {"type": "AdaptiveCard"}, "Test")
            assert result is False


class TestSendCardToUsers:
    """Tests for send_card_to_users function."""

    def test_skips_users_not_opted_in(self, app, sample_user):
        """Test that it skips users who haven't opted in."""
        from app.utils.teams import send_card_to_users
        from app.models import User

        with app.app_context():
            user = User.query.get(sample_user["id"])
            user.teams_opt_in = False

            result = send_card_to_users([user], {"type": "AdaptiveCard"}, "Test")
            assert result == 0

    def test_skips_users_without_teams_account(self, app, sample_user):
        """Test that it skips users without teams_account."""
        from app.utils.teams import send_card_to_users
        from app.models import User

        with app.app_context():
            user = User.query.get(sample_user["id"])
            user.teams_opt_in = True
            user.teams_account = None

            result = send_card_to_users([user], {"type": "AdaptiveCard"}, "Test")
            assert result == 0
