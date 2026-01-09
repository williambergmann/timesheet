"""
Notification Service

Handles sending SMS notifications for timesheet events.
Creates notification records and sends via Twilio.
"""

from datetime import datetime
from flask import current_app
from ..models import Notification, NotificationType, User
from ..extensions import db
from ..utils.sms import send_sms, format_phone_number
from ..utils.email import send_template_email


class NotificationService:
    """
    Service for sending SMS notifications to users.

    Handles:
    - Timesheet approval notifications
    - Needs attention notifications
    - Weekly reminder notifications (scheduled)
    """

    @staticmethod
    def notify_approved(timesheet):
        """
        Send notification when a timesheet is approved.

        Args:
            timesheet: The approved Timesheet object

        Returns:
            Notification: The created notification record
        """
        user = timesheet.user
        if not user:
            current_app.logger.warning(
                f"Cannot notify: timesheet {timesheet.id} has no associated user"
            )
            return None

        # Email notification (REQ-011)
        NotificationService._send_approval_email(timesheet)

        # Check if user has opted in and has a phone number
        if not user.sms_opt_in:
            current_app.logger.info(
                f"SMS skipped for {user.email}: user has not opted in"
            )
            return None

        phone = format_phone_number(user.phone)
        if not phone:
            current_app.logger.info(
                f"SMS skipped for {user.email}: no valid phone number"
            )
            return None

        # Format the message
        week_str = timesheet.week_start.strftime("%b %d, %Y")
        message = f"✅ Your timesheet for week of {week_str} has been approved!"

        # Create notification record
        notification = Notification(
            user_id=user.id,
            timesheet_id=timesheet.id,
            type=NotificationType.APPROVED,
            message=message,
        )
        db.session.add(notification)

        # Send SMS
        result = send_sms(phone, message)

        if result.get("success"):
            notification.sent = True
            notification.sent_at = datetime.utcnow()
            current_app.logger.info(
                f"Approval notification sent to {user.email} ({phone})"
            )
        else:
            notification.sent = False
            notification.error = result.get("error", "Unknown error")
            current_app.logger.error(
                f"Failed to send approval notification to {user.email}: {notification.error}"
            )

        db.session.commit()
        return notification

    @staticmethod
    def notify_needs_attention(timesheet, reason=None):
        """
        Send notification when a timesheet needs attention.

        Args:
            timesheet: The Timesheet object marked as needing attention
            reason: Optional reason for the rejection

        Returns:
            Notification: The created notification record
        """
        user = timesheet.user
        if not user:
            current_app.logger.warning(
                f"Cannot notify: timesheet {timesheet.id} has no associated user"
            )
            return None

        # Email notification (REQ-011)
        NotificationService._send_needs_attention_email(timesheet, reason)

        # Check if user has opted in and has a phone number
        if not user.sms_opt_in:
            current_app.logger.info(
                f"SMS skipped for {user.email}: user has not opted in"
            )
            return None

        phone = format_phone_number(user.phone)
        if not phone:
            current_app.logger.info(
                f"SMS skipped for {user.email}: no valid phone number"
            )
            return None

        # Format the message
        week_str = timesheet.week_start.strftime("%b %d, %Y")
        if reason:
            message = f"⚠️ Your timesheet for week of {week_str} needs attention: {reason}"
        else:
            message = f"⚠️ Your timesheet for week of {week_str} needs attention. Please log in to add the required attachment."

        # Truncate if too long (SMS limit is 160 chars for single segment)
        if len(message) > 160:
            message = message[:157] + "..."

        # Create notification record
        notification = Notification(
            user_id=user.id,
            timesheet_id=timesheet.id,
            type=NotificationType.NEEDS_ATTACHMENT,
            message=message,
        )
        db.session.add(notification)

        # Send SMS
        result = send_sms(phone, message)

        if result.get("success"):
            notification.sent = True
            notification.sent_at = datetime.utcnow()
            current_app.logger.info(
                f"Needs attention notification sent to {user.email} ({phone})"
            )
        else:
            notification.sent = False
            notification.error = result.get("error", "Unknown error")
            current_app.logger.error(
                f"Failed to send needs attention notification to {user.email}: {notification.error}"
            )

        db.session.commit()
        return notification

    @staticmethod
    def send_weekly_reminder(user, week_start):
        """
        Send a weekly reminder to submit timesheet.

        Args:
            user: The User object to remind
            week_start: The date of week start

        Returns:
            Notification: The created notification record
        """
        # Email notification (REQ-011)
        NotificationService._send_reminder_email(user, week_start)

        # Check if user has opted in and has a phone number
        if not user.sms_opt_in:
            return None

        phone = format_phone_number(user.phone)
        if not phone:
            return None

        # Format the message
        week_str = week_start.strftime("%b %d")
        message = f"📋 Reminder: Don't forget to submit your timesheet for week of {week_str}!"

        # Create notification record
        notification = Notification(
            user_id=user.id,
            timesheet_id=None,
            type=NotificationType.REMINDER,
            message=message,
        )
        db.session.add(notification)

        # Send SMS
        result = send_sms(phone, message)

        if result.get("success"):
            notification.sent = True
            notification.sent_at = datetime.utcnow()
        else:
            notification.sent = False
            notification.error = result.get("error", "Unknown error")

        db.session.commit()
        return notification

    @staticmethod
    def notify_unsubmitted(user, week_start):
        """
        Send a reminder for an unsubmitted timesheet from the previous week.

        This is sent starting Monday and every day after until the timesheet
        is submitted or approved. Includes a link to open the app directly.

        Args:
            user: The User object to remind
            week_start: The date of the unsubmitted week (previous week's Sunday)

        Returns:
            Notification: The created notification record, or None if not sent
        """
        # Email notification (REQ-011)
        NotificationService._send_unsubmitted_email(user, week_start)

        # Check if user has opted in and has a phone number
        if not user.sms_opt_in:
            current_app.logger.info(
                f"SMS skipped for {user.email}: user has not opted in"
            )
            return None

        phone = format_phone_number(user.phone)
        if not phone:
            current_app.logger.info(
                f"SMS skipped for {user.email}: no valid phone number"
            )
            return None

        # Get the app URL from config
        app_url = current_app.config.get("APP_URL", "http://localhost/app")

        # Format the message - similar to the Timesheets Bot format
        message = (
            f"⏰ You have not submitted last week's timesheet.\n\n"
            f"Open in Timesheets App: {app_url}"
        )

        # Create notification record
        notification = Notification(
            user_id=user.id,
            timesheet_id=None,
            type=NotificationType.UNSUBMITTED,
            message=message,
        )
        db.session.add(notification)

        # Send SMS
        result = send_sms(phone, message)

        if result.get("success"):
            notification.sent = True
            notification.sent_at = datetime.utcnow()
            current_app.logger.info(
                f"Unsubmitted reminder sent to {user.email} ({phone})"
            )
        else:
            notification.sent = False
            notification.error = result.get("error", "Unknown error")
            current_app.logger.error(
                f"Failed to send unsubmitted reminder to {user.email}: {notification.error}"
            )

        db.session.commit()
        return notification

    @staticmethod
    def notify_admin_new_submission(timesheet):
        """
        Notify admins when a new timesheet is submitted (REQ-011).
        """
        from ..models import UserRole

        admins = User.query.filter_by(role=UserRole.ADMIN).all()
        if not admins:
            current_app.logger.info("Email admin notification skipped: no admins found")
            return None

        week_str = timesheet.week_start.strftime("%b %d, %Y")
        totals = timesheet.calculate_totals()
        field_hours = sum(
            float(e.hours) for e in timesheet.entries if e.hour_type == "Field"
        )
        has_field_hours = field_hours > 0
        has_attachments = timesheet.attachments.count() > 0

        for admin in admins:
            if not admin.email_opt_in:
                continue
            recipients = admin.get_notification_emails()
            if not recipients:
                continue
            send_template_email(
                recipients,
                subject=f"New Timesheet Submitted ({week_str})",
                template_name="admin_new_submission",
                year=datetime.utcnow().year,
                app_url=current_app.config.get("APP_URL", "http://localhost/app"),
                user_name=timesheet.user.display_name if timesheet.user else "Unknown",
                user_email=timesheet.user.email if timesheet.user else "",
                week_start=week_str,
                total_hours=float(totals["total"]),
                field_hours=float(field_hours),
                has_field_hours=has_field_hours,
                traveled=timesheet.traveled,
                has_attachments=has_attachments,
                attachment_count=timesheet.attachments.count(),
            )

        return True

    @staticmethod
    def _send_approval_email(timesheet):
        user = timesheet.user
        if not user or not user.email_opt_in:
            return None

        recipients = user.get_notification_emails()
        if not recipients:
            return None

        week_str = timesheet.week_start.strftime("%b %d, %Y")
        totals = timesheet.calculate_totals()
        approved_by = None
        if timesheet.approver:
            approved_by = timesheet.approver.display_name

        return send_template_email(
            recipients,
            subject=f"Timesheet Approved ({week_str})",
            template_name="approved",
            year=datetime.utcnow().year,
            app_url=current_app.config.get("APP_URL", "http://localhost/app"),
            week_start=week_str,
            total_hours=float(totals["total"]),
            approved_by=approved_by,
        )

    @staticmethod
    def _send_needs_attention_email(timesheet, reason=None):
        user = timesheet.user
        if not user or not user.email_opt_in:
            return None

        recipients = user.get_notification_emails()
        if not recipients:
            return None

        week_str = timesheet.week_start.strftime("%b %d, %Y")

        return send_template_email(
            recipients,
            subject=f"Timesheet Needs Attention ({week_str})",
            template_name="needs_attention",
            year=datetime.utcnow().year,
            app_url=current_app.config.get("APP_URL", "http://localhost/app"),
            week_start=week_str,
            reason=reason,
        )

    @staticmethod
    def _send_reminder_email(user, week_start):
        if not user or not user.email_opt_in:
            return None

        recipients = user.get_notification_emails()
        if not recipients:
            return None

        week_str = week_start.strftime("%b %d, %Y")

        return send_template_email(
            recipients,
            subject=f"Timesheet Reminder ({week_str})",
            template_name="reminder",
            year=datetime.utcnow().year,
            app_url=current_app.config.get("APP_URL", "http://localhost/app"),
            week_start=week_str,
        )

    @staticmethod
    def _send_unsubmitted_email(user, week_start):
        if not user or not user.email_opt_in:
            return None

        recipients = user.get_notification_emails()
        if not recipients:
            return None

        week_str = week_start.strftime("%b %d, %Y")

        return send_template_email(
            recipients,
            subject=f"Timesheet Past Due ({week_str})",
            template_name="unsubmitted",
            year=datetime.utcnow().year,
            app_url=current_app.config.get("APP_URL", "http://localhost/app"),
            week_start=week_str,
        )
