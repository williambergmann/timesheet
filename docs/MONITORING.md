# Monitoring & Error Tracking

This guide covers setting up error monitoring and application observability for the Northstar Timesheet application.

---

## Sentry Error Monitoring

[Sentry](https://sentry.io) provides real-time error tracking and performance monitoring.

### Features

- **Error Tracking**: Capture unhandled exceptions with full stack traces
- **Request Context**: See which user, endpoint, and request data triggered errors
- **Performance Monitoring**: Track slow database queries and API response times
- **Alerts**: Get notified via email, Slack, or PagerDuty when errors occur
- **Release Tracking**: Associate errors with specific deployments

---

## Setup

### Step 1: Create Sentry Account & Project

1. Go to [sentry.io](https://sentry.io) and sign up (free tier: 5K errors/month)
2. Create a new project:
   - Platform: **Flask**
   - Project name: `northstar-timesheet`
3. Copy the **DSN** from the project settings

### Step 2: Configure Environment Variables

Add to your `.env` file:

```bash
# Sentry Error Monitoring
SENTRY_DSN=https://your-key@sentry.io/your-project-id
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1
```

| Variable                    | Description                            | Example                                    |
| --------------------------- | -------------------------------------- | ------------------------------------------ |
| `SENTRY_DSN`                | Project Data Source Name (from Sentry) | `https://abc123@o123.ingest.sentry.io/456` |
| `SENTRY_ENVIRONMENT`        | Environment name in Sentry dashboard   | `development`, `staging`, `production`     |
| `SENTRY_TRACES_SAMPLE_RATE` | % of requests to trace (0.0-1.0)       | `0.1` (10% in production)                  |

### Step 3: Restart Application

```bash
# Docker
docker compose -f docker/docker-compose.prod.yml down
docker compose -f docker/docker-compose.prod.yml up -d

# Local development
flask run
```

You should see in the logs:

```
Sentry initialized for environment: production
```

### Step 4: Verify Integration

Trigger a test error to confirm Sentry is working:

```bash
# Create a test error endpoint (remove after testing)
curl -X POST http://localhost/api/test-sentry-error
```

Or add a temporary test route:

```python
# In app/routes/main.py (REMOVE AFTER TESTING)
@main_bp.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0
```

Check the Sentry dashboard — you should see the error within 30 seconds.

---

## Configuration Reference

### Sample Rates

| Environment | `SENTRY_TRACES_SAMPLE_RATE` | Rationale                                    |
| ----------- | --------------------------- | -------------------------------------------- |
| Development | `1.0`                       | Capture everything for debugging             |
| Staging     | `0.5`                       | Balance coverage and quota                   |
| Production  | `0.1` - `0.2`               | Control costs, sample representative traffic |

### Integrations Enabled

The Sentry SDK is configured with these integrations:

| Integration             | Purpose                                   |
| ----------------------- | ----------------------------------------- |
| `FlaskIntegration`      | Capture Flask request context, route info |
| `SqlalchemyIntegration` | Track database query performance          |

### Privacy Settings

```python
# Current configuration in app/__init__.py
send_default_pii=False,  # Don't send user emails/IPs automatically
request_bodies="medium", # Capture request bodies up to 10KB
```

To capture user info with errors, you can add:

```python
# In your auth callback or login route
import sentry_sdk
sentry_sdk.set_user({"id": user.id, "email": user.email})
```

---

## Alerting

### Recommended Alert Rules

Set up these alerts in Sentry (Project Settings → Alerts):

| Alert             | Condition              | Action        |
| ----------------- | ---------------------- | ------------- |
| High Error Volume | >10 errors in 1 hour   | Email + Slack |
| First Seen Error  | New error type         | Email         |
| P0 Errors         | 500 errors on `/api/*` | PagerDuty     |
| Slow Transactions | P95 latency > 2s       | Email         |

### Slack Integration

1. Go to Sentry → Settings → Integrations → Slack
2. Connect your Slack workspace
3. Create alerts that post to `#northstar-alerts`

---

## Performance Monitoring

Sentry tracks these performance metrics automatically:

- **Transaction Duration**: Time from request start to response
- **Database Queries**: Count and duration of SQL queries
- **HTTP Spans**: Outbound API calls (Twilio, Azure, etc.)

### Viewing Performance Data

1. Go to Sentry dashboard → **Performance**
2. Filter by `environment:production`
3. See:
   - Slowest endpoints
   - Most called endpoints
   - Apdex score (user satisfaction)

### Custom Spans

For detailed tracing of specific operations:

```python
import sentry_sdk

with sentry_sdk.start_span(op="pdf.generate", description="Generate timesheet PDF"):
    # Your PDF generation code
    pdf_buffer = generate_pdf(timesheet)
```

---

## Troubleshooting

### Sentry Not Capturing Errors

**Check 1: DSN is set**

```bash
grep SENTRY_DSN .env
# Should show your DSN, not empty
```

**Check 2: Verify initialization**

```bash
docker logs timesheet-web-1 2>&1 | grep -i sentry
# Should show: "Sentry initialized for environment: ..."
```

**Check 3: Test error capture**

```python
import sentry_sdk
sentry_sdk.capture_message("Test message from Northstar Timesheet")
```

### High Error Volume / Quota Issues

If hitting Sentry's free tier limits:

1. Reduce `SENTRY_TRACES_SAMPLE_RATE` to `0.05` (5%)
2. Add error filtering in `app/__init__.py`:

   ```python
   def before_send(event, hint):
       # Ignore specific errors
       if 'HTTPException' in str(hint.get('exc_info', '')):
           return None
       return event

   sentry_sdk.init(
       dsn=dsn,
       before_send=before_send,
       # ... other options
   )
   ```

### Performance Impact

Sentry adds minimal overhead:

- ~1-2ms per request for event serialization
- Events are sent asynchronously (non-blocking)
- Batch sending reduces network calls

---

## Other Observability

### Existing: Structured Logging (REQ-036)

The application already has structured logging via `app/utils/observability.py`:

- Request IDs in all log entries
- JSON-formatted logs for parsing
- Performance timing on API endpoints

### Existing: Health Check (REQ-043)

Health endpoint at `/health` returns:

- Database connectivity status
- Redis connectivity status
- Application version

### Future: Metrics Export

For Prometheus/Grafana integration, consider adding:

```bash
pip install prometheus-flask-exporter
```

---

## Cost Considerations

### Sentry Pricing (as of 2026)

| Tier      | Errors/Month | Price     |
| --------- | ------------ | --------- |
| Developer | 5,000        | Free      |
| Team      | 50,000       | $26/month |
| Business  | 100,000+     | Custom    |

### Reducing Costs

1. **Lower sample rate**: Set `SENTRY_TRACES_SAMPLE_RATE=0.05`
2. **Filter noisy errors**: Ignore expected exceptions (404s, validation errors)
3. **Use rate limits**: Sentry has built-in rate limiting per project

---

_Last Updated: January 12, 2026_
