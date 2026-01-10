# Email Notification Service (REQ-011)

> **Status:** ✅ IMPLEMENTED (January 2026)
> **Contact:** Development Team

## Overview

The Email Notification Service provides a reliable way to notify users and administrators about timesheet events. It works alongside the SMS and Teams notification systems to ensure users receive timely updates according to their preferences.

## Features

- **SMTP Integration**: Sends emails via standard SMTP servers (Gmail, SendGrid, Exchange, etc.).
- **Template System**: Uses Jinja2 templates for consistent, professional branding.
- **Support for Multiple Events**:
  - `Timesheet Approved` (to User)
  - `Timesheet Needs Attention` (to User)
  - `Weekly Reminder` (to User)
  - `Unsubmitted Timesheet` (to User - Past Due)
  - `New Submission` (to Admin)
- **User Preferences**: Respects `email_opt_in` setting on the User profile.
- **Dev Mode**: Logs emails to console when SMTP is not configured, preventing accidental spam during development.

## Configuration

The service is configured via environment variables in `.env` (or Azure App Settings).

| Variable          | Description                  | Default                 |
| ----------------- | ---------------------------- | ----------------------- |
| `SMTP_HOST`       | Hostname of the SMTP server  | `""` (Disabled)         |
| `SMTP_PORT`       | Port number                  | `587`                   |
| `SMTP_USER`       | Username for authentication  | `""`                    |
| `SMTP_PASSWORD`   | Password for authentication  | `""`                    |
| `SMTP_FROM_EMAIL` | Sender email address         | `""`                    |
| `SMTP_FROM_NAME`  | Sender display name          | `"Northstar Timesheet"` |
| `SMTP_USE_TLS`    | Enable TLS encryption        | `true`                  |
| `SMTP_USE_SSL`    | Enable SSL encryption        | `false`                 |
| `APP_URL`         | Base URL for links in emails | `http://localhost/app`  |

### Example: Gmail SMTP

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password  # Use App Password, not account password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=Northstar Timesheet
SMTP_USE_TLS=true
```

> ⚠️ **Gmail Note**: You must use an [App Password](https://support.google.com/accounts/answer/185833) if 2FA is enabled.

### Example: SendGrid

```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.your-api-key
SMTP_FROM_EMAIL=noreply@yourdomain.com
SMTP_FROM_NAME=Northstar Timesheet
SMTP_USE_TLS=true
```

### Example: Microsoft 365 / Exchange Online

```bash
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=your-email@yourdomain.com
SMTP_PASSWORD=your-password
SMTP_FROM_EMAIL=your-email@yourdomain.com
SMTP_FROM_NAME=Northstar Timesheet
SMTP_USE_TLS=true
```

### User Preferences

Users can opt-out of emails via their profile settings. The system checks `User.email_opt_in` before sending.

- Admin notifications for new submissions are sent to all users with `role='ADMIN'` who have `email_opt_in=True`.

## Templates

Email templates are located in `templates/email/`.

- `base.html`: Main layout with header, footer, and styles.
- `approved.html`: Approval confirmation.
- `needs_attention.html`: Rejection details and reason.
- `reminder.html`: Gentle weekly reminder.
- `unsubmitted.html`: Urgent past-due reminder.
- `admin_new_submission.html`: Summary for admins.

To edit styles, modify the `<style>` block in `base.html`. The CSS is inlined for maximum client compatibility.

## Usage

The service is integrated into the `NotificationService` class.

```python
from app.services.notification import NotificationService

# Send approval email (and SMS/Teams)
NotificationService.notify_approved(timesheet)

# Send rejection email
NotificationService.notify_needs_attention(timesheet, reason="Missing receipt")

# Send reminders
NotificationService.send_weekly_reminder(user, week_start_date)
```

## Testing

In development, if `SMTP_HOST` is not set, emails are logged to the standard output:

```text
[DEV EMAIL] To=user@example.com Subject=Timesheet Approved (Jan 05, 2026)
```

Unit tests cover template rendering, header construction, and valid/invalid configuration handling.
Run tests with: `pytest tests/test_email.py`

## Troubleshooting

| Problem                        | Solution                                                   |
| ------------------------------ | ---------------------------------------------------------- |
| Emails not sending             | Check `SMTP_HOST` is set and not a placeholder value       |
| Authentication failed          | Verify `SMTP_USER` and `SMTP_PASSWORD` are correct         |
| Connection timeout             | Ensure firewall allows outbound connections on `SMTP_PORT` |
| Gmail "Less secure apps" error | Use an App Password instead of your account password       |
| Emails going to spam           | Configure SPF/DKIM records for your sending domain         |
| Template not found             | Verify template exists in `templates/email/` directory     |

### Debug Mode

To see detailed SMTP communication, set the log level to DEBUG:

```python
import logging
logging.getLogger('app').setLevel(logging.DEBUG)
```

## Security Notes

- **Never commit credentials**: Store `SMTP_PASSWORD` in environment variables or Azure Key Vault.
- **Use TLS/SSL**: Always enable `SMTP_USE_TLS=true` for secure connections.
- **App Passwords**: For Gmail and other providers with 2FA, use app-specific passwords.
- **Rate Limiting**: The service does not implement rate limiting—configure this at the SMTP provider level if needed.
- **Unsubscribe**: Users can disable emails via their profile settings (`email_opt_in`).
