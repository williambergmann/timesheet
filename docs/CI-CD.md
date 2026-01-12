# CI/CD Pipeline

This document describes the continuous integration and deployment pipeline for the Northstar Timesheet application.

---

## GitHub Actions Workflows

### Test Workflow (`.github/workflows/test.yml`)

Runs on every push and pull request to `main` and `develop` branches.

#### Jobs

| Job             | Purpose                  | Duration | Dependencies       |
| --------------- | ------------------------ | -------- | ------------------ |
| `unit-tests`    | Run pytest with coverage | ~2 min   | PostgreSQL, Redis  |
| `e2e-tests`     | Run Playwright E2E tests | ~5 min   | unit-tests, Docker |
| `security-scan` | Run Bandit and Safety    | ~1 min   | None               |

#### Unit Tests Job

- **Python version**: 3.11
- **Services**: PostgreSQL 15, Redis 7
- **Steps**:
  1. Checkout code
  2. Set up Python with pip cache
  3. Install dependencies
  4. Lint with flake8
  5. Run pytest with coverage
  6. Upload coverage to Codecov

#### E2E Tests Job

- **Runs after**: unit-tests (only if they pass)
- **Uses**: Docker Compose for full stack
- **Steps**:
  1. Checkout code
  2. Install Playwright (Chromium only)
  3. Start Docker Compose stack
  4. Wait for application health check
  5. Run Playwright tests
  6. Upload test artifacts (reports, screenshots)
  7. Stop Docker Compose

#### Security Scan Job

- **Tools**: Bandit (code), Safety (dependencies)
- **Behavior**: Warnings don't fail the build (informational)

---

## Pre-commit Hooks

### Installation

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run on all files (first time)
pre-commit run --all-files
```

### Hooks Configured

| Hook                  | Purpose                | Auto-fix |
| --------------------- | ---------------------- | -------- |
| `trailing-whitespace` | Remove trailing spaces | ✅       |
| `end-of-file-fixer`   | Ensure newline at EOF  | ✅       |
| `check-yaml`          | Validate YAML syntax   | ❌       |
| `check-json`          | Validate JSON syntax   | ❌       |
| `black`               | Python code formatting | ✅       |
| `isort`               | Sort Python imports    | ✅       |
| `flake8`              | Python linting         | ❌       |
| `bandit`              | Security linting       | ❌       |
| `detect-secrets`      | Find leaked secrets    | ❌       |
| `pytest-quick`        | Run quick unit tests   | ❌       |

### Skipping Hooks

```bash
# Skip all hooks for one commit
git commit --no-verify -m "WIP: work in progress"

# Skip specific hooks
SKIP=pytest-quick git commit -m "docs: update readme"
```

---

## Codecov Integration

### Setup (One-time)

1. Go to [codecov.io](https://codecov.io) and sign in with GitHub
2. Add the `Northstar-Technologies/timesheet` repository
3. Copy the upload token
4. Add to GitHub repository secrets:
   - Settings → Secrets and variables → Actions
   - New secret: `CODECOV_TOKEN` = (paste token)

### Coverage Reports

After setup, coverage reports will be:

- Uploaded automatically on every push
- Visible as PR comments
- Available at `codecov.io/gh/Northstar-Technologies/timesheet`

### Coverage Targets

| Metric          | Current | Target | Status         |
| --------------- | ------- | ------ | -------------- |
| Overall         | 83%     | 85%    | 🔄 In Progress |
| `app/routes/`   | 80%+    | 85%    | ✅ Good        |
| `app/services/` | 82%     | 80%    | ✅ Good        |
| `app/utils/`    | 60%     | 70%    | 🔄 In Progress |

---

## Local Development

### Running Tests Locally

```bash
# Unit tests only
pytest tests/ --ignore=tests/e2e -v

# With coverage
pytest tests/ --ignore=tests/e2e --cov=app --cov-report=html
open htmlcov/index.html

# E2E tests (requires Docker stack running)
cd docker && docker compose up -d
npx playwright test

# Specific E2E test
npx playwright test tests/e2e/login.spec.js
```

### Running Linters Locally

```bash
# Flake8
flake8 app --max-line-length=120

# Black (check only)
black app --check --line-length=120

# Black (auto-format)
black app --line-length=120

# Bandit security scan
bandit -r app -ll -ii

# Safety dependency check
safety check -r requirements.txt
```

---

## Branch Protection Rules

Recommended branch protection for `main`:

| Setting                             | Value                     |
| ----------------------------------- | ------------------------- |
| Require pull request before merging | ✅                        |
| Require status checks to pass       | ✅                        |
| Required status checks              | `unit-tests`, `e2e-tests` |
| Require branches to be up to date   | ✅                        |
| Require conversation resolution     | ✅                        |

### Setting Up Branch Protection

1. Go to GitHub → Settings → Branches
2. Add rule for `main`
3. Enable settings from table above
4. Save changes

---

## Secrets Required

| Secret          | Purpose                 | Where to Get |
| --------------- | ----------------------- | ------------ |
| `CODECOV_TOKEN` | Upload coverage reports | codecov.io   |

### Optional Secrets (for deployment)

| Secret              | Purpose          |
| ------------------- | ---------------- |
| `AZURE_CREDENTIALS` | Azure deployment |
| `SENTRY_DSN`        | Error monitoring |
| `SLACK_WEBHOOK`     | Notifications    |

---

## Workflow Status Badges

Add these to your README.md:

```markdown
![Tests](https://github.com/Northstar-Technologies/timesheet/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/Northstar-Technologies/timesheet/graph/badge.svg)](https://codecov.io/gh/Northstar-Technologies/timesheet)
```

---

## Troubleshooting

### E2E Tests Failing in CI

**Symptom**: Tests pass locally but fail in CI

**Common causes**:

1. **Timing issues**: CI is slower, increase timeouts
2. **Port conflicts**: Ensure Docker ports are available
3. **Browser differences**: CI uses headless Chromium

**Debug steps**:

```bash
# Download artifacts from failed run
# Check playwright-report/index.html for screenshots
```

### Coverage Not Uploading

**Symptom**: Codecov badge shows no data

**Fixes**:

1. Verify `CODECOV_TOKEN` secret is set
2. Check codecov-action logs in GitHub Actions
3. Ensure `coverage.xml` is generated

### Pre-commit Hooks Slow

**Symptom**: Commits take >30 seconds

**Fixes**:

```bash
# Skip pytest for quick commits
SKIP=pytest-quick git commit -m "quick fix"

# Or disable pytest hook permanently (edit .pre-commit-config.yaml)
# Change: stages: [commit] → stages: [push]
```

---

_Last Updated: January 12, 2026_
