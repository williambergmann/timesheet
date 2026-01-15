"""
Authentication Routes

Microsoft 365 / MSAL authentication endpoints.
Rate limited to prevent brute-force attacks (REQ-042).
"""

from flask import Blueprint, redirect, url_for, session, request, current_app
import msal
from ..extensions import limiter

auth_bp = Blueprint("auth", __name__)


def _is_dev_mode():
    """Check if we're in development mode without valid Azure credentials."""
    client_id = current_app.config.get("AZURE_CLIENT_ID")
    client_secret = current_app.config.get("AZURE_CLIENT_SECRET")

    # Check if credentials are placeholder values or missing
    # Note: tenant_id can be 'common' for multi-tenant apps, so we don't check it
    return (
        not client_id
        or not client_secret
        or "your-azure" in str(client_id).lower()
        or "your-azure" in str(client_secret).lower()
    )


def _get_msal_app():
    """Create MSAL ConfidentialClientApplication instance."""
    return msal.ConfidentialClientApplication(
        current_app.config["AZURE_CLIENT_ID"],
        authority=current_app.config["AZURE_AUTHORITY"],
        client_credential=current_app.config["AZURE_CLIENT_SECRET"],
    )


def _get_auth_url(login_hint=None):
    """Build Microsoft 365 authorization URL."""
    msal_app = _get_msal_app()

    return msal_app.get_authorization_request_url(
        scopes=current_app.config["AZURE_SCOPES"],
        redirect_uri=current_app.config["AZURE_REDIRECT_URI"],
        login_hint=login_hint,
    )


@auth_bp.route("/login")
@limiter.limit(lambda: current_app.config.get("RATELIMIT_AUTH_LIMIT", "10 per minute"))
def login():
    """
    Initiate Microsoft 365 login flow.

    In development mode without Azure credentials, creates a test user session.
    If Azure is configured but fails, redirects to generic Microsoft login.
    """
    try:
        # Development mode bypass
        if _is_dev_mode():
            from ..models import User
            from ..extensions import db

            # Create or get a test user (check both azure_id AND email to avoid duplicates)
            test_user = User.query.filter_by(azure_id="dev-user-001").first()
            if not test_user:
                test_user = User.query.filter_by(email="dev@localhost").first()
            if not test_user:
                test_user = User(
                    azure_id="dev-user-001",
                    email="dev@localhost",
                    display_name="Development User",
                    is_admin=True,  # Give dev user admin access
                    notification_emails=["dev@localhost"],
                )
                db.session.add(test_user)
                db.session.commit()

            session["user"] = test_user.to_dict()
            current_app.logger.warning("DEV MODE: Bypassing Azure AD authentication")
            return redirect(url_for("main.app"))  # REQ-016: Auto-redirect to app

        # Production: redirect to Azure AD
        login_hint = request.args.get("login_hint") or None
        auth_url = _get_auth_url(login_hint=login_hint)
        return redirect(auth_url)
    except Exception as e:
        # If Azure configuration fails, redirect to generic Microsoft login
        current_app.logger.error(f"Auth error: {e}")
        # Redirect to generic Microsoft login portal as fallback
        microsoft_login_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
        current_app.logger.warning("Redirecting to generic Microsoft login (Azure not configured)")
        return redirect(microsoft_login_url)


@auth_bp.route("/callback")
@limiter.limit("20 per minute")  # Slightly higher limit for OAuth flow
def callback():
    """
    Handle OAuth callback from Microsoft.

    Exchanges authorization code for access token and creates session.
    """
    from ..models import User
    from ..extensions import db

    # Check for errors
    if "error" in request.args:
        error = request.args.get("error")
        error_desc = request.args.get("error_description", "")
        current_app.logger.error(f"Auth error: {error} - {error_desc}")
        return f"Authentication error: {error}", 400

    # Get authorization code
    code = request.args.get("code")
    if not code:
        return "No authorization code received", 400

    # Exchange code for token
    msal_app = _get_msal_app()
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=current_app.config["AZURE_SCOPES"],
        redirect_uri=current_app.config["AZURE_REDIRECT_URI"],
    )

    if "error" in result:
        current_app.logger.error(f"Token error: {result}")
        return f"Token error: {result.get('error_description', '')}", 400

    # Get user info from ID token claims
    id_token_claims = result.get("id_token_claims", {})
    azure_id = id_token_claims.get("oid") or id_token_claims.get("sub")
    email = id_token_claims.get("preferred_username") or id_token_claims.get("email")
    display_name = id_token_claims.get("name", email)

    if not azure_id or not email:
        return "Could not get user info from token", 400

    # Find or create user in database
    user = User.query.filter_by(azure_id=azure_id).first()

    if not user:
        # Create new user
        user = User(
            azure_id=azure_id,
            email=email,
            display_name=display_name,
            notification_emails=[email],
        )
        db.session.add(user)
        db.session.commit()
        current_app.logger.info(f"Created new user: {email}")
    else:
        # Update user info if changed
        user.email = email
        user.display_name = display_name
        if user.notification_emails is None:
            user.notification_emails = [email]
        db.session.commit()

    # Store user in session
    session["user"] = user.to_dict()
    session["access_token"] = result.get("access_token")

    return redirect(url_for("main.app"))  # REQ-016: Auto-redirect to app


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    End user session.

    Clears session and redirects to login page.
    """
    session.clear()
    return redirect(url_for("main.login_page"))


@auth_bp.route("/dev-login", methods=["POST"])
@limiter.limit(lambda: current_app.config.get("RATELIMIT_AUTH_LIMIT", "10 per minute"))
def dev_login():
    """
    Development login with username/password.
    
    Five-tier test accounts (REQ-061):
    - trainee/trainee: Trainee role (Training hours only)
    - internal/internal: Internal role (Internal, PTO, Holiday, Unpaid)
    - engineer/engineer: Engineer role (Field, PTO, Holiday, Unpaid)
    - approver/approver: Approver role (all hours, approve trainee/engineer)
    - admin/password: Admin role (full access)
    
    Legacy accounts (backwards compatible):
    - staff/staff: Maps to Internal role
    - support/support: Maps to Approver role
    """
    from ..models import User, UserRole
    from ..extensions import db
    from flask import render_template
    
    username = request.form.get("username", "").strip().lower()
    password = request.form.get("password", "")
    
    # Five-tier test account credentials (REQ-061)
    TEST_ACCOUNTS = {
        "trainee": {
            "password": "trainee",
            "role": UserRole.TRAINEE,
            "display_name": "Test Trainee"
        },
        "internal": {
            "password": "internal",
            "role": UserRole.INTERNAL,
            "display_name": "Test Internal"
        },
        "engineer": {
            "password": "engineer",
            "role": UserRole.ENGINEER,
            "display_name": "Test Engineer"
        },
        "approver": {
            "password": "approver",
            "role": UserRole.APPROVER,
            "display_name": "Test Approver"
        },
        "admin": {
            "password": "password",
            "role": UserRole.ADMIN,
            "display_name": "Admin User"
        },
        # Legacy accounts for backwards compatibility
        "staff": {
            "password": "staff",
            "role": UserRole.INTERNAL,  # Maps to new INTERNAL role
            "display_name": "Test Staff"
        },
        "support": {
            "password": "support",
            "role": UserRole.APPROVER,  # Maps to new APPROVER role
            "display_name": "Test Support"
        },
        "user": {
            "password": "user",
            "role": UserRole.INTERNAL,
            "display_name": "Test User"
        },
    }
    
    # Validate credentials
    if username not in TEST_ACCOUNTS:
        return render_template(
            "login.html",
            error="Invalid username or password",
            dev_mode=_is_dev_mode(),
        )
    
    if TEST_ACCOUNTS[username]["password"] != password:
        return render_template(
            "login.html",
            error="Invalid username or password",
            dev_mode=_is_dev_mode(),
        )
    
    account = TEST_ACCOUNTS[username]
    
    # Create or get user in database
    email = f"{username}@localhost"
    user = User.query.filter_by(email=email).first()
    
    if not user:
        user = User(
            azure_id=f"dev-{username}-001",
            email=email,
            display_name=account["display_name"],
            role=account["role"],
            is_admin=(account["role"] == UserRole.ADMIN),  # Legacy field
            notification_emails=[email],
        )
        db.session.add(user)
        db.session.commit()
        current_app.logger.info(f"Created dev user: {email} (role={account['role'].value})")
    else:
        # Update role and display name
        user.role = account["role"]
        user.is_admin = (account["role"] == UserRole.ADMIN)
        user.display_name = account["display_name"]
        if user.notification_emails is None:
            user.notification_emails = [email]
        db.session.commit()
    
    # Store user in session
    session["user"] = user.to_dict()
    current_app.logger.info(
        f"DEV LOGIN: {username} logged in (role={account['role'].value})"
    )
    
    return redirect(url_for("main.app"))  # REQ-016: Auto-redirect to app


@auth_bp.route("/me")
@limiter.limit(lambda: current_app.config.get("RATELIMIT_API_LIMIT", "30 per minute"))
def me():
    """
    Get current user info.

    Returns:
        dict: Current user data or 401 if not authenticated
    """
    if "user" not in session:
        return {"error": "Not authenticated"}, 401

    return session["user"]
