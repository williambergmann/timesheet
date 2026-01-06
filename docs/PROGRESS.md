# Timesheet App - Development Progress

**Last Updated:** January 6, 2026

## Project Overview

Replace PowerApps timesheet application with Flask + vanilla JS/CSS solution.

## Current Status

✅ **Core application is functional and deployed locally**

The app supports Microsoft 365 authentication, timesheet CRUD operations, admin approval workflow, and the UI is complete with the new "Add Row" pattern for hour entry.

---

## Completed Tasks

- [x] **Phase 1: Project Setup & Foundation**

  - [x] Docker configuration (Dockerfile, docker-compose.yml, nginx.conf)
  - [x] Flask app factory with blueprints
  - [x] Configuration and extensions
  - [x] Database models (User, Timesheet, Entry, Attachment, Note, Notification)
  - [x] Route blueprints (auth, timesheets, admin, events, main)
  - [x] Utility decorators (login_required, admin_required)
  - [x] HTML templates (base, index, login)
  - [x] CSS stylesheets (main.css, components.css)
  - [x] JavaScript files (api.js, timesheet.js, app.js, admin.js, sse.js)

- [x] **Premium UI Design**

  - [x] Forest green color scheme (#006400)
  - [x] Glassmorphism effects
  - [x] Google Fonts (Inter)
  - [x] Micro-animations and hover effects
  - [x] Northstar star logo (SVG)

- [x] **Test Suite Implementation**

  - [x] Pytest configuration and fixtures (conftest.py)
  - [x] Model tests - 21 tests
  - [x] Timesheet API tests - 22 tests
  - [x] Admin API tests - 24 tests
  - [x] Auth tests - 10 tests
  - [x] **Total: 85 tests passing, 74% code coverage**

- [x] **Microsoft 365 Authentication**

  - [x] MSAL integration with Azure AD
  - [x] Login/logout flow
  - [x] Session management
  - [x] Dev mode bypass for local development

- [x] **UI Refactor (Hour Entry)**

  - [x] Replace static multi-row grid with dropdown + add button
  - [x] Dynamic row creation per hour type
  - [x] Edit/Done/Remove row actions (lock/unlock pattern)
  - [x] Consistent button styling
  - [x] Week starts on Sunday (timezone-safe calculation)
  - [x] Field hours attachment warning with confirmation dialog

- [x] **Documentation**
  - [x] AZURE.md - Azure AD configuration guide
  - [x] TWILIO.md - Twilio SMS integration guide
  - [x] IMPLEMENTATION.md - Full implementation plan with phases
  - [x] WALKTHROUGH.md - App walkthrough with screenshots
  - [x] roadmap.md - Future improvements and design decisions
  - [x] BOT.md - Microsoft Teams chatbot planning
  - [x] UI.md - UI refactor documentation
  - [x] DARKMODE.md - Dark mode planning document
  - [x] POWERAPPS.md - Original PowerApps reference (feature parity guide)

---

## In Progress

### Dark Mode (Planning)

Planning a UI overhaul to default to dark mode, following Google/YouTube design guidelines:

- [x] Research Material Design dark theme principles
- [x] Document color palette (DARKMODE.md)
- [x] Define elevation overlay system
- [ ] Implement dark mode CSS variables
- [ ] Update all components
- [ ] Test accessibility (WCAG contrast)

See `DARKMODE.md` for full implementation plan.

### PowerApps Feature Parity

Documented all features from original PowerApps for implementation:

- [x] Analyze PowerApps UI and document all elements
- [x] Create POWERAPPS.md with complete feature reference
- [ ] **P0:** Add red warning "Field engineers must submit at least one image."
- [ ] **P0:** Add User Notes field (255 char max)
- [ ] **P0:** Add Admin Notes field (read-only for users)
- [ ] **P1:** Add Time Code help popup (?)
- [ ] **P1:** Add row totals column
- [ ] **P2:** Add status definitions popup

See `POWERAPPS.md` for complete feature comparison.

### Teams Bot Integration (Planned)

Planning document complete for Microsoft Teams chatbot:

- [ ] Bot messaging endpoint
- [ ] Command handling (submit_hours, create_timesheet, etc.)
- [ ] Proactive notifications (weekly reminders)
- [ ] Adaptive Cards integration

See `BOT.md` for implementation plan.

---

## Remaining Work

### Phase 2: Integration & Refinement

- [ ] Alembic database migrations (currently using db.create_all())
- [ ] Twilio SMS notification implementation
- [ ] Dark mode UI implementation
- [ ] End-to-end workflow testing
- [ ] Production deployment testing

### Phase 3: Production Deployment

- [ ] Configure production Azure AD app
- [ ] Set up Twilio credentials
- [ ] Deploy to production server
- [ ] User acceptance testing

---

## Recent Changes (January 6, 2026)

| Commit    | Description                                                               |
| --------- | ------------------------------------------------------------------------- |
| `2202c99` | Fix: Timezone bug in getWeekStart() - weeks now correctly start on Sunday |
| `ebe89cf` | Style: Normalize hour-type-row button styling                             |

---

## Branches

| Branch | Purpose              | Status        |
| ------ | -------------------- | ------------- |
| `main` | Stable, working code | ✅ Up to date |

---

## Quick Commands

```bash
# Start development server
cd docker && docker compose up -d

# Run tests
pytest tests/ -v

# View logs
docker compose logs -f web

# Hard refresh browser (bypass cache)
Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
```

## Notes

- ~60 users expected
- Week starts on Sunday
- Full week timesheets only
- Two roles: Admin and Regular User
- Dark mode coming soon (see DARKMODE.md)
