"""
Route Decorators

Authentication and authorization decorators.
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
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorator to require admin privileges.
    
    Must be used AFTER @login_required. Returns 403 if not admin.
    
    Usage:
        @app.route('/admin-only')
        @login_required
        @admin_required
        def admin_route():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user', {}).get('is_admin'):
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function
