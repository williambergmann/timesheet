"""
Flask Extensions

Centralized extension initialization to avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Database
db = SQLAlchemy()

# Database migrations
migrate = Migrate()
