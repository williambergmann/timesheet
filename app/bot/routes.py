"""
Teams Bot Routes (REQ-012)
"""

from datetime import datetime
from flask import Blueprint, request, jsonify, current_app

from ..extensions import csrf, db
from ..models import TeamsConversation, User, Timesheet, TimesheetStatus, Note
from ..services.notification import NotificationService
from ..utils.pay_periods import get_confirmed_pay_period
from ..utils.teams import (
    build_help_card,
    build_timesheet_card,
    send_teams_message,
    is_teams_configured,
)

bot_bp = Blueprint("bot", __name__)


def _extract_user_principal(activity):
    from_user = activity.get("from", {})
    principal = from_user.get("userPrincipalName") or from_user.get("email")
    if principal:
        return principal.strip().lower()
    return None


def _resolve_user(activity, principal):
    if principal:
        user = User.query.filter_by(teams_account=principal).first()
        if not user:
            user = User.query.filter_by(email=principal).first()
        return user
    return None


def _upsert_conversation(activity):
    service_url = activity.get("serviceUrl")
    conversation_id = activity.get("conversation", {}).get("id")
    if not service_url or not conversation_id:
        return None

    from_user = activity.get("from", {})
    recipient = activity.get("recipient", {})
    channel_data = activity.get("channelData", {})

    teams_user_id = from_user.get("aadObjectId") or from_user.get("id")
    teams_user_name = from_user.get("name")
    teams_user_principal = _extract_user_principal(activity)
    tenant_id = (channel_data.get("tenant") or {}).get("id")

    user = _resolve_user(activity, teams_user_principal)

    conversation = None
    if teams_user_id:
        conversation = TeamsConversation.query.filter_by(
            teams_user_id=teams_user_id
        ).first()
    if not conversation and user:
        conversation = TeamsConversation.query.filter_by(user_id=user.id).first()

    if not conversation:
        conversation = TeamsConversation(
            user_id=user.id if user else None,
            conversation_id=conversation_id,
            service_url=service_url,
            channel_id=activity.get("channelId", "msteams"),
            bot_id=recipient.get("id") or current_app.config.get("TEAMS_APP_ID", ""),
            bot_name=recipient.get("name"),
            tenant_id=tenant_id,
            teams_user_id=teams_user_id,
            teams_user_name=teams_user_name,
            teams_user_principal=teams_user_principal,
            last_activity=datetime.utcnow(),
        )
        db.session.add(conversation)
    else:
        conversation.user_id = user.id if user else conversation.user_id
        conversation.conversation_id = conversation_id
        conversation.service_url = service_url
        conversation.channel_id = activity.get("channelId", "msteams")
        conversation.bot_id = recipient.get("id") or conversation.bot_id
        conversation.bot_name = recipient.get("name") or conversation.bot_name
        conversation.tenant_id = tenant_id or conversation.tenant_id
        conversation.teams_user_id = teams_user_id or conversation.teams_user_id
        conversation.teams_user_name = teams_user_name or conversation.teams_user_name
        conversation.teams_user_principal = (
            teams_user_principal or conversation.teams_user_principal
        )
        conversation.last_activity = datetime.utcnow()

    db.session.commit()
    return conversation


def _resolve_conversation_user(conversation):
    if conversation.user:
        return conversation.user

    if conversation.teams_user_principal:
        user = User.query.filter_by(
            teams_account=conversation.teams_user_principal
        ).first()
        if not user:
            user = User.query.filter_by(email=conversation.teams_user_principal).first()
        if user:
            conversation.user_id = user.id
            db.session.commit()
            return user

    return None


def _send_reply(conversation, text, card=None):
    if not is_teams_configured():
        current_app.logger.info("Bot reply skipped: Teams not configured")
        return

    try:
        send_teams_message(conversation, text, card)
    except Exception as exc:
        current_app.logger.error("Bot reply failed: %s", exc)


def _handle_card_action(activity, conversation):
    value = activity.get("value") or {}
    action = value.get("action")
    if not action:
        return False

    if not conversation:
        return True

    try:
        user = _resolve_conversation_user(conversation)
        if not user:
            _send_reply(conversation, "Unable to match your Teams account to a user.")
            return True

        timesheet_id = value.get("timesheet_id")
        if not timesheet_id:
            _send_reply(conversation, "Missing timesheet reference.")
            return True

        timesheet = Timesheet.query.filter_by(id=timesheet_id).first()
        if not timesheet:
            _send_reply(conversation, "Timesheet not found.")
            return True

        if not user.can_approve(timesheet.user):
            _send_reply(conversation, "You are not authorized to approve this timesheet.")
            return True

        if get_confirmed_pay_period(timesheet.week_start):
            _send_reply(conversation, "Pay period is locked for this timesheet.")
            return True

        if action == "approve_timesheet":
            if timesheet.status not in [
                TimesheetStatus.SUBMITTED,
                TimesheetStatus.NEEDS_APPROVAL,
            ]:
                _send_reply(conversation, "Timesheet cannot be approved from this status.")
                return True

            timesheet.status = TimesheetStatus.APPROVED
            timesheet.approved_at = datetime.utcnow()
            timesheet.approved_by = user.id
            db.session.commit()
            NotificationService.notify_approved(timesheet)
            _send_reply(conversation, "Timesheet approved.")
            return True

        if action == "reject_timesheet":
            if timesheet.status != TimesheetStatus.SUBMITTED:
                _send_reply(conversation, "Only submitted timesheets can be rejected.")
                return True

            timesheet.status = TimesheetStatus.NEEDS_APPROVAL
            reason = (value.get("reason") or "").strip()
            if reason:
                timesheet.admin_notes = reason
                note = Note(
                    timesheet_id=timesheet.id,
                    author_id=user.id,
                    content=f"Needs approval: {reason}",
                )
                db.session.add(note)

            db.session.commit()
            NotificationService.notify_needs_attention(timesheet, reason)
            _send_reply(conversation, "Timesheet marked as needs attention.")
            return True
    except Exception as exc:
        current_app.logger.error("Bot action error: %s", exc)
        _send_reply(conversation, "Something went wrong processing that action.")
        return True

    return False


@bot_bp.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}


@bot_bp.route("/messages", methods=["POST"])
@csrf.exempt
def messages():
    activity = request.get_json(silent=True) or {}
    activity_type = activity.get("type")

    conversation = _upsert_conversation(activity)

    if activity_type == "message":
        if _handle_card_action(activity, conversation):
            return jsonify({"status": "ok"})

        text = (activity.get("text") or "").strip().lower()
        app_url = current_app.config.get("APP_URL", "http://localhost/app")

        if text in ("help", "hi", "hello"):
            card = build_help_card(app_url)
            _send_reply(conversation, "Here are some options:", card)
        elif text in ("submit", "submit timesheet", "status"):
            card = build_timesheet_card(
                "Timesheet Quick Link",
                datetime.utcnow().strftime("%b %d, %Y"),
                ["Open the app to view or submit your timesheet."],
                app_url,
            )
            _send_reply(conversation, "Open Timesheets:", card)
        else:
            _send_reply(conversation, "Type 'help' to see what I can do.")

    if activity_type == "conversationUpdate":
        members_added = activity.get("membersAdded", [])
        bot_id = (activity.get("recipient") or {}).get("id")
        if bot_id and any(member.get("id") == bot_id for member in members_added):
            app_url = current_app.config.get("APP_URL", "http://localhost/app")
            card = build_help_card(app_url)
            _send_reply(conversation, "Thanks for connecting!", card)

    return jsonify({"status": "ok"})
