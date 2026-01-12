# Contributing to Northstar Timesheet

Thank you for contributing to the Northstar Timesheet application! This guide will help you get started.

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Northstar-Technologies/timesheet.git
cd timesheet
```

### 2. Start the Development Environment

```bash
# Start all services (nginx, flask, postgres, redis)
cd docker
docker compose up -d --build

# Wait for services to be healthy
docker compose ps
```

The application will be available at `http://localhost`.

### 3. Verify It's Working

```bash
# Check health endpoint
curl http://localhost/health

# View logs
docker compose logs -f web
```

---

## Development Workflow

### Making Changes

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

   - Backend: `app/` directory (Flask)
   - Frontend: `static/js/`, `static/css/`, `templates/`
   - Tests: `tests/` directory

3. **Run pre-commit hooks**

   ```bash
   # Install pre-commit (first time only)
   pip install pre-commit
   pre-commit install

   # Hooks run automatically on commit, or manually:
   pre-commit run --all-files
   ```

4. **Run tests**

   ```bash
   # Unit tests
   pytest tests/ --ignore=tests/e2e -v

   # E2E tests (requires Docker running)
   npx playwright test
   ```

5. **Commit with a descriptive message**
   ```bash
   git commit -m "feat: add holiday awareness warning"
   ```

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix      | Use For                                          |
| ----------- | ------------------------------------------------ |
| `feat:`     | New features                                     |
| `fix:`      | Bug fixes                                        |
| `docs:`     | Documentation only                               |
| `test:`     | Adding/updating tests                            |
| `refactor:` | Code changes that don't add features or fix bugs |
| `style:`    | Formatting, missing semicolons, etc.             |
| `chore:`    | Maintenance tasks                                |

**Examples:**

```
feat: add REQ-022 holiday awareness warning
fix: resolve BUG-006 upload error on NEEDS_UPLOAD status
docs: update CONTRIBUTING.md with deployment steps
test: add PDF export tests for admin routes
```

---

## Running Tests

### Unit Tests (Python)

```bash
# All unit tests
pytest tests/ --ignore=tests/e2e -v

# With coverage
pytest tests/ --ignore=tests/e2e --cov=app --cov-report=html
open htmlcov/index.html

# Specific test file
pytest tests/test_auth.py -v

# Specific test
pytest tests/test_auth.py::test_login_redirect -v
```

### E2E Tests (Playwright)

```bash
# Ensure Docker is running
cd docker && docker compose up -d

# Run all E2E tests
npx playwright test

# Run specific test
npx playwright test tests/e2e/login.spec.js

# Run with visible browser
npx playwright test --headed

# Debug mode
npx playwright test --debug
```

### Pre-commit Checks

```bash
# Run all hooks
pre-commit run --all-files

# Run specific hook
pre-commit run flake8 --all-files
pre-commit run black --all-files
```

---

## Code Style

### Python

- **Formatter**: Black (line length 120)
- **Linter**: Flake8
- **Import sorting**: isort (black profile)

```bash
# Auto-format
black app --line-length=120
isort app --profile=black

# Check only
black app --check
flake8 app --max-line-length=120
```

### JavaScript

- Use ES6+ features
- Prefer `const` over `let`, avoid `var`
- Use template literals for string interpolation
- Document functions with JSDoc comments

### CSS

- Use CSS custom properties (variables) from `static/css/main.css`
- Follow BEM naming convention where applicable
- Dark mode is default; test in both themes

---

## Project Structure

```
timesheet/
├── app/                    # Flask application
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   ├── models.py           # SQLAlchemy models
│   └── config.py           # Configuration
├── static/
│   ├── js/                 # Frontend JavaScript
│   │   └── timesheet/      # Modular timesheet components
│   └── css/                # Stylesheets
├── templates/              # Jinja2 templates
├── tests/
│   ├── e2e/                # Playwright E2E tests
│   └── test_*.py           # Pytest unit tests
├── docker/                 # Docker configuration
├── docs/                   # Documentation
└── migrations/             # Database migrations
```

---

## Database Migrations

### Creating a Migration

```bash
# After modifying models.py
flask db migrate -m "Add new_column to users"

# Review the generated migration in migrations/versions/
# Then apply it
flask db upgrade
```

### Rolling Back

```bash
# Rollback one migration
flask db downgrade

# Rollback to specific revision
flask db downgrade abc123
```

---

## Deployment

### Local Development

```bash
cd docker
docker compose up -d --build
```

### Production

See [docs/SSL-SETUP.md](SSL-SETUP.md) for HTTPS configuration.

```bash
# Production deployment
cd docker
docker compose -f docker-compose.prod.yml up -d --build

# View production logs
docker compose -f docker-compose.prod.yml logs -f
```

---

## Pull Request Process

1. **Ensure all tests pass**

   ```bash
   pytest tests/ --ignore=tests/e2e
   npx playwright test
   ```

2. **Update documentation** if needed

3. **Create PR with description**

   - What does this change?
   - Why is it needed?
   - How was it tested?

4. **Wait for CI checks** to pass (GitHub Actions)

5. **Request review** from a team member

---

## Getting Help

- **Bug reports**: See [docs/BUGS.md](BUGS.md)
- **Feature requests**: Check [docs/REQUIREMENTS.md](REQUIREMENTS.md)
- **Architecture questions**: See [docs/CHECKIN.md](CHECKIN.md)
- **Security concerns**: See [docs/SECURITY.md](SECURITY.md)

---

## Environment Variables

Copy `.env.example` to create your local `.env`:

```bash
cp .env.example docker/.env
```

Key variables for development:

| Variable       | Description            | Default                                              |
| -------------- | ---------------------- | ---------------------------------------------------- |
| `FLASK_ENV`    | Environment mode       | `development`                                        |
| `DATABASE_URL` | PostgreSQL connection  | `postgresql://timesheet:timesheet@db:5432/timesheet` |
| `SECRET_KEY`   | Session encryption key | Auto-generated in dev                                |

See `.env.example` for all available options.

---

_Last Updated: January 12, 2026_
