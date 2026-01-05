# Implementation Notes (Northstar Timesheet)

## Overview

This repo is a Flask + PostgreSQL timesheet application with a vanilla JS/HTML/CSS frontend. It’s intended to run behind Nginx, with Gunicorn (gevent) serving the Flask app and Redis backing Server-Sent Events (SSE) pub/sub.

Core features implemented:
- User timesheet CRUD (draft -> submit workflow)
- Admin review/approve workflow
- Attachments upload/download for field-hour approvals
- Notes on timesheets
- Real-time updates via SSE (Redis pub/sub)

## Repo Layout

- `app/`: Flask application code
  - `app/__init__.py`: `create_app()` factory, blueprint registration
  - `app/config.py`: env-driven configuration
  - `app/extensions.py`: SQLAlchemy + Migrate instances
  - `app/models/`: SQLAlchemy models
  - `app/routes/`: Flask blueprints (auth, timesheets, admin, events, main)
  - `app/utils/`: auth/admin decorators
- `templates/`: Jinja templates (`base.html`, `index.html`, `login.html`)
- `static/`: frontend assets (JS/CSS/images)
- `docker/`: container definitions (`Dockerfile`, `docker-compose.yml`, `nginx.conf`)
- `uploads/`: attachment storage (mounted volume in Docker)

## Runtime Architecture

In Docker, the request flow is:

1. `nginx` serves as reverse proxy and handles SSE-friendly proxy settings for `/api/events`.
2. `web` runs `gunicorn` with `gevent` workers and serves both API and static/template routes.
3. `db` is PostgreSQL (persistent volume).
4. `redis` supports SSE pub/sub (persistent volume).

Key config files:
- `docker/docker-compose.yml`: service wiring and environment defaults
- `docker/nginx.conf`: reverse proxy + `/api/` rate limiting + `/api/events` SSE settings
- `docker/Dockerfile`: Python 3.11 image, installs `requirements.txt`, runs Gunicorn

## Configuration

Configuration is read from environment variables (also loaded from `.env` via `python-dotenv` in non-container runs).

Important env vars (see `.env.example` and `app/config.py`):
- `SECRET_KEY`
- `DATABASE_URL`
- `REDIS_URL`
- Azure AD (MSAL): `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`, `AZURE_REDIRECT_URI`
- Twilio (optional): `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`
- Uploads: `UPLOAD_FOLDER`, `MAX_CONTENT_LENGTH`

## Backend (Flask)

### App Factory

`app:create_app()` (see `app/__init__.py`) sets:
- Template/static paths to repo root `templates/` and `static/`
- SQLAlchemy + Migrate initialization
- Blueprint registration
- `db.create_all()` on startup (helpful for quick-start; consider relying on migrations for production)

### Blueprints and Routes

- `main` (`app/routes/main.py`)
  - `GET /`: serves the SPA-like `templates/index.html` (requires session)
  - `GET /health`: simple health endpoint

- `auth` (`app/routes/auth.py`)
  - `GET /auth/login`: starts MSAL flow; in “dev mode” creates a local admin session
  - `GET /auth/callback`: OAuth callback, creates/updates `User` records
  - `POST /auth/logout`: clears session
  - `GET /auth/me`: returns session user

- `timesheets` (`app/routes/timesheets.py`) (user-scoped)
  - `GET /api/timesheets`: list current user timesheets
  - `POST /api/timesheets`: create a draft timesheet (optionally auto-populate)
  - `GET/PUT/DELETE /api/timesheets/<id>`: view/update/delete draft
  - `POST /api/timesheets/<id>/entries`: replace all entries for the draft
  - `POST /api/timesheets/<id>/submit`: submit; may become `NEEDS_APPROVAL` if missing required attachment
  - `POST /api/timesheets/<id>/attachments`: upload attachment (draft-only)
  - `DELETE /api/timesheets/<id>/attachments/<attachment_id>`: delete attachment (draft-only)
  - `POST /api/timesheets/<id>/notes`: add a note

- `admin` (`app/routes/admin.py`) (admin-scoped)
  - `GET /api/admin/timesheets`: list all non-draft timesheets
  - `GET /api/admin/timesheets/<id>`: view timesheet details
  - `POST /api/admin/timesheets/<id>/approve`: approve
  - `POST /api/admin/timesheets/<id>/reject`: mark `NEEDS_APPROVAL`
  - `POST /api/admin/timesheets/<id>/unapprove`: revert approved -> submitted
  - `GET /api/admin/timesheets/<id>/attachments/<attachment_id>`: download attachment
  - `POST /api/admin/timesheets/<id>/notes`: add an admin note

- `events` (`app/routes/events.py`)
  - `GET /api/events`: SSE stream, backed by Redis pub/sub

### Data Model

Main models are in `app/models/`:
- `User`: employees synced from Microsoft identity
- `Timesheet`: weekly record (week starts Sunday), status workflow
- `TimesheetEntry`: (date, hour_type, hours)
- `Attachment`: stored filename + original filename + MIME + size
- `Note`: comments attached to a timesheet
- `Notification`: records for (future) Twilio SMS sending

## Frontend

The UI is rendered from `templates/index.html` and then driven by vanilla JS:
- `static/js/api.js`: fetch wrapper + API calls
- `static/js/app.js`: view switching + wiring event handlers + file upload UX
- `static/js/timesheet.js`: timesheet form/grid logic
- `static/js/admin.js`: admin list/detail workflows
- `static/js/sse.js`: subscribes to `/api/events` and refreshes UI on updates

The server injects `window.currentUser` in `templates/index.html` so the frontend can enable admin-only behaviors.

## Local Development

### Docker (recommended)

From repo root:
```bash
cd docker
docker-compose up --build
```

Then browse `http://localhost`.

### Local venv (API-only / custom setup)

Requires local Postgres/Redis and env vars configured:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app:create_app
flask run
```

## Code Quality Checks

This repo includes dev dependencies for Python formatting/linting.

Commands:
```bash
source .venv/bin/activate
black app
flake8 app
python -m compileall app
```

Notes:
- `pytest` is installed but there are currently no tests collected.
- `.flake8` is configured with `max-line-length = 88` to match Black.

