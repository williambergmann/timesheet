"""
Flask Extensions

Centralized extension initialization to avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Database
db = SQLAlchemy()

# Database migrations
migrate = Migrate()

# CSRF protection (REQ-031)
csrf = CSRFProtect()

# Rate limiting (REQ-042)
# Storage backend (Redis) is configured in app factory using app.config["RATELIMIT_STORAGE_URI"]
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],  # Default limits for all routes
)
