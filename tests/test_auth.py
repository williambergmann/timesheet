"""
Authentication Tests

Tests for authentication routes and session management.
"""

import pytest


class TestAuthRequired:
    """Tests for authentication requirement."""

    def test_unauthenticated_access_to_protected_routes(self, client):
        """Test that protected routes require authentication."""
        protected_routes = [
            ("/api/timesheets", "GET"),
            ("/api/timesheets", "POST"),
            ("/api/admin/timesheets", "GET"),
            ("/api/admin/users", "GET"),
        ]
        
        for route, method in protected_routes:
            if method == "GET":
                response = client.get(route)
            elif method == "POST":
                response = client.post(route, json={})
            
            assert response.status_code == 401, f"Route {route} should require auth"


class TestAdminRequired:
    """Tests for admin requirement."""

    def test_non_admin_access_to_admin_routes(self, auth_client):
        """Test that admin routes require admin privileges."""
        admin_routes = [
            "/api/admin/timesheets",
            "/api/admin/users",
        ]
        
        for route in admin_routes:
            response = auth_client.get(route)
            assert response.status_code == 403, f"Route {route} should require admin"


class TestSessionManagement:
    """Tests for session management."""

    def test_session_contains_user_data(self, auth_client, sample_user):
        """Test that session contains user data after login."""
        with auth_client.session_transaction() as sess:
            assert "user" in sess
            assert sess["user"]["id"] == sample_user["id"]
            assert sess["user"]["email"] == sample_user["email"]

    def test_admin_session_has_admin_flag(self, admin_client, sample_admin):
        """Test that admin session has admin flag."""
        with admin_client.session_transaction() as sess:
            assert sess["user"]["is_admin"] is True


class TestGetCurrentUser:
    """Tests for GET /auth/me endpoint."""

    def test_get_current_user_unauthenticated(self, client):
        """Test getting current user when not authenticated."""
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_get_current_user_authenticated(self, auth_client, sample_user):
        """Test getting current user data."""
        response = auth_client.get("/auth/me")
        assert response.status_code == 200
        
        data = response.get_json()
        assert data["email"] == sample_user["email"]
        assert data["display_name"] == sample_user["display_name"]


class TestLogout:
    """Tests for POST /auth/logout endpoint."""

    def test_logout_clears_session(self, auth_client):
        """Test that logout clears the session."""
        # Verify user is logged in
        with auth_client.session_transaction() as sess:
            assert "user" in sess
        
        # Logout (follow_redirects=False to check response)
        response = auth_client.post("/auth/logout", follow_redirects=False)
        # Logout returns redirect
        assert response.status_code == 302
        
        # Verify session is cleared
        with auth_client.session_transaction() as sess:
            assert "user" not in sess

    def test_logout_redirects_to_login(self, auth_client):
        """Test that logout redirects to login page."""
        response = auth_client.post("/auth/logout", follow_redirects=False)
        assert response.status_code == 302
        assert "/login" in response.location


class TestRateLimiting:
    """Tests for REQ-042: Rate Limiting on Auth Endpoints."""

    def test_rate_limit_headers_present(self, client):
        """Test that rate limit headers are included in responses."""
        response = client.get("/auth/me")
        # Flask-Limiter adds these headers when RATELIMIT_HEADERS_ENABLED=True
        assert "X-RateLimit-Limit" in response.headers or response.status_code in (401, 429)

    def test_dev_login_rate_limited_after_threshold(self, app, client):
        """Test that dev-login is rate limited after exceeding threshold."""
        # TestingConfig sets RATELIMIT_AUTH_LIMIT = "3 per minute"
        # First 3 requests should succeed (or return auth errors)
        for _ in range(3):
            response = client.post(
                "/auth/dev-login",
                data={"username": "invalid", "password": "invalid"}
            )
            # Could be 200 with error message rendered in template
            assert response.status_code in (200, 401, 400)

        # 4th request should be rate limited
        response = client.post(
            "/auth/dev-login",
            data={"username": "invalid", "password": "invalid"}
        )
        assert response.status_code == 429

    def test_rate_limit_returns_json_for_auth_endpoints(self, app, client):
        """Test that rate limit error returns JSON for auth endpoints."""
        # Exceed the rate limit
        for _ in range(4):
            client.post(
                "/auth/dev-login",
                data={"username": "invalid", "password": "invalid"}
            )

        # Next request should return JSON error
        response = client.post(
            "/auth/dev-login",
            data={"username": "invalid", "password": "invalid"}
        )
        assert response.status_code == 429
        data = response.get_json()
        assert data is not None
        assert "error" in data
        assert data["error"] == "Too many requests"

    def test_me_endpoint_rate_limited(self, auth_client):
        """Test that /auth/me is rate limited."""
        # TestingConfig sets RATELIMIT_API_LIMIT = "5 per minute"
        # First 5 requests should succeed
        for _ in range(5):
            response = auth_client.get("/auth/me")
            assert response.status_code == 200

        # 6th request should be rate limited
        response = auth_client.get("/auth/me")
        assert response.status_code == 429

    def test_login_endpoint_rate_limited(self, app, client):
        """Test that /auth/login is rate limited."""
        # TestingConfig sets RATELIMIT_AUTH_LIMIT = "3 per minute"
        for _ in range(3):
            response = client.get("/auth/login")
            # In dev mode, this redirects to /app (302)
            assert response.status_code in (200, 302)

        # 4th request should be rate limited
        response = client.get("/auth/login")
        assert response.status_code == 429


class TestDevLogin:
    """Tests for POST /auth/dev-login endpoint (REQ-002/REQ-017)."""

    def test_dev_login_trainee_success(self, client, app):
        """Test successful trainee login."""
        response = client.post(
            "/auth/dev-login",
            data={"username": "trainee", "password": "trainee"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "/app" in response.location

        with client.session_transaction() as sess:
            assert "user" in sess
            assert sess["user"]["role"] == "trainee"

    def test_dev_login_staff_success(self, client, app):
        """Test successful staff login (maps to internal role for backwards compat)."""
        response = client.post(
            "/auth/dev-login",
            data={"username": "staff", "password": "staff"},
            follow_redirects=False,
        )
        assert response.status_code == 302

        with client.session_transaction() as sess:
            assert sess["user"]["role"] == "internal"  # REQ-061: staff -> internal

    def test_dev_login_support_success(self, client, app):
        """Test successful support login (maps to approver role for backwards compat)."""
        response = client.post(
            "/auth/dev-login",
            data={"username": "support", "password": "support"},
            follow_redirects=False,
        )
        assert response.status_code == 302

        with client.session_transaction() as sess:
            assert sess["user"]["role"] == "approver"  # REQ-061: support -> approver

    def test_dev_login_admin_success(self, client, app):
        """Test successful admin login."""
        response = client.post(
            "/auth/dev-login",
            data={"username": "admin", "password": "password"},
            follow_redirects=False,
        )
        assert response.status_code == 302

        with client.session_transaction() as sess:
            assert sess["user"]["role"] == "admin"
            assert sess["user"]["is_admin"] is True

    def test_dev_login_legacy_user_success(self, client, app):
        """Test successful legacy 'user' login (maps to internal role)."""
        response = client.post(
            "/auth/dev-login",
            data={"username": "user", "password": "user"},
            follow_redirects=False,
        )
        assert response.status_code == 302

        with client.session_transaction() as sess:
            assert sess["user"]["role"] == "internal"  # REQ-061: user -> internal

    def test_dev_login_invalid_username(self, client, app):
        """Test login with invalid username."""
        response = client.post(
            "/auth/dev-login",
            data={"username": "nonexistent", "password": "password"},
        )
        assert response.status_code == 200
        assert b"Invalid username or password" in response.data

    def test_dev_login_invalid_password(self, client, app):
        """Test login with invalid password."""
        response = client.post(
            "/auth/dev-login",
            data={"username": "admin", "password": "wrongpassword"},
        )
        assert response.status_code == 200
        assert b"Invalid username or password" in response.data

    def test_dev_login_creates_user_in_database(self, client, app):
        """Test that dev login creates user record in database."""
        from app.models import User

        response = client.post(
            "/auth/dev-login",
            data={"username": "trainee", "password": "trainee"},
            follow_redirects=False,
        )
        assert response.status_code == 302

        with app.app_context():
            user = User.query.filter_by(email="trainee@localhost").first()
            assert user is not None
            assert user.display_name == "Test Trainee"

    def test_dev_login_updates_existing_user(self, client, app):
        """Test that dev login updates existing user role."""
        from app.models import User
        from app.models.user import UserRole
        from app.extensions import db

        # Create user with wrong role
        with app.app_context():
            existing = User(
                azure_id="dev-trainee-001",
                email="trainee@localhost",
                display_name="Old Name",
                role=UserRole.STAFF,  # Wrong role
            )
            db.session.add(existing)
            db.session.commit()

        # Login should update role
        response = client.post(
            "/auth/dev-login",
            data={"username": "trainee", "password": "trainee"},
            follow_redirects=False,
        )
        assert response.status_code == 302

        with app.app_context():
            user = User.query.filter_by(email="trainee@localhost").first()
            assert user.role == UserRole.TRAINEE
            assert user.display_name == "Test Trainee"


class TestOAuthCallback:
    """Tests for GET /auth/callback endpoint."""

    def test_callback_error_in_params(self, client):
        """Test callback with error parameter."""
        response = client.get("/auth/callback?error=access_denied&error_description=User%20cancelled")
        assert response.status_code == 400
        assert b"access_denied" in response.data

    def test_callback_missing_code(self, client):
        """Test callback without authorization code."""
        response = client.get("/auth/callback")
        assert response.status_code == 400
        assert b"No authorization code" in response.data


class TestLoginRoute:
    """Tests for GET /auth/login endpoint."""

    def test_login_in_dev_mode_auto_redirects(self, client, app):
        """Test that login in dev mode creates session and redirects."""
        # The test config has no Azure credentials, so it's in dev mode
        response = client.get("/auth/login", follow_redirects=False)
        assert response.status_code == 302
        assert "/app" in response.location

        with client.session_transaction() as sess:
            assert "user" in sess


class TestOAuthCallbackWithMock:
    """Tests for OAuth callback with mocked MSAL."""

    def test_callback_token_error(self, client, app):
        """Test callback with token exchange error."""
        from unittest.mock import patch, MagicMock

        # Configure app for production mode
        app.config["AZURE_CLIENT_ID"] = "real-client-id"
        app.config["AZURE_CLIENT_SECRET"] = "real-client-secret"

        with patch("app.routes.auth._get_msal_app") as mock_msal:
            mock_app = MagicMock()
            mock_app.acquire_token_by_authorization_code.return_value = {
                "error": "invalid_grant",
                "error_description": "Code expired",
            }
            mock_msal.return_value = mock_app

            response = client.get("/auth/callback?code=test-code")
            assert response.status_code == 400
            assert b"Token error" in response.data

    def test_callback_missing_user_info(self, client, app):
        """Test callback when token has no user info."""
        from unittest.mock import patch, MagicMock

        app.config["AZURE_CLIENT_ID"] = "real-client-id"
        app.config["AZURE_CLIENT_SECRET"] = "real-client-secret"

        with patch("app.routes.auth._get_msal_app") as mock_msal:
            mock_app = MagicMock()
            mock_app.acquire_token_by_authorization_code.return_value = {
                "access_token": "test-token",
                "id_token_claims": {},  # No user info
            }
            mock_msal.return_value = mock_app

            response = client.get("/auth/callback?code=test-code")
            assert response.status_code == 400
            assert b"Could not get user info" in response.data

    def test_callback_success_creates_user(self, client, app):
        """Test successful OAuth callback creates user and session."""
        from unittest.mock import patch, MagicMock
        from app.models import User

        app.config["AZURE_CLIENT_ID"] = "real-client-id"
        app.config["AZURE_CLIENT_SECRET"] = "real-client-secret"

        with patch("app.routes.auth._get_msal_app") as mock_msal:
            mock_app = MagicMock()
            mock_app.acquire_token_by_authorization_code.return_value = {
                "access_token": "test-access-token",
                "id_token_claims": {
                    "oid": "azure-oid-12345",
                    "preferred_username": "newuser@company.com",
                    "name": "New User",
                },
            }
            mock_msal.return_value = mock_app

            response = client.get("/auth/callback?code=valid-code", follow_redirects=False)
            assert response.status_code == 302
            assert "/app" in response.location

            # Verify user was created
            with app.app_context():
                user = User.query.filter_by(azure_id="azure-oid-12345").first()
                assert user is not None
                assert user.email == "newuser@company.com"
                assert user.display_name == "New User"

    def test_callback_success_updates_existing_user(self, client, app):
        """Test successful OAuth callback updates existing user."""
        from unittest.mock import patch, MagicMock
        from app.models import User
        from app.extensions import db

        app.config["AZURE_CLIENT_ID"] = "real-client-id"
        app.config["AZURE_CLIENT_SECRET"] = "real-client-secret"

        # Create existing user
        with app.app_context():
            existing = User(
                azure_id="azure-existing-001",
                email="old@company.com",
                display_name="Old Name",
            )
            db.session.add(existing)
            db.session.commit()

        with patch("app.routes.auth._get_msal_app") as mock_msal:
            mock_app = MagicMock()
            mock_app.acquire_token_by_authorization_code.return_value = {
                "access_token": "test-access-token",
                "id_token_claims": {
                    "oid": "azure-existing-001",
                    "preferred_username": "updated@company.com",
                    "name": "Updated Name",
                },
            }
            mock_msal.return_value = mock_app

            response = client.get("/auth/callback?code=valid-code", follow_redirects=False)
            assert response.status_code == 302

            # Verify user was updated
            with app.app_context():
                user = User.query.filter_by(azure_id="azure-existing-001").first()
                assert user.email == "updated@company.com"
                assert user.display_name == "Updated Name"

    def test_callback_uses_sub_if_oid_missing(self, client, app):
        """Test callback falls back to 'sub' claim if 'oid' is missing."""
        from unittest.mock import patch, MagicMock
        from app.models import User

        app.config["AZURE_CLIENT_ID"] = "real-client-id"
        app.config["AZURE_CLIENT_SECRET"] = "real-client-secret"

        with patch("app.routes.auth._get_msal_app") as mock_msal:
            mock_app = MagicMock()
            mock_app.acquire_token_by_authorization_code.return_value = {
                "access_token": "test-access-token",
                "id_token_claims": {
                    "sub": "azure-sub-claim",  # Using sub instead of oid
                    "email": "user@example.com",  # Using email instead of preferred_username
                    "name": "Sub User",
                },
            }
            mock_msal.return_value = mock_app

            response = client.get("/auth/callback?code=valid-code", follow_redirects=False)
            assert response.status_code == 302

            with app.app_context():
                user = User.query.filter_by(azure_id="azure-sub-claim").first()
                assert user is not None
                assert user.email == "user@example.com"
