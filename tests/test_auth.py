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
