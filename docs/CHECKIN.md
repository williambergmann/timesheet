# Project Health Check-In

> **Purpose:** Candid assessment of project risks, technical debt, and improvement priorities.
>
> **Last Updated:** January 11, 2026

---

## 1. Which parts of the project currently carry the highest risk of errors or regressions?

### High Risk Areas:

| Area                           | Risk Level | Reasoning                                                   |
| ------------------------------ | ---------- | ----------------------------------------------------------- |
| **`app/routes/timesheets.py`** | 🔴 High    | Core business logic. 81% covered but logic is complex.      |
| **`app/routes/admin.py`**      | 🔴 High    | 37% test coverage. Export/Reporting logic largely untested. |
| **`app/routes/auth.py`**       | 🟠 Medium  | 44% test coverage. Azure flow mock is needed.               |
| **`static/js/timesheet.js`**   | 🟡 Low-Med | ✅ Improved with modularization and new validation logic.   |

### Why These Are Risky:

- **Low Admin Coverage**: Admin dashboard features (exports) are critical but have low test coverage.
- **Auth Complexity**: Azure AD integration needs robust testing with mocks.

---

## 2. If you had to simplify this project without losing functionality, where would you start and why?

### Recommended Simplification Order:

1. **Extract frontend state management**

   - Move `TimesheetModule` state into a simple store pattern
   - Separate data fetching, state, and rendering concerns

2. **Consolidate CSS files**

   - Merge `main.css`, `components.css`, and inline styles
   - ✅ Dark mode is now forced, simplifying theme logic (REQ-047)

3. **Unify notification services**
   - Create a single `NotificationService` for SMS, Email, Teams

---

## 3. Which problems are not visible yet but will appear as the project grows?

### Hidden Scaling Issues:

| Problem                 | Trigger         | Impact                                              |
| ----------------------- | --------------- | --------------------------------------------------- |
| **Test Suite Slowness** | More tests      | Serial execution taking too long (need parallelism) |
| **N+1 query patterns**  | 100+ timesheets | Slow admin dashboard                                |

---

## 9. Which improvements would deliver the best impact-to-effort ratio in the short term?

### Quick Wins (High Impact, Low Effort):

| Improvement                | Effort  | Impact    | Notes                                                    |
| -------------------------- | ------- | --------- | -------------------------------------------------------- |
| **Cover Admin Routes**     | 1 day   | 🟢 High   | `app/routes/admin.py` is critical but low coverage (37%) |
| **Cover User/Auth Routes** | 1 day   | 🟢 High   | `users.py` (16%) and `auth.py` (44%) need tests          |
| **Mock Teams API**         | 0.5 day | 🟡 Medium | `utils/teams.py` needs isolation for testing             |

### Medium-Term Wins:

- **Background job queue** (3-5 days): Reliable notifications
- **Object storage** (3-5 days): Horizontal scaling

---

## 10. What currently prevents this project from reaching a "production-robust" level?

### Production Blockers:

| Blocker                 | Severity    | Status               | Path to Resolution                                      |
| ----------------------- | ----------- | -------------------- | ------------------------------------------------------- |
| **Test Coverage < 85%** | 🟠 High     | 🔄 In Progress (68%) | Create `test_admin.py`, `test_users.py`, `test_auth.py` |
| **HTTPS/SSL Missing**   | 🔴 Critical | 📋 Planned           | Configure Nginx with Certbot                            |
| **Default DB Password** | 🔴 Critical | 📋 Planned           | Update docker-compose/.env                              |

### Production Readiness Checklist:

- [x] Attachments storage abstraction (REQ-033)
- [x] Background job queue module (REQ-034)
- [ ] 85%+ test coverage (Currently 68%)
- [x] Structured logging with request tracing (REQ-036)
- [x] Rate limiting on auth endpoints (REQ-042)
- [x] Documented backup/restore (REQ-045)
- [x] Security audit passed (REQ-032)

---

## Summary: Top 5 Priorities

1. **Move attachments to object storage** — Unblocks horizontal scaling
2. **Add background job queue** — Reliable notifications, no request blocking
3. **Split and test `timesheet.js`** — Reduce regression risk in core UI
4. **Standardize API responses** — Consistent error handling
5. **Complete auth hardening** — Production security baseline

---

_Document created January 8, 2026, updated January 10, 2026_
