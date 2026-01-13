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


# ============================================================================
# Mocked Bot Token Tests
# ============================================================================

class TestGetBotToken:
    """Tests for _get_bot_token function with mocked MSAL."""

    def test_raises_when_not_configured(self, app):
        """Test that _get_bot_token raises when Teams is not configured."""
        from app.utils.teams import _get_bot_token

        app.config["TEAMS_NOTIFICATIONS_ENABLED"] = False

        with app.app_context():
            with pytest.raises(RuntimeError, match="not configured"):
                _get_bot_token()

    @patch("app.utils.teams.is_teams_configured")
    @patch("msal.ConfidentialClientApplication")
    def test_acquires_token_from_msal(self, mock_msal_class, mock_configured, app):
        """Test that _get_bot_token acquires token from MSAL."""
        from app.utils.teams import _get_bot_token, _TOKEN_CACHE

        mock_configured.return_value = True
        
        mock_app = MagicMock()
        mock_app.acquire_token_for_client.return_value = {
            "access_token": "test-bot-token-12345",
            "expires_in": 3600,
        }
        mock_msal_class.return_value = mock_app

        app.config["TEAMS_NOTIFICATIONS_ENABLED"] = True
        app.config["TEAMS_APP_ID"] = "real-app-id"
        app.config["TEAMS_APP_PASSWORD"] = "real-password"
        app.config["TEAMS_TENANT_ID"] = "test-tenant"

        # Clear cache
        _TOKEN_CACHE["access_token"] = ""
        _TOKEN_CACHE["expires_at"] = 0

        with app.app_context():
            token = _get_bot_token()
            assert token == "test-bot-token-12345"
            mock_app.acquire_token_for_client.assert_called_once()

    @patch("app.utils.teams.is_teams_configured")
    @patch("msal.ConfidentialClientApplication")
    def test_uses_cached_token(self, mock_msal_class, mock_configured, app):
        """Test that _get_bot_token uses cached token if not expired."""
        from app.utils.teams import _get_bot_token, _TOKEN_CACHE
        import time

        mock_configured.return_value = True

        # Set a cached token that hasn't expired
        _TOKEN_CACHE["access_token"] = "cached-token"
        _TOKEN_CACHE["expires_at"] = time.time() + 3600

        app.config["TEAMS_NOTIFICATIONS_ENABLED"] = True
        app.config["TEAMS_APP_ID"] = "real-app-id"
        app.config["TEAMS_APP_PASSWORD"] = "real-password"

        with app.app_context():
            token = _get_bot_token()
            assert token == "cached-token"
            # MSAL should not be called since we have a cached token
            mock_msal_class.assert_not_called()

        # Clean up cache for other tests
        _TOKEN_CACHE["access_token"] = ""
        _TOKEN_CACHE["expires_at"] = 0

    @patch("app.utils.teams.is_teams_configured")
    @patch("msal.ConfidentialClientApplication")
    def test_raises_on_token_error(self, mock_msal_class, mock_configured, app):
        """Test that _get_bot_token raises on MSAL error."""
        from app.utils.teams import _get_bot_token, _TOKEN_CACHE

        mock_configured.return_value = True

        mock_app = MagicMock()
        mock_app.acquire_token_for_client.return_value = {
            "error": "invalid_client",
            "error_description": "Invalid client credentials",
        }
        mock_msal_class.return_value = mock_app

        _TOKEN_CACHE["access_token"] = ""
        _TOKEN_CACHE["expires_at"] = 0

        app.config["TEAMS_NOTIFICATIONS_ENABLED"] = True
        app.config["TEAMS_APP_ID"] = "real-app-id"
        app.config["TEAMS_APP_PASSWORD"] = "real-password"

        with app.app_context():
            with pytest.raises(RuntimeError, match="Failed to acquire bot token"):
                _get_bot_token()


# ============================================================================
# Mocked Send Message Tests
# ============================================================================

class TestSendTeamsMessageWithMock:
    """Tests for send_teams_message with mocked HTTP and token."""

    @patch("app.utils.teams._get_bot_token")
    @patch("app.utils.teams.is_teams_configured")
    @patch("requests.post")
    def test_sends_message_successfully(self, mock_post, mock_configured, mock_token, app):
        """Test successful message send to Teams."""
        from app.utils.teams import send_teams_message

        mock_configured.return_value = True
        mock_token.return_value = "test-bot-token"
        mock_post.return_value = MagicMock(status_code=200)

        mock_conversation = MagicMock()
        mock_conversation.service_url = "https://smba.trafficmanager.net/amer/"
        mock_conversation.conversation_id = "conv-123"
        mock_conversation.bot_id = "bot-id-123"
        mock_conversation.bot_name = "Northstar Bot"

        with app.app_context():
            result = send_teams_message(mock_conversation, "Hello Teams!")
            assert result is True
            mock_post.assert_called_once()
            
            # Verify the URL was constructed correctly
            call_args = mock_post.call_args
            url = call_args[0][0]
            assert "v3/conversations/conv-123/activities" in url

    @patch("app.utils.teams._get_bot_token")
    @patch("app.utils.teams.is_teams_configured")
    @patch("requests.post")
    def test_sends_message_with_card(self, mock_post, mock_configured, mock_token, app):
        """Test sending message with adaptive card."""
        from app.utils.teams import send_teams_message

        mock_configured.return_value = True
        mock_token.return_value = "test-bot-token"
        mock_post.return_value = MagicMock(status_code = 201)

        mock_conversation = MagicMock()
        mock_conversation.service_url = "https://smba.trafficmanager.net/amer/"
        mock_conversation.conversation_id = "conv-456"
        mock_conversation.bot_id = "bot-id"
        mock_conversation.bot_name = "Bot"

        card = {"type": "AdaptiveCard", "body": [{"type": "TextBlock", "text": "Hello"}]}

        with app.app_context():
            result = send_teams_message(mock_conversation, "Fallback", card)
            assert result is True

            # Verify card was included in payload
            call_args = mock_post.call_args
            payload = call_args[1]["json"]
            assert "attachments" in payload

    @patch("app.utils.teams._get_bot_token")
    @patch("app.utils.teams.is_teams_configured")
    @patch("requests.post")
    def test_raises_on_http_error(self, mock_post, mock_configured, mock_token, app):
        """Test that HTTP errors raise RuntimeError."""
        from app.utils.teams import send_teams_message

        mock_configured.return_value = True
        mock_token.return_value = "test-bot-token"
        mock_post.return_value = MagicMock(status_code=401, text="Unauthorized")

        mock_conversation = MagicMock()
        mock_conversation.service_url = "https://example.com/"
        mock_conversation.conversation_id = "conv-789"
        mock_conversation.bot_id = "bot-id"
        mock_conversation.bot_name = "Bot"

        with app.app_context():
            with pytest.raises(RuntimeError, match="Teams send failed"):
                send_teams_message(mock_conversation, "Test")


# ============================================================================
# Conversation Lookup Tests
# ============================================================================

class TestGetConversationWithExisting:
    """Tests for get_conversation_for_user with existing conversations."""

    def test_returns_existing_conversation(self, app, sample_user):
        """Test that it returns existing conversation linked to user."""
        from app.utils.teams import get_conversation_for_user
        from app.models import User, TeamsConversation
        from app.extensions import db

        with app.app_context():
            user = User.query.get(sample_user["id"])
            user.teams_opt_in = True
            user.teams_account = "user@company.com"
            
            # Create a conversation for this user
            conversation = TeamsConversation(
                user_id=user.id,
                conversation_id="conv-test-123",
                service_url="https://smba.trafficmanager.net/amer/",
                bot_id="bot-id",
                bot_name="Test Bot",
            )
            db.session.add(conversation)
            db.session.commit()

            result = get_conversation_for_user(user)
            assert result is not None
            assert result.conversation_id == "conv-test-123"

    def test_links_conversation_by_teams_account(self, app, sample_user):
        """Test that it finds and links conversation by teams_account."""
        from app.utils.teams import get_conversation_for_user
        from app.models import User, TeamsConversation
        from app.extensions import db

        with app.app_context():
            user = User.query.get(sample_user["id"])
            user.teams_opt_in = True
            user.teams_account = "newuser@company.com"
            db.session.commit()

            # Create a conversation linked by teams_user_principal (not user_id)
            conversation = TeamsConversation(
                user_id=None,  # Not linked to any user yet
                teams_user_principal="newuser@company.com",
                conversation_id="conv-auto-link",
                service_url="https://smba.trafficmanager.net/amer/",
                bot_id="bot-id",
                bot_name="Test Bot",
            )
            db.session.add(conversation)
            db.session.commit()

            result = get_conversation_for_user(user)
            assert result is not None
            assert result.conversation_id == "conv-auto-link"
            # Should have been linked to the user
            assert result.user_id == user.id


# ============================================================================
# Admin Card Tests
# ============================================================================

class TestBuildAdminSubmissionCard:
    """Tests for build_admin_submission_card function."""

    def test_builds_card_with_timesheet_data(self, app, submitted_timesheet):
        """Test building admin submission card with timesheet data."""
        from app.utils.teams import build_admin_submission_card
        from app.models import Timesheet

        with app.app_context():
            timesheet = Timesheet.query.get(submitted_timesheet["id"])
            
            card = build_admin_submission_card(timesheet, "https://app.example.com")

            assert card["type"] == "AdaptiveCard"
            assert len(card["actions"]) == 3  # Approve, Needs Attention, Open Admin
            
            # Check that it has the input field for reason
            has_input = any(
                item.get("type") == "Input.Text" and item.get("id") == "reason"
                for item in card["body"]
            )
            assert has_input

    def test_card_includes_approve_action(self, app, submitted_timesheet):
        """Test that card includes Approve submit action."""
        from app.utils.teams import build_admin_submission_card
        from app.models import Timesheet

        with app.app_context():
            timesheet = Timesheet.query.get(submitted_timesheet["id"])
            
            card = build_admin_submission_card(timesheet, "https://app.example.com")

            approve_action = next(
                (a for a in card["actions"] if a.get("title") == "Approve"),
                None
            )
            assert approve_action is not None
            assert approve_action["type"] == "Action.Submit"
            assert approve_action["data"]["action"] == "approve_timesheet"


# ============================================================================
# Send Card to Users (Success Path)
# ============================================================================

class TestSendCardToUsersWithMock:
    """Tests for send_card_to_users with successful sends."""

    @patch("app.utils.teams.send_card_to_user")
    def test_counts_successful_sends(self, mock_send, app, sample_user):
        """Test that successful sends are counted."""
        from app.utils.teams import send_card_to_users
        from app.models import User

        mock_send.return_value = True

        with app.app_context():
            user = User.query.get(sample_user["id"])
            user.teams_opt_in = True
            user.teams_account = "user@company.com"

            result = send_card_to_users([user], {"type": "AdaptiveCard"}, "Test")
            assert result == 1
            mock_send.assert_called_once()

    @patch("app.utils.teams.send_card_to_user")
    def test_handles_send_exceptions(self, mock_send, app, sample_user):
        """Test that exceptions during send are caught and logged."""
        from app.utils.teams import send_card_to_users
        from app.models import User

        mock_send.side_effect = Exception("Network error")

        with app.app_context():
            user = User.query.get(sample_user["id"])
            user.teams_opt_in = True
            user.teams_account = "user@company.com"

            # Should not raise, should return 0
            result = send_card_to_users([user], {"type": "AdaptiveCard"}, "Test")
            assert result == 0

    @patch("app.utils.teams.send_card_to_user")
    def test_sends_to_multiple_users(self, mock_send, app, sample_user, sample_admin):
        """Test sending to multiple users."""
        from app.utils.teams import send_card_to_users
        from app.models import User
        from app.extensions import db

        mock_send.return_value = True

        with app.app_context():
            user1 = User.query.get(sample_user["id"])
            user1.teams_opt_in = True
            user1.teams_account = "user1@company.com"

            user2 = User.query.get(sample_admin["id"])
            user2.teams_opt_in = True
            user2.teams_account = "user2@company.com"
            db.session.commit()

            result = send_card_to_users([user1, user2], {"type": "AdaptiveCard"}, "Test")
            assert result == 2
            assert mock_send.call_count == 2
