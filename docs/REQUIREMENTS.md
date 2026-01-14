# Feature Requirements

> **Purpose:** Track new feature requirements identified from stakeholder decisions.
>
> **Source:** Design decisions captured in [DESIGN.md](DESIGN.md), plus roadmap/security/testing notes in `docs/`
>
> **Last Updated:** January 14, 2026

---

## 📅 Session Log

### January 8, 2026 - Progress Summary

**Completed Today:**

| Requirement       | Description                                                          | Status      |
| ----------------- | -------------------------------------------------------------------- | ----------- |
| REQ-023 / BUG-001 | Read-only submitted timesheets with status-specific UX               | ✅ Complete |
| REQ-029           | Production DB lifecycle (removed db.create_all, use migrations only) | ✅ Complete |
| REQ-031           | CSRF protection for all mutating endpoints (Flask-WTF)               | ✅ Complete |

**Documentation Created:**

- ✅ Created `CHECKIN.md` - Comprehensive project health assessment
- ✅ Documented BUG-003 - Draft timesheets Save/Submit button verification
- ✅ Expanded MCP.md integration in requirements

**New Requirements Added:**

- REQ-042: Rate limiting on auth endpoints
- REQ-043: Health check endpoint
- REQ-044: Frontend modularization (split JS)
- REQ-045: Backup/restore documentation
- REQ-046: E2E tests with Playwright

---

### ✅ January 9, 2026 - Completed

**Recommended Priority Order (ALL COMPLETED):**

1. ✅ **REQ-043: Health Check Endpoint** - Added `/health` endpoint
2. ✅ **BUG-003: Draft Timesheet Buttons** - Fixed, buttons now visible
3. ✅ **REQ-042: Rate Limiting** - Added Flask-Limiter to auth endpoints
4. ✅ **REQ-046: E2E Tests** - Set up Playwright with 29 passing tests

**Additional Work Completed:**

| Requirement | Description                                 | Status      |
| ----------- | ------------------------------------------- | ----------- |
| REQ-003     | User notification preferences UI            | ✅ Complete |
| REQ-006     | Biweekly pay period confirmation            | ✅ Complete |
| REQ-010     | SharePoint sync for attachments             | ✅ Complete |
| REQ-011     | Email notifications (SMTP)                  | ✅ Complete |
| REQ-012     | Teams bot notifications                     | ✅ Complete |
| REQ-019     | Export format options (CSV/Excel/PDF)       | ✅ Complete |
| REQ-021     | Per-option reimbursement attachments        | ✅ Complete |
| REQ-035     | API validation module                       | ✅ Complete |
| REQ-036     | Observability/structured logging            | ✅ Complete |
| REQ-037     | Unit tests (validation, SMS, notifications) | ✅ Complete |
| REQ-038     | UX and accessibility updates                | ✅ Complete |
| REQ-039     | Admin data report view                      | ✅ Complete |
| REQ-044     | Frontend JS modularization                  | ✅ Complete |
| REQ-045     | Backup/restore documentation                | ✅ Complete |

**P0 Items Status:**

- ✅ REQ-030: Auth/session hardening - Complete with nonce verification
- 🔄 REQ-015: Azure AD integration - Needs production validation

---

### 🚀 January 10, 2026 - Start Here

**All P0 Code Complete!** 🎉

REQ-015 (Azure AD) code is fully implemented. Production validation requires real Azure credentials - see checklist in REQ-015 section.

**Completed Today:**

| Requirement | Description                                         | Status      |
| ----------- | --------------------------------------------------- | ----------- |
| REQ-015     | Azure AD Integration (code complete)                | ✅ Complete |
| REQ-033     | Attachment Storage Strategy (already in storage.py) | ✅ Complete |
| REQ-005     | Current Week Filter (already implemented)           | ✅ Complete |
| —           | Fix 26 failing tests                                | ✅ Complete |
| —           | Email service documentation                         | ✅ Complete |

**🐛 Bugs To Fix Today:**

| Bug ID  | Severity | Description                           | Status      |
| ------- | -------- | ------------------------------------- | ----------- |
| BUG-002 | P1       | Reimbursement amounts display "$null" | ✅ Complete |
| BUG-003 | P0       | Dev login causes duplicate key error  | ✅ Verified |

**🔒 Security Tasks Today:**

| Task                                    | Priority | Status      |
| --------------------------------------- | -------- | ----------- |
| Generate strong production `SECRET_KEY` | P0       | ✅ Complete |

---

### ✅ January 11, 2026 - Today's Work

**Completed Today:**

| Task            | Description                                    | Status         |
| --------------- | ---------------------------------------------- | -------------- |
| REQ-047         | User Theme Selection specification             | ✅ Documented  |
| BUG-002         | Reimbursement validation (client-side)         | ✅ Implemented |
| Migration fixes | Fixed 007, 008, 009 revision ID chain          | ✅ Complete    |
| Dark mode       | Force dark mode, preserve light mode CSS       | ✅ Complete    |
| BUGS.md         | Fixed duplicate BUG-003 IDs, added bug index   | ✅ Complete    |
| REQUIREMENTS.md | Added file references to Implementation Status | ✅ Complete    |
| `test_main.py`  | 17 tests for main routes, health, metrics      | ✅ Complete    |
| `.coveragerc`   | Exclude unused modules from coverage           | ✅ Complete    |
| Test coverage   | Improved from 53% to 68% (253 tests)           | 🔄 In Progress |

**Key Files Changed:**

- `static/js/timesheet.js` - Added `validateReimbursementItems()`, `highlightInvalidReimbursementItems()`
- `static/js/app.js` - Added validation call before submit
- `static/css/main.css` - Commented out light mode (forced dark mode)
- `static/css/components.css` - Added `.validation-error`, `.input-error` styles
- `migrations/versions/007_*.py`, `008_*.py`, `009_*.py` - Fixed revision IDs
- `templates/index.html` - Updated CSS/JS version strings
- `docs/BUGS.md` - Renumbered bugs, added index table
- `docs/REQUIREMENTS.md` - Added REQ-047, file references, status updates
- `tests/test_events.py` - Added SSE endpoint tests (11 tests)
- `tests/test_attachments.py` - Added attachment tests (10 tests)
- `tests/test_main.py` - Added main routes tests (17 tests)
- `.coveragerc` - Coverage exclusions for unused modules
- `app/routes/events.py` - Fixed session context bug in SSE generator
- `app/config.py` - Added UPLOAD_FOLDER temp directory for TestingConfig

**Recently Completed:**

| Task                             | Priority | Status  | Reference                                                                                       |
| -------------------------------- | -------- | ------- | ----------------------------------------------------------------------------------------------- |
| Add `test_events.py` (SSE tests) | P2       | ✅ Done | Created `tests/test_events.py`, test `app/routes/events.py` SSE endpoints                       |
| Add `test_attachments.py`        | P1       | ✅ Done | Created `tests/test_attachments.py`, test upload/download/delete via `app/routes/timesheets.py` |
| Add `test_main.py`               | P1       | ✅ Done | Created `tests/test_main.py` with 17 tests for main routes, health, metrics                     |
| Configure coverage exclusions    | P2       | ✅ Done | Created `.coveragerc` to exclude unused modules (bot, jobs, sharepoint, storage, scheduler)     |

**Test Coverage Progress:**

| Metric                 | Before | After | Target  |
| ---------------------- | ------ | ----- | ------- |
| Total Coverage         | 53%    | 68%   | 85%     |
| Tests Passing          | 236    | 253   | —       |
| `app/routes/main.py`   | 24%    | 97%   | ✅ Done |
| `app/routes/events.py` | 0%     | 88%   | ✅ Done |

---

### ✅ January 12, 2026 - Completed

**Test Coverage Push: 68% → 83% (Goal: 85%)**

Major effort to improve test coverage. Created 137 new tests across multiple test files.

**Completed Today — Morning Session (Tests):**

| Task                        | Description                                  | Status      |
| --------------------------- | -------------------------------------------- | ----------- |
| `tests/test_users.py`       | User settings endpoint tests (31 tests)      | ✅ Complete |
| `tests/test_admin_extended` | Extended admin route tests (55 tests)        | ✅ Complete |
| `tests/test_auth.py`        | Auth flow tests with MSAL mocking (30 tests) | ✅ Complete |
| `tests/test_teams.py`       | Teams integration tests (22 tests)           | ✅ Complete |
| `tests/test_notification`   | Notification service edge cases (15 tests)   | ✅ Complete |
| Bug fix                     | Ambiguous join in admin.py data report       | ✅ Complete |
| Documentation               | Testing infrastructure guidelines            | ✅ Complete |

**Completed Today — Afternoon Session (Platform & CI/CD):**

| Task                          | Description                                          | Status      |
| ----------------------------- | ---------------------------------------------------- | ----------- |
| HTTPS/SSL Configuration       | `nginx-ssl.conf`, `docker-compose.prod.yml`          | ✅ Complete |
| Database Password Enforcement | Production compose requires `POSTGRES_PASSWORD`      | ✅ Complete |
| Azure Credential Rotation     | Rotation procedure documented in `AZURE.md`          | ✅ Complete |
| Sentry Error Monitoring       | `sentry-sdk`, Flask integration, `MONITORING.md`     | ✅ Complete |
| GitHub Actions Workflow       | `.github/workflows/test.yml` (pytest, Playwright)    | ✅ Complete |
| Pre-commit Hooks              | `.pre-commit-config.yaml` (Black, flake8, Bandit)    | ✅ Complete |
| Codecov Integration           | Coverage upload in GitHub Actions                    | ✅ Complete |
| Security Scanning             | Bandit + Safety in CI, detect-secrets in pre-commit  | ✅ Complete |
| Documentation Cleanup         | Removed 137 lines of stale duplicate content         | ✅ Complete |
| REQ-051: CONTRIBUTING.md      | Contributor guide: clone, run, test, deploy          | ✅ Complete |
| BUG-006: Investigation        | Root cause identified (auto-status-change on upload) | ✅ Complete |
| BUG-006: Fix                  | Removed auto-status-change, added 3 tests            | ✅ Complete |

**Test Coverage Results:**

| Module                         | Before | After | Target  |
| ------------------------------ | ------ | ----- | ------- |
| **Total Coverage**             | 68%    | 83%   | 85%     |
| **Tests Passing**              | 253    | 390   | 300+ ✅ |
| `app/routes/users.py`          | 16%    | 98%   | ✅ Done |
| `app/routes/auth.py`           | 44%    | 91%   | ✅ Done |
| `app/routes/admin.py`          | 37%    | 74%   | 80%     |
| `app/services/notification.py` | 77%    | 82%   | ✅ Done |
| `app/utils/teams.py`           | 32%    | 57%   | 70%     |

**Key Files Created:**

| File                             | Purpose                                       |
| -------------------------------- | --------------------------------------------- |
| `docker/nginx-ssl.conf`          | Production nginx with TLS, HSTS, CSP headers  |
| `docker/docker-compose.prod.yml` | Production stack with Let's Encrypt           |
| `docs/SSL-SETUP.md`              | SSL setup guide (Let's Encrypt + custom)      |
| `docs/MONITORING.md`             | Sentry setup and troubleshooting              |
| `docs/CI-CD.md`                  | CI/CD pipeline documentation                  |
| `.github/workflows/test.yml`     | GitHub Actions (pytest, Playwright, security) |
| `.pre-commit-config.yaml`        | Local dev hooks (Black, flake8, Bandit)       |
| `CONTRIBUTING.md`                | How to clone, run, test, deploy               |

**Key Commits:**

1. `test: push coverage to 83% with 390 tests`
2. `docs: add testing infrastructure guidelines`
3. `feat: add HTTPS/SSL production configuration`
4. `docs: complete P0 platform improvements documentation`
5. `feat: add Sentry error monitoring integration (P1)`
6. `feat: add CI/CD pipeline with GitHub Actions and pre-commit hooks`
7. `docs: add CONTRIBUTING.md (REQ-051)`
8. `docs: complete BUG-006 investigation`
9. `fix: resolve BUG-006 upload on NEEDS_APPROVAL status`

---

### 📅 January 13, 2026 — Full Day

**Goal: Ship features, push to 85% coverage**

| Task                                 | Time Est. | Priority | Status      | Reference                                                                      |
| ------------------------------------ | --------- | -------- | ----------- | ------------------------------------------------------------------------------ |
| REQ-022: Holiday awareness           | 2-3 hours | P1       | ✅ Complete | Verified: indicator, tooltip, warning dialog work                              |
| REQ-053: Unsaved changes fix         | 30 min    | P1       | ✅ Complete | Warning clears after Save Draft                                                |
| REQ-054: Daily totals row            | 1-2 hours | P1       | ✅ Complete | Total row + grand total working                                                |
| REQ-055: Day hours cap at 24         | 30 min    | P1       | ✅ Complete | Prevents >24h per day, shows warning toast                                     |
| REQ-056: Future week warning         | 30 min    | P1       | ✅ Complete | Warn on Submit if week ends after today                                        |
| Add PDF/Excel export tests           | 1-2 hours | P1       | ✅ Complete | 28 tests added, admin.py 74% → 84%, fixed bug                                  |
| Complete Teams mocking tests         | 1 hour    | P2       | ✅ Complete | 14 tests added, teams.py 57% → 99%                                             |
| Azure Container deployment           | 2 hours   | P1       | ✅ Complete | Deployed to ACI, http://northstar-timesheet-test.eastus.azurecontainer.io:5000 |
| Mobile UI: Hide New Timesheet btn    | 15 min    | P2       | ✅ Complete | Hidden on mobile, accessible in hamburger menu                                 |
| Mobile UI: Remove Settings from menu | 15 min    | P2       | ✅ Complete | Settings only in user dropdown                                                 |
| Single-column layout: Timesheets     | 15 min    | P2       | ✅ Complete | Stacked vertical cards on all screen sizes                                     |
| Single-column layout: Settings       | 15 min    | P2       | ✅ Complete | Notification cards stacked vertically                                          |
| REQ-058: Notification prompt spec    | 30 min    | P1       | ✅ Complete | Mint green banner documented in REQUIREMENTS.md                                |
| BUG-007: Document hamburger resize   | 10 min    | P2       | ✅ Complete | Bug logged in BUGS.md                                                          |

**Coverage Target:**

| Module                | Current | Target | Strategy              |
| --------------------- | ------- | ------ | --------------------- |
| **Total**             | 87%     | 85%    | ✅ Exceeded target!   |
| `app/routes/admin.py` | 84%     | 80%+   | ✅ Complete (was 74%) |
| `app/utils/teams.py`  | 99%     | 70%+   | ✅ Complete (was 57%) |

---

### REQ-054: Daily Totals Row (P1)

**Description:**
Add a summary row at the bottom of the timesheet hours grid showing the total hours for each day (column totals) and the grand total for the week. This row should appear in both the "New Timesheet" editor and the "My Timesheets" view when viewing an existing timesheet.

**Current State (see screenshot):**

- Each hour type row shows its own row total (e.g., "Internal Hours: 40", "Training: 40")
- ❌ No daily totals row showing column sums
- ❌ No grand total for the entire week

**Required:**

| Column    | Content                                    |
| --------- | ------------------------------------------ |
| Hour Type | "**Day Total**" (bold label)               |
| Sun-Sat   | Sum of all hour types for that day         |
| Total     | Grand total hours for the week (all types) |
| Actions   | Empty (no edit/delete for totals row)      |

**Example:**

```
Hour Type       | Sun | Mon | Tue | Wed | Thu | Fri | Sat | Total | Actions
----------------|-----|-----|-----|-----|-----|-----|-----|-------|--------
Internal Hours  |  0  |  8  |  8  |  8  |  8  |  8  |  0  |   40  | ✏️ ×
Training        |  0  |  8  |  8  |  8  |  8  |  8  |  0  |   40  | ✏️ ×
----------------|-----|-----|-----|-----|-----|-----|-----|-------|--------
Day Total       |  0  | 16  | 16  | 16  | 16  | 16  |  0  |   80  |
```

**Implementation Notes:**

1. **Frontend (`static/js/timesheet.js` or `timesheet/entries.js`):**

   - Add `renderDayTotals()` function
   - Calculate column sums from all `hour-input` values
   - Append a styled "totals" row to the entries table
   - Update on any hour input change

2. **Styling (`static/css/components.css`):**

   - Add `.hour-type-row.totals-row` class
   - Bold text, slightly different background (e.g., darker or primary tint)
   - Match the existing row styling

3. **Read-only mode:**
   - Totals row should display in both editable and read-only views

**Acceptance Criteria:**

- [x] Day Total row appears at bottom of hour types grid
- [x] Shows sum of all hour types for each day (Sun-Sat)
- [x] Shows grand total for week in Total column
- [x] Updates dynamically when hours are changed
- [x] Styled distinctly from data rows (bold/different background)
- [x] Works in New Timesheet and existing timesheet views

### 📅 January 14, 2026 — Today's Work

**Completed Today:**

| Task                              | Description                                                     | Status      |
| --------------------------------- | --------------------------------------------------------------- | ----------- |
| BUG-008: Delete draft not working | Fixed SSE application context error causing network congestion  | ✅ Complete |
| SSE endpoint fix                  | Moved `redis_url` lookup outside generator to fix context error | ✅ Complete |
| Sort dropdown wording             | Changed "Sort:" to "Sort by:", "Newest/Oldest" to "Date ↓/↑"    | ✅ Complete |
| UI Polish                         | Unified logo usage (fixed size mismatch in light/dark modes)    | ✅ Complete |
| Infrastructure decision           | Azure hosting cancelled — will self-host on existing servers    | ✅ Decided  |

**Bug Root Cause Analysis:**

The delete button appeared to not work for draft timesheets opened from "My Timesheets". Investigation revealed:

1. **Frontend ID handling was correct** — `populateForm()` properly sets `timesheet-id`, `deleteTimesheet()` correctly reads it
2. **Backend delete API was working** — Direct API calls returned `200 OK`
3. **Root cause: SSE application context error** — The `/api/events` endpoint was crashing with `RuntimeError: Working outside of application context` because `current_app.config` was accessed inside a generator function
4. **Cascade effect:** SSE failures → `500 Internal Server Error` → rapid reconnection attempts → `429 Too Many Requests` → network congestion blocked the DELETE fetch request → `TypeError: Failed to fetch`

**Fix:** Moved `redis_url = current_app.config.get("REDIS_URL", ...)` outside the `generate()` function in `app/routes/events.py`.

**Infrastructure Decision:**

Azure Container Instances deployment tested successfully but will not be used for production. Decision made to self-host on existing company servers, which provides:

- No ongoing cloud costs
- Full control over infrastructure
- Faster deployment cycles
- No dependency on Azure credentials

Azure credentials and ACI resources can be removed/deprovisioned.

**Alternative Hosting Options (for reference):**

_If cloud hosting were needed for development/testing, faster free alternatives exist:_

| Service          | Deploy Speed | Free Tier     | Best For        |
| ---------------- | ------------ | ------------- | --------------- |
| **Railway.app**  | ~30 seconds  | 500 hrs/month | Quick testing   |
| **Fly.io**       | ~30 seconds  | 3 shared CPUs | Edge deployment |
| **Render.com**   | ~1 minute    | 750 hrs/month | Python apps     |
| **Local Docker** | Instant      | Forever       | Development ✅  |

For production self-hosting, requirements are:

- Docker/Docker Compose installed on servers
- Reverse proxy (nginx) for SSL — use `docker/nginx-ssl.conf`
- PostgreSQL and Redis (can run in containers via `docker-compose.prod.yml`)

---

### 📋 Backlog (Future Work)

_Items below are pending implementation. Priority to be determined._

**Features:**

| REQ     | Description             | Priority | Rationale                             |
| ------- | ----------------------- | -------- | ------------------------------------- |
| REQ-024 | Travel mileage tracking | P1       | Larger feature, needs UI design first |
| REQ-025 | Expanded expense types  | P2       | Dependent on REQ-024 architecture     |
| REQ-047 | User theme selection    | P2       | UX polish, not blocking launch        |
| REQ-057 | UI Redesign (Premium)   | P2       | Modern aesthetic, see breakdown below |
| REQ-058 | Notification prompt     | P1       | Encourage users to enable reminders   |

**REQ-057 UI Redesign Breakdown:**

_Reference designs:_

- **Mockup**: `docs/assets/ui_redesign_mockup.png`
- **Prototype HTML**: `file:///Users/lappy/.gemini/antigravity/playground/giant-juno/index.html`

| Component           | Change Description                                                             | Effort |
| ------------------- | ------------------------------------------------------------------------------ | ------ |
| Navigation buttons  | Gradient buttons (green→blue) for New/My Timesheets                            | Small  |
| Icons               | Replace emojis with SVG icons (Feather) — ✅ My Timesheets, New Timesheet done | Medium |
| Color palette       | Dark theme: #111827 background, refined accent colors                          | Small  |
| Sidebar styling     | Pill-shaped active states, hover effects with transparency                     | Medium |
| Card styling        | Subtle borders, rounded corners, consistent shadows                            | Small  |
| Typography          | Switch to Inter/Outfit font, improved hierarchy                                | Small  |
| User profile        | Avatar with initials badge in header                                           | Small  |
| Status tags         | Pill-shaped badges with color coding                                           | Small  |
| Hour type rows      | Cleaner row styling with subtle separators                                     | Medium |
| Input fields        | Dark theme inputs with focus states                                            | Small  |
| Toast notifications | Modern slide-in toasts with icons                                              | Small  |
| Notification bell   | Bell icon with red dot indicator for pending actions                           | Small  |
| Loading states      | Skeleton loaders instead of spinners                                           | Medium |
| Settings page       | Reorganize into Notifications + Appearance sections (rows)                     | Medium |
| Timesheet list      | Single-column layout (full-width cards stacked vertically)                     | Small  |
| Date sort toggle    | Sort by date button with ↓/↑ arrow (newest first default)                      | Small  |

**Acceptance Criteria:**

- [ ] Gradient primary buttons (green→blue) for main navigation
- [ ] SVG icons replace all emoji usage
- [ ] Dark theme color palette applied consistently
- [ ] Sidebar has pill-shaped active/hover states
- [ ] Cards have subtle borders and consistent border-radius
- [ ] Inter or similar modern font applied
- [ ] User initials avatar in header
- [ ] Status badges use pill styling with appropriate colors
- [ ] All forms use dark-themed inputs
- [ ] Notification bell with red dot for pending actions (e.g., needs upload)
- [ ] Settings page has two sections: Notifications (rows) and Appearance
- [ ] Responsive design maintained at all breakpoints
- [ ] Settings page reorganized into Notifications + Appearance sections (rows)
- [ ] My Timesheets uses single-column layout (full-width cards stacked vertically)
- [ ] Date sort toggle: button shows ↓ for newest-first (default), ↑ for oldest-first when clicked

---

**REQ-058: Notification Prompt Popup (P1)**

A mint green notification prompt banner that encourages users to enable notifications. Displays on the My Timesheets view for users who haven't enabled notifications yet.

**UI Design (inline layout matching reference):**

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  🔔  Never miss a timesheet!  Turn on notifications                              ×   │
│                                ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾                                │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

**Visual Specifications:**

| Property      | Value                                                   |
| ------------- | ------------------------------------------------------- |
| Background    | Mint green (`#86efac`) - matches app button color       |
| Border        | 2px solid darker mint (`#6ee79a`) for subtle depth      |
| Border radius | `var(--radius-lg)` (rounded pill-like)                  |
| Text color    | Dark text (`#1a1a1a`) for contrast on light background  |
| Layout        | Single line, centered content, × dismiss on right       |
| Icon          | 🔔 Alarm bell emoji                                     |
| Main text     | "Never miss a timesheet!" (regular weight)              |
| CTA text      | "Turn on notifications" (underlined, clickable link)    |
| Padding       | `var(--spacing-sm)` vertical, `var(--spacing-lg)` horiz |
| Position      | Top of My Timesheets view, above filter bar             |
| Width         | Full-width banner (like reference image)                |

**Behavior:**

1. **Display condition:** Show only if user has no notification channels enabled (no email, SMS, or Teams)
2. **Click action:** Clicking "Turn on notifications" (underlined text) navigates to User Settings → Notifications section (`#settings` view with scroll to notifications)
3. **Dismiss option:** × button on right side; stores `notification_prompt_dismissed` in localStorage (don't show again for 30 days)
4. **Responsive:** Full-width on all screen sizes

**Implementation Notes:**

1. **HTML (`templates/index.html`):**

   - Add a new `#notification-prompt` div above `#timesheets-list`
   - Initially hidden, shown via JavaScript based on conditions

2. **CSS (`static/css/components.css`):**

   ```css
   .notification-prompt {
     background: #86efac;
     border: 2px solid #6ee79a;
     border-radius: var(--radius-lg);
     padding: var(--spacing-sm) var(--spacing-lg);
     margin-bottom: var(--spacing-lg);
     display: flex;
     align-items: center;
     justify-content: center;
     gap: var(--spacing-sm);
     color: #1a1a1a;
     font-size: var(--font-size-sm);
     position: relative;
   }

   .notification-prompt-content {
     display: flex;
     align-items: center;
     gap: var(--spacing-sm);
   }

   .notification-prompt-icon {
     font-size: 1rem;
   }

   .notification-prompt-link {
     color: #1a1a1a;
     text-decoration: underline;
     cursor: pointer;
     margin-left: var(--spacing-xs);
   }

   .notification-prompt-link:hover {
     opacity: 0.8;
   }

   .notification-prompt-dismiss {
     position: absolute;
     right: var(--spacing-md);
     background: none;
     border: none;
     color: #1a1a1a;
     font-size: 1.2rem;
     cursor: pointer;
     opacity: 0.6;
     padding: 0;
     line-height: 1;
   }

   .notification-prompt-dismiss:hover {
     opacity: 1;
   }
   ```

3. **JavaScript (`static/js/app.js` or `settings.js`):**
   - Check user settings on page load
   - If no notification channels enabled and not dismissed, show prompt
   - On link click: navigate to `#settings` and scroll to notification section

**Acceptance Criteria:**

- [ ] Mint green banner (`#86efac`) appears at top of My Timesheets view
- [ ] Contains: 🔔 emoji + "Never miss a timesheet!" + underlined "Turn on notifications"
- [ ] All content on single line, centered
- [ ] × dismiss button on right side
- [ ] Clicking underlined text navigates to Settings → Notifications section
- [ ] Banner only shows if user has no notifications enabled
- [ ] Dismiss button stores preference for 30 days in localStorage
- [ ] Dark text (`#1a1a1a`) on light mint background for readability

**Technical Improvements:**

| REQ     | Description                | Priority | Rationale                              |
| ------- | -------------------------- | -------- | -------------------------------------- |
| REQ-048 | Architecture diagram       | P2       | Documentation quality, not blocking    |
| REQ-049 | API versioning             | P2       | No breaking changes planned short-term |
| REQ-050 | OpenAPI/Swagger spec       | P2       | Nice for external devs, not urgent     |
| REQ-052 | Database-driven hour types | P3       | Config flexibility, not needed for MVP |

**Testing:**

| Task                    | Priority | Rationale                        |
| ----------------------- | -------- | -------------------------------- |
| Push coverage to 90%    | P2       | 87% achieved, 3% remaining       |
| Add observability tests | P3       | Azure Monitor mocking is complex |

---

## 🎯 Priority Legend

- **P0** - Must have for launch
- **P1** - Important, should have
- **P2** - Nice to have
- **P3** - Future consideration

---

## 👥 User Roles & Permissions

### REQ-001: Four-Tier Role System (P0) ✅

Implement a 4-level role hierarchy with different permissions.

**Status: ✅ IMPLEMENTED (January 2026)**

| Role        | Submit Own | Approve Trainee | Approve All | Hour Types Available |
| ----------- | ---------- | --------------- | ----------- | -------------------- |
| **Trainee** | ✅         | ❌              | ❌          | Training only        |
| **Support** | ✅         | ✅              | ❌          | All types            |
| **Staff**   | ✅         | ❌              | ❌          | All types            |
| **Admin**   | ✅         | ✅              | ✅          | All types            |

**Implementation:**

- ✅ Added `role` enum field to User model (`UserRole`: TRAINEE, SUPPORT, STAFF, ADMIN)
- ✅ Role-based permission checks in `app/routes/admin.py`
- ✅ Hour type dropdown filtering based on user role in frontend
- ✅ Backend validation rejects invalid hour types for trainees
- ✅ Legacy `is_admin` field maintained for backward compatibility

---

### REQ-002: Dev Mode Test Accounts (P0) ✅

Create test accounts on the login page for development.

**Status: ✅ IMPLEMENTED (January 2026)**

| Role    | Username | Password |
| ------- | -------- | -------- |
| Trainee | trainee  | trainee  |
| Support | support  | support  |
| Staff   | staff    | staff    |
| Admin   | admin    | password |

**Implementation:**

- ✅ Added `/auth/dev-login` POST endpoint in `app/routes/auth.py`
- ✅ Test accounts created on-demand with proper roles
- ✅ Dev login buttons shown only when Azure credentials not configured
- ✅ Each account demonstrates its role's capabilities

---

## 📱 User Settings

### REQ-003: User Notification Preferences (P1)

Add a User Settings section where users can configure:

**Contact Information:**

- Phone number (for SMS notifications)
- Email address (for email notifications)

**Notification Preferences:**

- [ ] Email notifications (toggle)
- [ ] SMS notifications (toggle)
- [ ] Teams notifications (toggle)

**Implementation Notes:**

- Add settings page accessible from user menu
- Store preferences in User model
- Default all notifications to ON for new users
- SMS opt-out already partially implemented
- Add a username drop-down menu in the header with a **Settings** option
- Settings page includes channel tiles for Email, SMS, and Teams
- Email: allow entering one or more email addresses
- SMS: allow selecting/entering one or more phone numbers
- Teams: allow connecting a Microsoft account for Teams notifications
- **Note:** Teams notifications don't require email entry—user is already authenticated via Microsoft SSO
- Allow multiple emails and phone numbers per user

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Implementation:**

- ✅ User settings view with Email/SMS/Teams tiles and toggles
- ✅ Username dropdown in header with Settings entry
- ✅ User model fields for notification preferences + contact lists
- ✅ Settings API (`GET/PUT /api/users/me/settings`) for saving preferences
- ✅ Multiple email/phone inputs with Teams account storage

---

### REQ-047: User Theme Selection (P2) 📋

Add a comprehensive theme selection system to User Settings with automatic mode and multiple theme options.

**Status:** 📋 Planned

**UI Structure (Settings Page):**

When **Automatic is OFF** (manual mode):

```
┌─────────────────────────────────────────────────┐
│  🎨 DARK MODE                                   │
├─────────────────────────────────────────────────┤
│  ⚙️  Automatic (follow system setting)   [OFF]  │
│  🌙  Dark Mode                             [ON]  │
│  ☀️  Light theme                      Northstar  │
│  🌃  Dark theme                          Night   │
└─────────────────────────────────────────────────┘
```

When **Automatic is ON** (Dark Mode toggle disappears):

```
┌─────────────────────────────────────────────────┐
│  🎨 DARK MODE                                   │
├─────────────────────────────────────────────────┤
│  ⚙️  Automatic (follow system setting)    [ON]  │
│  ☀️  Light theme                      Northstar  │
│  🌃  Dark theme                        Midnight  │
└─────────────────────────────────────────────────┘
```

**Theme Options:**

| Category  | Theme Name   | Description                           | Primary Color            |
| --------- | ------------ | ------------------------------------- | ------------------------ |
| **Light** | Northstar 🌲 | Default light theme (Northstar green) | `#006400` (Forest Green) |
| **Light** | Sky 🌊       | Blue accent theme                     | `#0284c7` (Sky Blue)     |
| **Light** | Sakura 🌸    | Pink accent theme                     | `#db2777` (Pink)         |
| **Dark**  | Night 🌙     | Default dark theme                    | Current dark mode colors |
| **Dark**  | Midnight 🌌  | AMOLED black (true black)             | `#000000` background     |

**Settings Behavior:**

| Setting                   | Default   | Behavior                                                           |
| ------------------------- | --------- | ------------------------------------------------------------------ |
| Automatic (follow system) | OFF       | When ON, **hides** Dark Mode toggle and follows OS preference      |
| Dark Mode                 | ON        | Toggle between dark/light themes (**hidden** when Automatic is ON) |
| Light theme               | Northstar | Selects which light theme variant to use (always visible)          |
| Dark theme                | Night     | Selects which dark theme variant to use (always visible)           |

**Features:**

- Toggle between automatic (system) and manual mode
- Dark Mode on/off toggle **disappears** when Automatic is enabled (not just disabled)
- Light theme selector: Northstar (Green), Sky (Blue), Sakura (Pink)
- Dark theme selector: Night (Default), Midnight (AMOLED Black)
- Save preference per-user in database
- Apply theme immediately without page reload
- Default to Dark Mode with Night theme for all users

**Current State:**

- ✅ Dark mode (Night) is currently forced as the only theme
- ✅ Light mode CSS is preserved in `static/css/light-mode-backup/`
- CSS uses `@media (prefers-color-scheme)` queries ready for re-enabling
- Main CSS: `static/css/main.css` (search for "REQ-047")

**Implementation Notes:**

1. **User Model Changes:**

   - Add `theme_automatic` (Boolean, default: False)
   - Add `theme_dark_mode` (Boolean, default: True)
   - Add `theme_light_variant` (Enum: NORTHSTAR, SKY, PRINCESS, default: NORTHSTAR)
   - Add `theme_dark_variant` (Enum: NIGHT, MIDNIGHT, default: NIGHT)

2. **CSS Organization:**

   - Create theme CSS files: `themes/light-northstar.css`, `themes/light-sky.css`, `themes/light-princess.css`, `themes/dark-night.css`, `themes/dark-midnight.css`
   - Use CSS custom properties (variables) for easy switching
   - Midnight theme should use `--color-bg-page: #000000` for true AMOLED black

3. **Theme Application:**

   - Use CSS classes on `<body>`: `theme-light-northstar`, `theme-light-sky`, `theme-dark-night`, etc.
   - Store preference in localStorage for instant page loads
   - Sync with database via settings API
   - Listen for `prefers-color-scheme` changes when Automatic is enabled

4. **Settings UI:**
   - Display Appearance section in User Settings
   - Automatic toggle disables/grays out Dark Mode toggle when ON
   - Theme selectors show current selection with disclosure arrows
   - Theme names display with emoji icons for visual appeal

---

## 📊 Admin Dashboard

### REQ-004: Pay Period Filter (P1) ✅

Add ability to filter timesheets by current pay period (biweekly).

**Status: ✅ IMPLEMENTED (January 8, 2026)**

**Features:**

- ✅ "Current Pay Period" quick filter button (💵 Pay Period)
- ✅ Pay period date range display (shows "Jan 5 - Jan 18" style badge)
- ✅ Fetches timesheets for both weeks in the pay period
- ✅ Configurable anchor date for pay period calendar

**Implementation Notes:**

- ✅ Uses `PAY_PERIOD_ANCHOR` (Jan 5, 2026) to calculate biweekly periods
- ✅ `getCurrentPayPeriod()` calculates start/end dates for current period
- ✅ Makes 2 API calls (one per week) and combines results
- ✅ Added to admin.js with style in components.css
- ✅ Clears when "Reset" or "This Week" clicked

---

### REQ-005: Current Week Filter (P1) ✅

Add quick filter for current week's timesheets or the current pay period (biweekly).

**Status: ✅ IMPLEMENTED (January 2026)**

**Features:**

- ✅ "This Week" quick filter button on admin dashboard
- ✅ Shows only timesheets with `week_start` = current Sunday
- ✅ Works alongside pay period filter (REQ-004)

**Implementation:**

- ✅ Button in `templates/index.html` (id: `admin-this-week-btn`)
- ✅ Handler in `static/js/admin.js` calculates current week's Sunday
- ✅ Clears pay period filter when activated
- ✅ Shows toast notification with week range

---

### REQ-006: Biweekly Pay Period Confirmation (P2)

Add confirmation step at end of pay period.

**Features:**

- Admin view showing all timesheets in pay period
- "Confirm Pay Period" action to lock/finalize
- Export all confirmed timesheets for payroll

**Implementation Notes:**

- May need new status or flag for "pay period confirmed"
- Prevents further edits after confirmation

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Implementation:**

- ✅ Pay period confirmation endpoint with approval checks
- ✅ Confirmed pay periods stored in `pay_periods` table
- ✅ Timesheets in confirmed periods are locked from edits/approval changes
- ✅ Admin UI includes Confirm Pay Period and payroll export button

---

## ⏱️ Time Entry Grid

### REQ-007: Column Totals (All Grids) (P1) ✅

Show total hours for each day (column) in all Time Entry grids.

**Status: ✅ IMPLEMENTED (January 2026)**

**Applies to:**

- ✅ Employee timesheet form
- ✅ Admin detail view

**Display:**

```
           Sun  Mon  Tue  Wed  Thu  Fri  Sat  | Row Total
Field        -   8    8    8    8    8    -   |    40
Internal     -   -    -    -    -    -    -   |     0
─────────────────────────────────────────────────────────
Day Total    0   8    8    8    8    8    0   |    40
```

**Implementation:**

- ✅ JavaScript calculates column totals dynamically
- ✅ Totals row added to time entry grid footer
- ✅ Updates automatically when hours change

---

### REQ-008: Row Totals (All Grids) (P1) ✅

Show total hours for each hour type (row) in all Time Entry grids.

**Status: ✅ IMPLEMENTED (January 2026)**

**Implementation:**

- ✅ Row totals displayed in rightmost column of grid
- ✅ Each hour type row shows sum of hours across all days
- ✅ Grand total row at bottom sums all hour types
- ✅ Totals update dynamically as user enters hours

---

### REQ-009: Auto-Populate Any Hour Type (P1) ✅

Extend auto-populate feature to work with any hour type selection.

**Status: ✅ IMPLEMENTED (January 8, 2026)**

**Previous:** Auto-populated 8h/day for Field Hours only

**Now:**

- ✅ User selects any hour type from dropdown
- ✅ User checks "Auto-fill 8h Mon-Fri when adding rows" checkbox
- ✅ System fills 8 hours for Mon-Fri for selected type

**Implementation Notes:**

- ✅ Removed `hourType === 'Field'` condition from `addHourTypeRow()`
- ✅ Updated checkbox label to be generic
- ✅ Works for: Field, Internal, Training, PTO, Unpaid, Holiday

---

## 📎 Attachments

### REQ-010: SharePoint Sync (P2)

Sync uploaded attachments to SharePoint for permanent storage.

**Status: ✅ IMPLEMENTED (January 2026)**

**Features:**

- Background job to upload files to SharePoint document library
- Maintain local copy for immediate access
- Track sync status per attachment

**Implementation Notes:**

- Use Microsoft Graph API for SharePoint access
- Define folder structure in SharePoint
- Handle sync failures gracefully
- Roadmap recommends S3/R2 object storage for scale; decide whether SharePoint sync remains primary or becomes secondary (see REQ-033)

**Implementation Detail:**

- Data model additions:
  - `Attachment` fields: `sharepoint_item_id`, `sharepoint_site_id`, `sharepoint_drive_id`, `sharepoint_web_url`, `sharepoint_sync_status` (`PENDING|SYNCED|FAILED`), `sharepoint_synced_at`, `sharepoint_last_attempt_at`, `sharepoint_last_error`, `sharepoint_retry_count`
  - Index `sharepoint_sync_status` for background job scans
- Storage flow:
  - Keep local file in `uploads/` for immediate access
  - After upload, enqueue a sync job with attachment ID and storage path
  - If SharePoint upload succeeds, store item IDs and mark `SYNCED`
  - If upload fails, increment retry count and mark `FAILED` with error
- Background job:
  - Add job in `app/jobs/` (similar to existing job patterns) that polls `PENDING|FAILED` items with exponential backoff
  - Limit concurrency to avoid Graph throttling
  - Log sync metrics and emit structured logs (success/failure) for observability
- Microsoft Graph integration:
  - Use app-only credentials from Azure AD (client credentials flow)
  - Create a SharePoint folder structure by year/week: `Timesheets/{YYYY}/{YYYY-MM-DD}/`
  - Upload to the correct drive (document library) and folder
  - Store `webUrl` for quick access from admin UI
- Admin UI:
  - Add read-only sync status + link in attachment display
  - Show failure reason and retry action for admins
- Security:
  - Store tokens server-side only
  - Restrict to specific site/drive IDs via config
- Config:
  - New env vars: `SP_SITE_ID`, `SP_DRIVE_ID`, `SP_BASE_FOLDER`, plus existing Azure credentials
  - Feature flag: `SHAREPOINT_SYNC_ENABLED` to gate background sync

---

## 🔔 Notifications

> SMS notifications are implemented via Twilio; see [TWILIO.md](TWILIO.md) for configuration, templates, and reminder scheduling.

### REQ-011: Email Notifications (P1)

Send email notifications for timesheet events.

**Status: ✅ IMPLEMENTED (January 2026)**

**Events:**

- Timesheet approved
- Timesheet marked "Needs Approval"
- Weekly reminder to submit (Friday)
- Admin: New timesheet submitted

**Implementation Notes:**

- SMTP-based delivery with config in `.env`/`app.config`
- Respects user notification preferences + email opt-in
- Template-based HTML emails for all events
- Logs in dev mode when SMTP is not configured

**Email Testing with Mailtrap:**

Mailtrap provides a safe email testing environment that catches all outgoing emails without delivering to real users.

_Setup:_

1. Create free account at https://mailtrap.io/register/signup
2. Go to **Email Testing → Inboxes** to get SMTP credentials
3. Add credentials to `.env.local` (gitignored):

```bash
# Mailtrap Sandbox SMTP
SMTP_HOST=sandbox.smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USER=api
SMTP_PASSWORD=your_api_token_here
SMTP_FROM_EMAIL=noreply@northstar-timesheet.com
SMTP_FROM_NAME=Northstar Timesheet
```

_Test Script:_

```bash
# Run email test (requires app context)
cd timesheet
python3 -c "
from app import create_app
from app.utils.email import send_email, is_smtp_configured
app = create_app()
with app.app_context():
    print('SMTP Configured:', is_smtp_configured())
    result = send_email(
        'test@example.com',
        'Test Email from Northstar',
        '<h1>Test</h1><p>This is a test email.</p>'
    )
    print('Result:', result)
"
```

_Dev Mode Behavior:_

When SMTP is **not configured**, emails are logged to console instead of sent:

```
[DEV EMAIL] To=user@example.com Subject=Timesheet Approved
```

This allows local development without Mailtrap setup.

_Free Tier Limits:_

| Plan           | Emails/Month | Use Case                    |
| -------------- | ------------ | --------------------------- |
| Email Sandbox  | 50           | Safe testing (no delivery)  |
| Email API/SMTP | 4,000        | Real delivery (150/day max) |

---

### REQ-012: Teams Bot Notifications (P2)

Extend existing Timesheet Bot to send all notification types.

**Status: ✅ IMPLEMENTED (January 2026)**

**Events:**

- All events from REQ-011
- Interactive cards for approve/reject

**Implementation Notes:**

- See [BOT.md](BOT.md) for Teams bot architecture
- Requires Teams app registration

**Implementation Detail:**

- Bot delivery:
  - Use the existing bot endpoint to send proactive messages for approvals, needs attention, reminders, and new submissions
  - Respect user notification preferences (Teams opt-in + saved Teams account)
- Adaptive Cards:
  - Include timesheet summary, week range, and totals
  - Approve/Reject buttons post back to bot command handlers
  - Provide deep link to `/app#admin` for full review
- Auth & identity:
  - Map incoming Teams user to `User.teams_account`
  - Validate bot framework tokens for incoming actions
- Background reminders:
  - Hook into existing reminder schedule; send Teams notifications alongside SMS/email
  - De-duplicate per user/week to avoid double sends
- Config:
  - `TEAMS_APP_ID`, `TEAMS_APP_PASSWORD`, `TEAMS_TENANT_ID`
  - Feature flag: `TEAMS_NOTIFICATIONS_ENABLED`

---

## 📝 Workflow

### REQ-013: Trainee Hour Type Restriction (P0) ✅

Trainees can only select "Training" from the hour type dropdown.

**Status: ✅ IMPLEMENTED (January 2026)**

**Implementation:**

- ✅ Frontend filters dropdown options based on `user.role`
- ✅ Backend validation rejects non-Training entries from trainees
- ✅ Error message displayed when trainee attempts to submit other hour types
- ✅ Integrated with REQ-001 role system

---

### REQ-014: Submit Without Attachment (Warning) (P1) ✅

Allow users to submit timesheets with Field Hours but no attachment.

**Status: ✅ IMPLEMENTED (January 2026)**

**Behavior:**

- ✅ Show warning: "Field Hours require attachment"
- ✅ User can choose to submit anyway via confirmation dialog
- ✅ Timesheet auto-flags as "Needs Approval"
- ✅ Highlight animation scrolls to attachment section

**Implementation:**

- ✅ `checkFieldHoursAttachment()` validates before submit
- ✅ Confirmation modal with "Submit Anyway" option
- ✅ Toast notification reminds user to add attachment
- ✅ Status set to `NEEDS_APPROVAL` for admin review

---

### REQ-015: Azure AD Integration (P0) ✅

Enable full Azure AD SSO for production authentication.

**Status: ✅ CODE COMPLETE (January 2026) - Pending Production Validation**

**Implementation Summary:**

| Component         | Status      | Location                          |
| ----------------- | ----------- | --------------------------------- |
| MSAL Auth Flow    | ✅ Complete | `app/routes/auth.py`              |
| User Provisioning | ✅ Complete | Get-or-create pattern in callback |
| Dev Mode Fallback | ✅ Complete | Four-tier test accounts           |
| Rate Limiting     | ✅ Complete | REQ-042 integration               |
| Documentation     | ✅ Complete | `docs/AZURE.md`                   |
| Configuration     | ✅ Complete | `.env.example`, `app/config.py`   |

**Current Behavior:**

| Credentials Configured | Microsoft Login | Dev Login Buttons |
| ---------------------- | --------------- | ----------------- |
| ❌ Not configured      | Shows dev mode  | ✅ Shown          |
| ✅ Configured          | ✅ Works        | ❌ Hidden         |

**Production Validation Checklist:**

To validate in staging/production with real Azure credentials:

- [ ] Create Azure App Registration (see [AZURE.md](AZURE.md) Step 1)
- [ ] Generate client secret (Step 3)
- [ ] Add redirect URI for your domain: `https://your-domain.com/auth/callback`
- [ ] Grant admin consent for `User.Read` permission
- [ ] Set environment variables in production:
  - `AZURE_CLIENT_ID`
  - `AZURE_CLIENT_SECRET`
  - `AZURE_TENANT_ID`
  - `AZURE_REDIRECT_URI=https://your-domain.com/auth/callback`
- [ ] Deploy and test:
  - [ ] Click "Sign in with Microsoft" → redirects to Microsoft
  - [ ] Authenticate with MS 365 account → redirects back
  - [ ] First login creates user in database
  - [ ] Subsequent logins retrieve existing user
  - [ ] User shows in admin user list with STAFF role

**Role Assignment (Phased Rollout):**

| Phase   | Role Source                    | Status         |
| ------- | ------------------------------ | -------------- |
| Phase 1 | Default to STAFF               | ✅ Implemented |
| Phase 2 | Northstar internal permissions | 📋 Planned     |
| Phase 3 | Azure AD group sync (optional) | 📋 Future      |

**Implementation Details:**

- ✅ MSAL ConfidentialClientApplication with authorization code flow
- ✅ Optional `login_hint` parameter for streamlined sign-in
- ✅ Access token + ID token claims stored in session
- ✅ User created with `azure_id`, `email`, `display_name`
- ✅ Default role: `STAFF` (admin can upgrade)
- ✅ `notification_emails` initialized with primary email
- ✅ Rate limiting: 10/minute on login, 20/minute on callback

---

### REQ-016: Auto-Redirect After Login (P0) ✅

After successful login, redirect users directly to their appropriate view.

**Status: ✅ IMPLEMENTED (January 2026)**

**Behavior:**

- ✅ All roles redirect to `/app` after login
- ✅ No intermediate landing page
- ✅ Dashboard loads immediately after authentication

**Implementation:**

- ✅ All login routes (`/auth/login`, `/auth/dev-login`, `/auth/callback`) redirect to `url_for("main.app")`
- ✅ Frontend handles admin tab via `#admin` hash

---

### REQ-017: Dev Mode Test Logins (P0) ✅

Display 4 clickable test login buttons on the login page.

**Status: ✅ IMPLEMENTED (January 2026)**

| Role    | Button Label | Credentials     |
| ------- | ------------ | --------------- |
| Trainee | 🎓 Trainee   | trainee/trainee |
| Support | 🛠️ Support   | support/support |
| Staff   | 👤 Staff     | staff/staff     |
| Admin   | 👑 Admin     | admin/password  |

**Implementation:**

- ✅ Buttons styled in `templates/login.html` with role icons
- ✅ Each button submits to `/auth/dev-login` with credentials
- ✅ Buttons shown only when Azure credentials not configured
- ✅ CSS styling in `static/css/main.css`

---

### REQ-018: Hour Type Filter (P1) ✅

Add filter on Admin Dashboard to show only timesheets containing specific hour types.

**Status: ✅ IMPLEMENTED (January 2026)**

**Options:**

- ✅ All Hour Types (default)
- ✅ Field Hours Only
- ✅ Internal Hours Only
- ✅ Training Only
- ✅ Mixed (multiple types)

**Implementation:**

- ✅ Dropdown added to admin dashboard filter bar
- ✅ Backend queries entries table to find matching timesheets
- ✅ Works alongside status and user filters

---

### REQ-019: Export Format Options (P1)

Add export functionality with multiple format options:

| Format | Description                             |
| ------ | --------------------------------------- |
| CSV    | Comma-separated values for Excel import |
| Excel  | Native .xlsx format                     |
| PDF    | Formatted printable report              |

**Export Scope:**

- Current filtered view (all visible timesheets)
- Single timesheet detail view
- Pay period summary

**Status: ✅ IMPLEMENTED (January 10, 2026)**

**Implementation:**

- ✅ Export endpoints for CSV, Excel (.xlsx), and PDF
- ✅ Admin dashboard format selector + export buttons
- ✅ Single timesheet detail export with summary + entries
- ✅ Pay period summary export (admin-only)

---

### REQ-020: Travel Flag Visibility (P1) ✅

Show travel status prominently on admin timesheet list.

**Status: ✅ IMPLEMENTED (January 2026)**

**Features:**

- ✅ Travel indicator ✈️ badge on timesheet cards
- ✅ Expense indicator 💰 badge on timesheet cards
- ✅ Visual prominence in admin card component

**Implementation:**

- ✅ `traveled` and `has_expenses` flags displayed in `admin.js` card rendering
- ✅ Badge styling in `components.css`
- ✅ Icons visible at a glance in timesheet list

---

### REQ-021: Per-Option Reimbursement Attachments (P1)

Each reimbursement type should have its own attachment requirement:

| Reimbursement Type | Attachment Required         |
| ------------------ | --------------------------- |
| Car                | Mileage log or receipt      |
| Flight             | Flight receipt/confirmation |
| Food               | Receipt(s)                  |
| Other              | Supporting documentation    |

**Implementation Notes:**

- Extend Attachment model to link to reimbursement type
- Validate each selected reimbursement type has attachment
- Show warning if missing (similar to Field Hours warning)

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Implementation:**

- ✅ Attachments tagged with reimbursement type
- ✅ UI warning for missing reimbursement receipts
- ✅ Submit flow warns and marks as Needs Approval when missing

---

### REQ-022: Holiday Awareness & Warning (P1)

Display holidays on the time entry grid and show a confirmation warning when users enter hours on a holiday.

**Features:**

- **Holiday Indicators:** Visually mark holidays on the calendar/grid (e.g., colored cell, icon, label)
- **Holiday List:** Maintain list of company-observed holidays (configurable)
- **Double-Verification Warning:** When a user enters hours on a holiday:
  - Display confirmation dialog: "This day is a holiday ([Holiday Name]). Are you sure you want to enter hours?"
  - User must confirm to proceed
  - Works for all hour types (Field, Internal, Training, etc.)
- **Holiday Hour Type:** Users can still select "Holiday" hour type for holiday pay

**Implementation Notes:**

- Store holidays in database (date, name, year) or configuration file
- Check entry dates against holiday list on input
- Show warning modal before saving hours on holiday
- Consider making holidays configurable per year
- Visual indicator should be visible before user enters hours

**Holiday Examples (US):**

- New Year's Day
- Memorial Day
- Independence Day (July 4th)
- Labor Day
- Thanksgiving
- Christmas Day

---

### REQ-023: Read-Only Submitted Timesheets (P0) ✅

Submitted timesheets should be read-only. Users should not be able to edit a timesheet after submission until an admin rejects it.

**Status: ✅ IMPLEMENTED (January 8, 2026)**

**Behavior:**

| Status         | Editable | Can Add Hours | Can Submit | Can Delete |
| -------------- | -------- | ------------- | ---------- | ---------- |
| Draft (NEW)    | ✅ Yes   | ✅ Yes        | ✅ Yes     | ✅ Yes     |
| Submitted      | ❌ No    | ❌ No         | ❌ No      | ❌ No      |
| Needs Approval | ✅ Yes   | ✅ Yes        | ✅ Yes     | ❌ No      |
| Approved       | ❌ No    | ❌ No         | ❌ No      | ❌ No      |

> **Decision Made:** `NEEDS_APPROVAL` (rejected) timesheets are fully editable so users can fix issues and resubmit.

**Implementation:**

- ✅ Added `isTimesheetEditable(status)` helper function
- ✅ `setFormReadOnly()` hides all edit controls for non-editable statuses
- ✅ Read-only notice banner displays status-specific message
- ✅ Backend routes updated to allow `NEEDS_APPROVAL` editing
- ✅ See [BUGS.md](BUGS.md) BUG-001 for full details

---

### REQ-024: Travel Mileage Tracking (P1)

When "Traveled this week" is checked in Additional Information, display a **Travel Details** section for mileage entry.

**Current Bug:**

- Checking "Traveled this week" does not reveal any additional input fields
- No way to track miles driven or travel method

**Required UI Elements:**

| Field                 | Type     | Description                                   | Validation              |
| --------------------- | -------- | --------------------------------------------- | ----------------------- |
| **Miles Traveled**    | Number   | Total miles driven for the week               | Min: 0, Max: 9999       |
| **Starting Location** | Text     | Origin address or city                        | Optional, max 100 chars |
| **Destination**       | Text     | Destination address or city                   | Optional, max 100 chars |
| **Travel Method**     | Dropdown | Car (Personal), Car (Company), Rental, Flight | Required when traveled  |

**Display Logic:**

- Show "Travel Details" section ONLY when "Traveled this week" checkbox is checked
- Collapse/hide section when unchecked
- Calculate mileage reimbursement rate (configurable, e.g., $0.67/mile IRS rate)

**Implementation Notes:**

- Add `miles_traveled` field to Timesheet model (nullable integer)
- Add `travel_method` enum field to Timesheet model
- Connect to Reimbursement Details if travel reimbursement is also needed
- Admin view should display travel icons based on travel_method

---

### REQ-025: Expanded Expense Type Dropdown (P1)

Expand the reimbursement expense type dropdown to include all common business expense categories.

**Current State:**

| Option  | Status     |
| ------- | ---------- |
| Car     | ✅ Exists  |
| Flight  | ✅ Exists  |
| Food    | ✅ Exists  |
| Other   | ✅ Exists  |
| Hotel   | ❌ Missing |
| Gas     | ❌ Missing |
| Parking | ❌ Missing |
| Toll    | ❌ Missing |

**Required Dropdown Options:**

| Expense Type | Icon | Attachment Required       |
| ------------ | ---- | ------------------------- |
| Car          | 🚗   | Mileage log               |
| Gas          | ⛽   | Gas station receipt       |
| Hotel        | 🏨   | Hotel folio/receipt       |
| Flight       | ✈️   | Flight confirmation       |
| Food         | 🍽️   | Receipt(s)                |
| Parking      | 🅿️   | Parking receipt           |
| Toll         | 🛣️   | Toll receipt or statement |
| Other        | 📄   | Supporting documentation  |

**Implementation Notes:**

- Update `reimbursement_type` enum in database schema
- Update frontend dropdown in timesheet form
- Each expense type should allow optional notes field
- Support multiple expenses of same type (e.g., multiple meals)

---

### REQ-026: Expense Amount Validation (P1)

Prevent null, empty, or invalid values in expense amount fields to avoid displaying "$null" or "$undefined".

**Current Bug:**

- Expense entries display "Car: $null" when amount is not properly set
- No client-side validation prevents empty submissions
- Backend accepts null values for reimbursement amounts

**Required Validation:**

| Rule                        | Client-Side       | Server-Side              |
| --------------------------- | ----------------- | ------------------------ |
| Amount must be a number     | ✅ type="number"  | ✅ Decimal validation    |
| Amount cannot be null/empty | ✅ required field | ✅ NOT NULL or default 0 |
| Amount must be ≥ $0.00      | ✅ min="0"        | ✅ Check constraint      |
| Amount must be ≤ $10,000    | ✅ max="10000"    | ✅ Check constraint      |
| Amount max 2 decimal places | ✅ step="0.01"    | ✅ Decimal(10,2)         |

**UI Improvements:**

- Display currency symbol ($) prefix in input field
- Default placeholder: "0.00" (not empty)
- If user clears field and submits, auto-set to $0.00
- Show inline error message for invalid amounts

**Display Formatting:**

- Always display amounts as "$X.XX" format (e.g., "$45.00" not "$45")
- For zero amounts, display "$0.00" (not "$null" or empty)
- Format negative refunds as "-$X.XX" if applicable

**Database Migration:**

- Add DEFAULT 0.00 to reimbursement_amount column
- Update existing NULL values to 0.00
- Add CHECK constraint: amount >= 0 AND amount <= 10000

**Implementation Notes:**

- Add client-side validation in timesheet form JavaScript
- Add server-side validation in `/api/timesheets` endpoint
- Update display logic in admin dashboard to handle edge cases
- Add unit tests for amount validation

---

### REQ-027: "Has Expenses" Expense Details Section (P1)

When "Has expenses" is checked in Additional Information, display an **Expense Details** section for tracking business expenses.

**Current Bug:**

- Checking "Has expenses" does not reveal any additional input fields
- Users have no way to itemize or describe their expenses
- Only "Reimbursement needed" shows the reimbursement section

**Required UI Behavior:**

| Checkbox             | Shows Section         | Purpose                                 |
| -------------------- | --------------------- | --------------------------------------- |
| Traveled this week   | Travel Details        | Mileage, destination (see REQ-024)      |
| Has expenses         | Expense Summary       | Quick note about expenses incurred      |
| Reimbursement needed | Reimbursement Details | Detailed expense line items for payment |

**Expense Summary Section (when "Has expenses" checked):**

| Field               | Type     | Description                            | Validation            |
| ------------------- | -------- | -------------------------------------- | --------------------- |
| **Expense Summary** | Textarea | Brief description of expenses incurred | Max 500 chars         |
| **Total Estimated** | Number   | Estimated total expense amount         | Optional, $0-$10,000  |
| **Paid By**         | Dropdown | Company Card, Personal, Mixed          | Required when checked |

**Display Logic:**

- Show "Expense Summary" section ONLY when "Has expenses" checkbox is checked
- If BOTH "Has expenses" AND "Reimbursement needed" are checked:
  - Show both sections
  - "Reimbursement Details" inherits context from "Expense Summary"
- Collapse/hide section when unchecked

**Implementation Notes:**

- Add `expense_summary` text field to Timesheet model
- Add `expense_paid_by` enum (company_card, personal, mixed)
- This section is for general expense acknowledgment
- Detailed reimbursement line items go in "Reimbursement Details" section

---

### REQ-028: Multiple Reimbursement Line Items (P1) ✅

Allow users to add multiple reimbursement entries, one for each expense requiring reimbursement.

**Status: ✅ IMPLEMENTED (January 8, 2026)**

**Previous State:**

- Only ONE reimbursement entry was possible (single Type/Amount/Date row)
- Could not track multiple expenses (e.g., gas + hotel + meals)

**Required UI:**

```
Reimbursement Details
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
| Type      | Amount    | Date       | Notes      | ✕ |
|-----------|-----------|------------|------------|---|
| 🏨 Hotel  | $129.99   | 01/06/2026 | Marriott   | ✕ |
| ⛽ Gas    | $45.00    | 01/07/2026 | Round trip | ✕ |
| 🍽️ Food   | $32.50    | 01/07/2026 | Lunch mtg  | ✕ |
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                              Total: $207.49

              [+ Add Expense]
```

**Features:**

- **Add Button:** "+ Add Expense" to create new line item
- **Remove Button:** "✕" to delete a line item
- **Running Total:** Display sum of all amounts at bottom
- **Notes Field:** Optional brief description per expense
- **Date Field:** Date expense was incurred
- **Type Icons:** Display emoji icons for each expense type (see REQ-025)

**Data Model:**

| Field     | Type          | Description                    |
| --------- | ------------- | ------------------------------ |
| id        | Integer       | Primary key                    |
| timesheet | Foreign Key   | Links to parent Timesheet      |
| type      | Enum          | Expense type (REQ-025 options) |
| amount    | Decimal(10,2) | Expense amount                 |
| date      | Date          | Date expense incurred          |
| notes     | String(200)   | Optional description           |

**Validation:**

- At least one line item required if "Reimbursement needed" is checked
- Each line item requires: Type + Amount (Notes/Date optional)
- Amount validation per REQ-026 (no null, $0-$10,000 range)
- Total sum displayed and saved to timesheet.total_reimbursement

**Implementation Notes:**

- ✅ Created `ReimbursementItem` model in `app/models/reimbursement.py`
- ✅ Added relationship to `Timesheet` model
- ✅ Updated `update_timesheet` route to handle `reimbursement_items` array
- ✅ Frontend: Dynamic form with add/remove buttons in `timesheet.js`
- ✅ CSS styling for line items in `components.css`
- ✅ Database migration: `004_add_reimbursement_items.py`
- ✅ Backward compatibility: Legacy `reimbursement_amount` field updated with total

---

## Security & Production Readiness

### REQ-029: Production Database Lifecycle (P0) ✅

Migrations should be the only schema management mechanism in production.

**Status: ✅ IMPLEMENTED (January 8, 2026)**

**Required Behavior:**

- Remove automatic `db.create_all()` on app startup
- Apply schema changes only via Alembic/Flask-Migrate
- Deployment step runs `flask db upgrade` before starting web workers

**Implementation:**

- ✅ Removed `db.create_all()` from `app/__init__.py` factory
- ✅ Created `docker/entrypoint.sh` that runs `flask db upgrade` before Gunicorn
- ✅ Updated `docker/Dockerfile` to use entrypoint script
- ✅ Schema is now exclusively managed via Flask-Migrate

---

### REQ-030: Authentication & Session Hardening (P0)

Ensure the OIDC flow and session handling meet production security expectations.

**Required Behavior:**

- Validate `state` and `nonce` in the MSAL callback
- Enforce strict redirect URI handling
- Harden session cookies: `Secure`, `HttpOnly`, `SameSite`
- Dev auth bypass only when explicitly enabled (not when env vars are missing)

---

### REQ-031: CSRF Protection for Mutating Endpoints (P0) ✅

All authenticated `POST`/`PUT`/`DELETE` routes must require a CSRF token.

**Status: ✅ IMPLEMENTED (January 8, 2026)**

**Implementation:**

- ✅ Added Flask-WTF CSRFProtect extension (`flask-wtf>=1.2.0`)
- ✅ CSRF extension initialized in app factory (`app/__init__.py`)
- ✅ CSRF token exposed via `<meta name="csrf-token">` tag in base template
- ✅ JavaScript API client reads token from meta tag for AJAX requests
- ✅ All POST/PUT/DELETE/PATCH requests include `X-CSRFToken` header
- ✅ Form submissions include `csrf_token` hidden input (e.g., logout form)

---

### REQ-032: Security Baseline & Audit (P1) ✅

Adopt the pre-deployment security checklist and keep it enforceable.

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Minimum Checklist:**

- Strong `SECRET_KEY`, no placeholder credentials in production
- Dependency scanning (e.g., Dependabot, safety, bandit)
- Container hardening (non-root user, updated base images)
- Rate limiting on sensitive endpoints (login, notifications)
- Admin action audit logging
- Explicit CORS/CSP policy if enabled
- See [SECURITY.md](SECURITY.md) for the full checklist

**Implementation:**

- ✅ Comprehensive security checklist in SECURITY.md (50+ items)
- ✅ Security audit performed with pass status
- ✅ Rate limiting implemented (REQ-042)
- ✅ Structured audit logging (REQ-036)
- ✅ Non-root container user confirmed
- ✅ CSRF protection enabled (REQ-031)
- ⚠️ HTTPS/production secrets pending (documented)

---

### REQ-033: Attachment Storage Strategy (P1) ✅

Finalize durable attachment storage for production scaling.

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Required Behavior:**

- Decide between SharePoint sync (REQ-010) and object storage (S3/R2), or both
- Store attachment metadata in Postgres with stable storage keys
- Support multi-instance web deployment without shared filesystem
- Use signed URLs for downloads if object storage is selected
- Consider malware scanning for untrusted uploads

**Implementation:**

- ✅ Created `app/utils/storage.py` with:
  - Abstract `StorageBackend` base class
  - `LocalStorageBackend` for development
  - `S3StorageBackend` for AWS S3 production
  - `R2StorageBackend` for Cloudflare R2 alternative
  - Signed URL generation for secure downloads
- ✅ Configuration via `STORAGE_BACKEND` env var
- ⚠️ Migration script pending (to move existing files)

---

### REQ-034: Background Jobs & Scheduled Notifications (P1) ✅

Move long-running work and reminders to a job queue.

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Required Behavior:**

- Use RQ or Celery for notifications, exports, and sync jobs
- Add retries and dead-letter handling
- Implement daily unsubmitted reminders (Mon-Fri) and weekly reminders
- Persist notification outcomes in the Notification table

**Implementation:**

- ✅ Created `app/jobs/__init__.py` with:
  - RQ-based job queue integration
  - `enqueue_notification()` for async notifications
  - `send_daily_reminders_job()` for Mon-Fri reminders
  - `send_weekly_reminders_job()` for Friday reminders
  - Scheduler integration with rq-scheduler
  - CLI commands (`flask jobs daily_reminders`, etc.)
- ⚠️ Requires `pip install rq rq-scheduler` for full functionality

---

### REQ-035: API Validation & Error Handling (P1) ✅

Standardize request validation and error responses.

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Required Behavior:**

- Validate request bodies (Marshmallow, Pydantic, or equivalent)
- Use a consistent error shape: `{ "error": "...", "code": "...", "details": {...} }`
- Add global exception handlers with request IDs in logs

**Implementation:**

- ✅ Created `app/utils/errors.py` with:
  - Standardized error codes (ErrorCode class)
  - Custom exception classes (APIError, ValidationError, NotFoundError, etc.)
  - Request ID middleware (X-Request-ID header)
  - Global exception handlers for all HTTP status codes
- ✅ Created `app/utils/validation.py` with:
  - Field class for schema-based validation
  - Common validators (validate_uuid, validate_date, validate_positive_number, etc.)
  - `@validate_json_body` decorator for route protection
- ✅ Registered error handlers in Flask app factory

---

### REQ-036: Observability & Metrics (P1) ✅

Add structured logging and basic operational metrics.

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Required Behavior:**

- Structured JSON logs with request_id, user_id, route, latency
- Generate `X-Request-ID` if missing and propagate
- Metrics for request duration, error rate, queue depth, DB/Redis errors

**Implementation:**

- ✅ Created `app/utils/observability.py` with:
  - `JSONFormatter` - Structured JSON log output
  - `RequestMetrics` - Request duration, error rate, top routes
  - X-Request-ID generation and propagation
  - X-Response-Time header with request duration
  - Automatic slow request detection (>1s)
- ✅ Added `/metrics` endpoint (admin-only) for monitoring
- ✅ Registered middleware in Flask app factory

---

### REQ-037: Testing Coverage & Gaps (P1) ✅

Close the top coverage gaps and raise overall coverage to 90%+.

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Required Tests:**

- ✅ `app/utils/sms.py` utilities (Twilio config + formatting)
- ✅ `app/services/notification.py` flows
- `app/routes/events.py` SSE stream + pub/sub (integration with E2E tests)
- `app/routes/timesheets.py` attachment upload + notes CRUD (covered by E2E)
- `app/routes/auth.py` MSAL flow + dev bypass (covered by E2E)
- See [TESTING.md](TESTING.md) for the full test plan and fixtures

**Implementation:**

- ✅ Added `tests/test_validation.py` - Field class, validators, schema validation
- ✅ Added `tests/test_errors.py` - Error codes, exceptions, error response helpers
- ✅ Added `tests/test_sms.py` - Twilio config, send_sms, phone formatting
- ✅ Added `tests/test_notification.py` - Notification service flows

---

## UX & Accessibility

### REQ-038: UX & Accessibility Backlog (P2)

Complete the remaining UI/UX items from supporting docs.

**Status: ✅ IMPLEMENTED (January 2026)**

**Scope:**

- Microsoft-style login page parity (LOGIN.md)
- Responsive enhancements: swipe gestures, orientation, print styles (RESPONSIVE.md)
- Dark mode review: logo treatment, brand compliance, print styles, prefers-color-scheme (DARKMODE.md)
- Accessibility audit: keyboard navigation, focus visibility, contrast
- UI refactor patterns reference (UI.md)
- Use [WALKTHROUGH.md](WALKTHROUGH.md) for end-user flow validation

**Implementation Notes:**

- Microsoft-style login template + stylesheet with dev-mode panel
- Added swipe gestures for mobile navigation and landscape tweaks
- Added print styles and light-mode tokens via `prefers-color-scheme`
- Improved focus-visible states and logo swapping for light mode

---

### REQ-039: PowerApps Data Report View (P2)

Implement the missing PowerApps `Screen1` data report view.

**Status: ✅ IMPLEMENTED (January 2026)**

**Implementation Notes:**

- Build a read-only data table view for raw entries
- Decide routing (admin-only vs separate report page)
- Preserve parity with the original PowerApps report fields (POWERAPPS.md)

**Implementation:**

- Admin-only data report view with filters + pagination
- Raw timesheet entries with user + totals context

---

## Developer Tooling

### REQ-040: MCP Tooling Integration (P3) - Deferred

> **Status:** 🔄 Deferred - Not actively used. See [MCP.md](MCP.md) for reference.

Optional AI tooling integration using Model Context Protocol (MCP) servers. This was explored but determined to add complexity without sufficient benefit for this project.

**Assessment:**

- MCP is not currently used in this project
- Direct API integrations (Microsoft Graph, PostgreSQL, Twilio) are preferred
- Document retained for future reference if MCP becomes relevant

---

### REQ-041: Support Dashboard for Trainee Approvals (P1) ✅

Support users should have access to an Admin Dashboard, but it should only display trainee training timesheets that require their approval.

**Status: ✅ IMPLEMENTED (January 8, 2026)**

**Previous Bug:**

- Support users did not see any Admin Dashboard option
- Support users could not access timesheets they are authorized to approve (per REQ-001)

**Required Behavior:**

| Role    | Dashboard Access | Visible Timesheets      |
| ------- | ---------------- | ----------------------- |
| Trainee | ❌ None          | N/A                     |
| Support | ✅ Limited       | Trainee timesheets only |
| Staff   | ❌ None          | N/A                     |
| Admin   | ✅ Full          | All timesheets          |

**Features:**

- ✅ Show "Trainee Approvals" navigation link for Support role
- ✅ Filter dashboard to show ONLY timesheets submitted by users with role = `trainee`
- ✅ Support can Approve/Reject trainee timesheets
- ✅ Support cannot see Staff or other Support timesheets

**UI Differences from Full Admin Dashboard:**

- ✅ Title: "Trainee Approvals" instead of "Admin Dashboard"
- ✅ No access to system settings or user management (list_users remains admin-only)
- ✅ Only approval-related actions available

**Implementation Notes:**

- ✅ Added `_can_access_timesheet()` helper for role-based authorization
- ✅ Changed all approval endpoints from `@admin_required` to `@can_approve`
- ✅ Added role-based filtering in `list_timesheets()` for Support users
- ✅ Updated sidebar navigation in `templates/index.html`
- ✅ Dashboard returns `view_mode` to frontend for UI customization

---

## Production Hardening (from CHECKIN.md Analysis)

### REQ-042: Rate Limiting on Auth Endpoints (P1) ✅

Protect authentication endpoints from brute-force attacks.

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Required Behavior:**

- Apply rate limiting to `/auth/login`, `/auth/dev-login`, `/auth/callback`
- Use Flask-Limiter with Redis backend
- Return 429 Too Many Requests after threshold
- Log rate limit violations

**Implementation:**

- ✅ Added Flask-Limiter>=3.5.0 to requirements.txt
- ✅ Configured limiter extension in `app/extensions.py`
- ✅ Rate limits applied to auth endpoints in `app/routes/auth.py`
- ✅ Custom 429 error handler with JSON responses for API endpoints
- ✅ Rate limit headers (X-RateLimit-\*) enabled in responses
- ✅ Configurable via environment variables:
  - `RATELIMIT_AUTH_LIMIT`: Auth endpoints (default: 10/minute)
  - `RATELIMIT_API_LIMIT`: API endpoints (default: 30/minute)
- ✅ Redis backend for production (memory for tests)
- ✅ Rate limit violations logged with IP and path

**Rate Limits Applied:**

| Endpoint          | Limit  | Purpose                        |
| ----------------- | ------ | ------------------------------ |
| `/auth/login`     | 10/min | Prevent login brute-force      |
| `/auth/dev-login` | 10/min | Prevent dev auth abuse         |
| `/auth/callback`  | 20/min | OAuth callback (higher margin) |
| `/auth/me`        | 30/min | API-level rate limiting        |

---

### REQ-043: Health Check Endpoint (P1)

Add health check endpoint for load balancers and monitoring.

**Required Behavior:**

- `GET /health` returns 200 OK when app is healthy
- Check database connectivity
- Check Redis connectivity (if used)
- Return 503 if any dependency is down

**Implementation Notes:**

- Should not require authentication
- Include version info in response: `{ "status": "healthy", "version": "1.0.0" }`
- Useful for Docker health checks and Kubernetes probes

---

### REQ-044: Frontend Modularization (P1) ✅

Split `timesheet.js` (1,400+ lines) into maintainable modules.

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Required Behavior:**

- Separate concerns: API calls, state management, DOM rendering
- Extract reusable components: toast notifications, modals, validation
- Enable parallel development without merge conflicts

**Module Structure:**

```
static/js/timesheet/
├── state.js        # ✅ Centralized state management with events
├── dates.js        # ✅ Date utilities, holidays, formatting
├── entries.js      # ✅ Time entry row add/remove/collect
├── attachments.js  # ✅ File upload, validation, display
└── index.js        # ✅ Module exports and initialization
```

**Implementation:**

- ✅ Created `static/js/timesheet/state.js` - Event-driven state management
- ✅ Created `static/js/timesheet/dates.js` - Date utilities with holidays
- ✅ Created `static/js/timesheet/entries.js` - Entry row management
- ✅ Created `static/js/timesheet/attachments.js` - File upload handling
- ✅ Created `static/js/timesheet/index.js` - Module aggregation
- ✅ Integrated with `templates/index.html` - All modules loading
- ⏳ Full migration from legacy timesheet.js is incremental

**Risk Mitigation:**

- E2E tests (REQ-046) in place to catch regressions
- Modules load alongside legacy code for gradual migration
- See [CHECKIN.md](CHECKIN.md) for detailed analysis

---

### REQ-045: Backup/Restore Documentation (P1) ✅

Document database backup and restore procedures.

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Required Behavior:**

- Document `pg_dump` command for PostgreSQL backups
- Document restore procedure
- Include attachment backup strategy
- Provide cron job example for automated backups

**Implementation:**

- ✅ Created [docs/BACKUP.md](BACKUP.md) with:
  - Database backup commands (Docker and direct)
  - Restore procedures with examples
  - Attachment backup/restore
  - Automated backup scripts and cron jobs
  - AWS S3 cloud backup instructions
  - Complete disaster recovery procedure
  - Backup verification checklist

---

### REQ-046: E2E Tests with Playwright (P1) ✅

Add end-to-end browser tests for critical user flows.

**Status: ✅ IMPLEMENTED (January 9, 2026)**

**Required Behavior:**

- Test happy paths: login, create timesheet, submit, admin approval
- Catch regressions before they reach production
- Run in CI/CD pipeline

**Test Coverage Implemented:**

| Flow                                       | File              | Priority |
| ------------------------------------------ | ----------------- | -------- |
| Dev login → Dashboard loads                | auth.spec.js      | P0       |
| Create new timesheet → Save draft          | timesheet.spec.js | P0       |
| Add time entries → Submit → Confirm        | timesheet.spec.js | P0       |
| Admin login → View timesheets → Approve    | admin.spec.js     | P0       |
| Upload attachment → Verify display         | timesheet.spec.js | P1       |
| CSRF protection (POST without token fails) | csrf.spec.js      | P1       |

**Implementation:**

- ✅ Playwright configuration in `playwright.config.js`
- ✅ Test fixtures with authenticated page contexts in `tests/e2e/fixtures.js`
- ✅ Authentication tests in `tests/e2e/auth.spec.js`
- ✅ Timesheet CRUD tests in `tests/e2e/timesheet.spec.js`
- ✅ Admin dashboard tests in `tests/e2e/admin.spec.js`
- ✅ CSRF protection tests in `tests/e2e/csrf.spec.js`
- ✅ NPM scripts: `npm run test:e2e`, `test:e2e:headed`, `test:e2e:docker`
- ✅ Docker Compose for E2E testing in `docker/docker-compose.e2e.yml`
- ✅ Documentation updated in `TESTING.md`

---

## ✅ Implementation Status

| Requirement | Status      | Description                          | Key Files                                                                                                       |
| ----------- | ----------- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| REQ-001     | ✅ Complete | Four-tier role system                | `app/models.py` (UserRole enum), `app/routes/admin.py`                                                          |
| REQ-002     | ✅ Complete | Dev mode test accounts               | `app/routes/auth.py` (`/auth/dev-login`)                                                                        |
| REQ-003     | ✅ Complete | User notification preferences        | `static/js/settings.js`, `templates/index.html` (#settings-view)                                                |
| REQ-004     | ✅ Complete | Pay period filter                    | `static/js/admin.js` (`getCurrentPayPeriod()`), `static/css/components.css`                                     |
| REQ-005     | ✅ Complete | Current week filter                  | `static/js/admin.js` (`admin-this-week-btn` handler)                                                            |
| REQ-006     | ✅ Complete | Pay period confirmation              | `app/routes/admin.py`, `app/models.py` (PayPeriod), `migrations/versions/006_add_pay_periods.py`                |
| REQ-007     | ✅ Complete | Column totals                        | `static/js/timesheet.js` (`updateColumnTotals()`)                                                               |
| REQ-008     | ✅ Complete | Row totals                           | `static/js/timesheet.js` (`updateRowTotal()`)                                                                   |
| REQ-009     | ✅ Complete | Auto-fill any hour type              | `static/js/timesheet.js` (`addHourTypeRow()`)                                                                   |
| REQ-010     | ✅ Complete | SharePoint sync                      | `app/services/sharepoint.py`, `app/jobs/sharepoint_sync.py`                                                     |
| REQ-011     | ✅ Complete | Email notifications                  | `app/services/email.py`, `templates/email/`, `docs/EMAIL.md`                                                    |
| REQ-012     | ✅ Complete | Teams bot notifications              | `app/routes/bot.py`, `app/services/teams.py`, `docs/BOT.md`                                                     |
| REQ-013     | ✅ Complete | Trainee hour type restriction        | `static/js/timesheet/entries.js`, `app/routes/timesheets.py`                                                    |
| REQ-014     | ✅ Complete | Submit without attachment warning    | `static/js/app.js` (`checkFieldHoursAttachment()`)                                                              |
| REQ-015     | ✅ Complete | Azure AD integration                 | `app/routes/auth.py`, `app/config.py`, `docs/AZURE.md`                                                          |
| REQ-016     | ✅ Complete | Auto-redirect after login            | `app/routes/auth.py` (redirect to `url_for("main.app")`)                                                        |
| REQ-017     | ✅ Complete | Dev login buttons                    | `templates/login.html`                                                                                          |
| REQ-018     | ✅ Complete | Hour type filter                     | `static/js/admin.js`, `templates/index.html` (#admin-hour-type-filter)                                          |
| REQ-019     | ✅ Complete | Export formats (CSV/XLSX/PDF)        | `app/routes/admin.py` (`/api/admin/export/`), `app/services/export.py`                                          |
| REQ-020     | ✅ Complete | Travel/expense badges                | `static/js/admin.js` (card rendering), `static/css/components.css`                                              |
| REQ-021     | ✅ Complete | Per-option reimbursement attachments | `app/models.py` (Attachment.reimbursement_type), `migrations/versions/007_add_attachment_reimbursement_type.py` |
| REQ-022     | ✅ Complete | Holiday awareness & warning          | `static/js/timesheet.js` (HOLIDAYS, checkHolidayInput), `static/css/components.css`                             |
| REQ-023     | ✅ Complete | Read-only submitted timesheets       | `static/js/timesheet.js` (`setFormReadOnly()`), `docs/BUGS.md` (BUG-001)                                        |
| REQ-024     | 📋 Planned  | Travel mileage tracking              | —                                                                                                               |
| REQ-025     | 📋 Planned  | Expanded expense types               | —                                                                                                               |
| REQ-026     | ✅ Complete | Expense amount validation            | `static/js/timesheet.js` (`validateReimbursementItems()`), `docs/BUGS.md` (BUG-002)                             |
| REQ-027     | ✅ Complete | Has expenses section                 | `templates/index.html` (#expense-section)                                                                       |
| REQ-028     | ✅ Complete | Multiple reimbursement items         | `app/models.py` (ReimbursementItem), `static/js/timesheet.js`                                                   |
| REQ-029     | ✅ Complete | Production DB lifecycle              | `docker/entrypoint.sh`, `migrations/`                                                                           |
| REQ-030     | ✅ Partial  | Auth/session hardening               | `app/routes/auth.py`, `docs/SECURITY.md`                                                                        |
| REQ-031     | ✅ Complete | CSRF protection                      | `app/__init__.py` (Flask-WTF), `static/js/api.js`                                                               |
| REQ-032     | ✅ Complete | Security audit                       | `docs/SECURITY.md`                                                                                              |
| REQ-033     | ✅ Complete | Object storage abstraction           | `app/services/storage.py`                                                                                       |
| REQ-034     | ✅ Complete | Background jobs module               | `app/jobs/`                                                                                                     |
| REQ-035     | ✅ Complete | API validation module                | `app/validation.py`, `app/routes/timesheets.py`                                                                 |
| REQ-036     | ✅ Complete | Observability & logging              | `app/logging_config.py`, `app/routes/health.py`                                                                 |
| REQ-037     | ✅ Complete | Unit test coverage                   | `tests/` (validation, sms, notifications, auth)                                                                 |
| REQ-038     | ✅ Complete | UX & accessibility                   | `static/css/components.css`, `templates/index.html`                                                             |
| REQ-039     | ✅ Complete | Admin data report view               | `static/js/admin.js` (#admin-reports-view), `app/routes/admin.py`                                               |
| REQ-040     | 📋 Deferred | MCP tooling integration              | —                                                                                                               |
| REQ-041     | ✅ Complete | Support dashboard                    | `static/js/admin.js`, `app/routes/admin.py`                                                                     |
| REQ-042     | ✅ Complete | Rate limiting                        | `app/__init__.py` (Flask-Limiter), `app/routes/auth.py`                                                         |
| REQ-043     | ✅ Complete | Health check endpoint                | `app/routes/health.py` (`/health`)                                                                              |
| REQ-044     | ✅ Complete | Frontend JS modularization           | `static/js/timesheet/` (state, dates, entries, attachments, index)                                              |
| REQ-045     | ✅ Complete | Backup/restore documentation         | `docs/BACKUP.md`                                                                                                |
| REQ-046     | ✅ Complete | E2E tests (Playwright)               | `tests/e2e/`, `playwright.config.js`, `docs/TESTING.md`                                                         |
| REQ-047     | 📋 Planned  | User theme selection                 | `static/css/main.css`, `static/css/light-mode-backup/`                                                          |
| REQ-048     | 📋 Planned  | Architecture diagram                 | Add to `docs/IMPLEMENTATION.md` (from CHECKIN.md §8)                                                            |
| REQ-049     | 📋 Planned  | API versioning                       | Add `/api/v1/` prefix, version header support (from CHECKIN.md §4)                                              |
| REQ-050     | 📋 Planned  | OpenAPI/Swagger spec                 | Document API contract for frontend developers (from CHECKIN.md §5)                                              |
| REQ-051     | ✅ Complete | CONTRIBUTING.md                      | `/CONTRIBUTING.md` — clone, run, test, deploy guide                                                             |
| REQ-052     | 📋 Future   | Database-driven hour types           | Make hour types configurable without code changes (from CHECKIN.md §4)                                          |
| REQ-053     | ✅ Complete | Unsaved changes warning              | `static/js/timesheet.js`, `static/js/app.js` — shows/hides warning on form changes                              |
| REQ-054     | ✅ Complete | Daily totals row                     | `static/js/timesheet.js`, `static/css/components.css` — Day Total row shows daily & weekly hour sums            |
| REQ-055     | ✅ Complete | Day hours cap at 24                  | `static/js/timesheet.js` — validates and caps daily total to 24h with toast warning                             |
| REQ-056     | ✅ Complete | Future week submission warning       | `static/js/app.js` lines 295-321 — warns on Submit if week ends after today, shows confim dialog                |
| REQ-057     | 📋 Planned  | UI Redesign (Premium)                | See REQ-057 breakdown: gradient buttons, SVG icons, dark theme polish                                           |
| REQ-058     | 📋 Planned  | Notification prompt popup            | Mint green banner (`#86efac`) prompting users to enable notifications                                           |

---

_Document maintained as the authoritative source for feature requirements. For other topics, see:_

- _Bugs: [`BUGS.md`](BUGS.md)_
- _Security: [`SECURITY.md`](SECURITY.md)_
- _Testing: [`TESTING.md`](TESTING.md)_
- _Roadmap: [`roadmap.md`](roadmap.md)_

_Last updated: January 13, 2026_
