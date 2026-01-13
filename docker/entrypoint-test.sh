#!/bin/bash
set -e

echo "Initializing database with db.create_all()..."
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database tables created successfully')
"

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 "app:create_app()"
