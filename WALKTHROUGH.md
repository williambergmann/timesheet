# Northstar Timesheet - Application Walkthrough

## Overview

The Northstar Timesheet application provides a modern, web-based timesheet management system for ~60 employees and trainees.

## Access Points

| URL          | Description                    |
| ------------ | ------------------------------ |
| `/`          | Redirect to dashboard or login |
| `/login`     | Microsoft 365 login page       |
| `/dashboard` | User dashboard (after login)   |
| `/app`       | Main timesheet application     |
| `/admin`     | Admin panel (admin users only) |

---

## User Journey

### 1. Login

Users authenticate via Microsoft 365:

1. Navigate to the application
2. Click "Sign in with Microsoft"
3. Complete Azure AD authentication
4. Redirected to dashboard

**Dev Mode:** When `AZURE_CLIENT_ID` is not configured, a development login page allows quick testing without Azure AD.

### 2. Dashboard

After login, users see:

- Welcome message with their name
- Quick stats (timesheets this week, pending approval)
- Recent activity

### 3. Timesheet Management

#### View Timesheets

- Filter by status (Draft, Submitted, Approved, Needs Upload)
- Click any timesheet card to view/edit

#### Create New Timesheet

1. Click "+ New Timesheet"
2. Select the week (defaults to current week)
3. Enter hours by day and hour type
4. Add travel/expense information if applicable
5. Upload attachments for field hours
6. Save as draft or submit

#### Hour Types

| Type         | Payable | Billable |
| ------------ | ------- | -------- |
| Field Hours  | ✅      | ✅       |
| Internal     | ✅      | ❌       |
| Training     | ❌      | ❌       |
| PTO          | ✅      | ❌       |
| Unpaid Leave | ❌      | ❌       |
| Holiday      | ✅      | ❌       |

### 4. Admin Functions

Administrators can:

- View all submitted timesheets
- Approve timesheets
- Request missing attachments
- Add admin notes
- Export data

---

## UI Design

### Color Scheme

- **Primary:** Forest green (`#006400` → `#004d00`)
- **Background:** Light grays with subtle texture
- **Accents:** Status-specific colors (green=approved, yellow=pending, red=needs attention)

### Modern Effects

- **Glassmorphism** on login card and modals
- **Gradient shadows** with green tints
- **Micro-animations** on buttons, cards, and transitions
- **Google Fonts** (Inter) for clean typography

### Components

- Premium sidebar with gradient and active state indicators
- Card-based layout with hover lift effects
- Responsive form inputs with focus states
- Toast notifications for user feedback

---

## Screenshots

![Dashboard](docs/images/new_dashboard.png)
_Main dashboard with forest green header and timesheet cards_

---

## Files Reference

### Frontend

| File                        | Purpose                                  |
| --------------------------- | ---------------------------------------- |
| `static/css/main.css`       | Global styles, CSS variables, typography |
| `static/css/components.css` | Component-specific styles                |
| `static/js/app.js`          | Main application logic                   |
| `static/js/timesheet.js`    | Timesheet form handling                  |
| `static/js/admin.js`        | Admin panel functionality                |
| `static/js/api.js`          | API client module                        |
| `static/js/sse.js`          | Server-Sent Events for real-time updates |

### Templates

| File                       | Purpose                       |
| -------------------------- | ----------------------------- |
| `templates/base.html`      | Base layout template          |
| `templates/index.html`     | Main app (timesheets + admin) |
| `templates/login.html`     | Login page                    |
| `templates/dashboard.html` | Dashboard page                |

---

## Development Branches

| Branch | Purpose                                           |
| ------ | ------------------------------------------------- |
| `main` | Stable, production-ready                          |
| `UI`   | Hour entry UI refactor (PowerApps-style dropdown) |
| `bot`  | Microsoft Teams chatbot integration               |

See [PROGRESS.md](PROGRESS.md) for current development status.
