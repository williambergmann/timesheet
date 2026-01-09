"""
Email utility helpers (REQ-011).
"""

import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app, render_template


def _normalize_recipients(to_email):
    if isinstance(to_email, str):
        recipients = [to_email]
    else:
        recipients = list(to_email or [])
    return [email.strip() for email in recipients if email and "@" in email]


def is_smtp_configured():
    smtp_host = current_app.config.get("SMTP_HOST", "")
    smtp_port = current_app.config.get("SMTP_PORT", 0)

    if not smtp_host or not smtp_port:
        return False

    placeholders = ("your-", "example", "placeholder", "xxx")
    return not any(token in str(smtp_host).lower() for token in placeholders)


def send_email(to_email, subject, html_content, text_content=None):
    recipients = _normalize_recipients(to_email)
    if not recipients:
        return {"success": False, "error": "No valid email recipients"}

    if not subject or not subject.strip():
        return {"success": False, "error": "Subject cannot be empty"}

    if not html_content or not html_content.strip():
        return {"success": False, "error": "Email content cannot be empty"}

    if not is_smtp_configured():
        current_app.logger.info(
            "[DEV EMAIL] To=%s Subject=%s", ", ".join(recipients), subject
        )
        return {
            "success": True,
            "dev_mode": True,
            "message": "Email logged (SMTP not configured)",
        }

    smtp_host = current_app.config.get("SMTP_HOST", "")
    smtp_port = int(current_app.config.get("SMTP_PORT", 587))
    smtp_user = current_app.config.get("SMTP_USER", "")
    smtp_password = current_app.config.get("SMTP_PASSWORD", "")
    smtp_from = current_app.config.get("SMTP_FROM_EMAIL", "") or smtp_user
    smtp_from_name = current_app.config.get(
        "SMTP_FROM_NAME", "Northstar Timesheet"
    )
    use_tls = current_app.config.get("SMTP_USE_TLS", True)
    use_ssl = current_app.config.get("SMTP_USE_SSL", False)

    if not text_content:
        text_content = re.sub(r"<[^>]+>", " ", html_content)
        text_content = re.sub(r"\s+", " ", text_content).strip()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{smtp_from_name} <{smtp_from}>"
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(text_content, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    try:
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port)
            if use_tls:
                server.starttls()

        if smtp_user and smtp_password:
            server.login(smtp_user, smtp_password)

        server.sendmail(smtp_from, recipients, msg.as_string())
        server.quit()

        current_app.logger.info(
            "Email sent: To=%s Subject=%s", ", ".join(recipients), subject
        )
        return {"success": True, "recipients": recipients}

    except smtplib.SMTPException as exc:
        current_app.logger.error("SMTP error: %s", exc)
        return {"success": False, "error": str(exc)}

    except Exception as exc:
        current_app.logger.error("Email send error: %s", exc)
        return {"success": False, "error": str(exc)}


def send_template_email(to_email, subject, template_name, **template_context):
    try:
        html_content = render_template(
            f"email/{template_name}.html", **template_context
        )
        try:
            text_content = render_template(
                f"email/{template_name}.txt", **template_context
            )
        except Exception:
            text_content = None

        return send_email(to_email, subject, html_content, text_content)
    except Exception as exc:
        current_app.logger.error("Email template error: %s", exc)
        return {"success": False, "error": str(exc)}
