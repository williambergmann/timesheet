"""
Route Decorators

Authentication and authorization decorators for the four-tier role system.

Role Hierarchy:
    TRAINEE - Can only submit Training hours, no approval rights
    STAFF   - Can submit all hour types, no approval rights  
    SUPPORT - Can submit all hour types, can approve trainee timesheets
    ADMIN   - Full access: all hour types, approve all timesheets
"""

from functools import wraps
from flask import session, jsonify


def login_required(f):
    """
    Decorator to require authentication.

    Checks for valid user session. Returns 401 if not authenticated.

    Usage:
        @app.route('/protected')
        @login_required
        def protected_route():
            ...
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """
    Decorator to require admin privileges.

    Must be used AFTER @login_required. Returns 403 if not admin.
    Checks both the new role field and legacy is_admin for compatibility.

    Usage:
        @app.route('/admin-only')
        @login_required
        @admin_required
        def admin_route():
            ...
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get("user", {})
        # Check new role system first, fall back to is_admin for compatibility
        role = user.get("role", "")
        is_admin = user.get("is_admin", False)
        
        if role != "admin" and not is_admin:
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)

    return decorated_function


def role_required(*allowed_roles):
    """
    Decorator to require specific roles.

    Must be used AFTER @login_required. Returns 403 if user's role
    is not in the allowed roles list.

    Args:
        *allowed_roles: Role strings that are allowed (e.g., 'admin', 'support')

    Usage:
        @app.route('/support-or-admin')
        @login_required
        @role_required('support', 'admin')
        def support_route():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = session.get("user", {})
            role = user.get("role", "staff")
            
            if role not in allowed_roles:
                return jsonify({
                    "error": f"Access denied. Required role: {', '.join(allowed_roles)}"
                }), 403
            return f(*args, **kwargs)

        return decorated_function
    return decorator


def can_approve(f):
    """
    Decorator to require approval permissions.

    Must be used AFTER @login_required. Returns 403 if user cannot
    approve timesheets. Admin can approve all; Support can approve trainees.

    Note: This only checks if user has ANY approval permission.
    The actual check for "can approve THIS specific timesheet" must be 
    done in the route handler using user.can_approve(target_user).

    Usage:
        @app.route('/approve/<id>')
        @login_required
        @can_approve
        def approve_timesheet(id):
            ...
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get("user", {})
        role = user.get("role", "staff")
        
        # Admin and Support have approval permissions
        if role not in ("admin", "support"):
            return jsonify({
                "error": "You don't have permission to approve timesheets"
            }), 403
        return f(*args, **kwargs)

    return decorated_function


def get_current_user_role():
    """
    Get current user's role from session.
    
    Returns:
        str: User's role ('trainee', 'staff', 'support', 'admin')
             Returns 'staff' as default if not set.
    """
    return session.get("user", {}).get("role", "staff")
