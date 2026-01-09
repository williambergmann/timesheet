#!/bin/bash
set -e

# REQ-029: Run database migrations before starting the application
# This ensures schema is always up-to-date in production

echo "Running database migrations..."
flask db upgrade

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 --worker-class gevent --workers 4 --timeout 120 "app:create_app()"
