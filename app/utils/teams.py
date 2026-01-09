"""
Teams Notification Utilities (REQ-012)

Sends proactive Teams notifications using Bot Framework.
"""

import time
from typing import Iterable, Optional

from flask import current_app


BOT_SCOPE = ["https://api.botframework.com/.default"]
_TOKEN_CACHE = {
    "access_token": "",
    "expires_at": 0,
}


def _is_placeholder(value: str) -> bool:
    if not value:
        return True
    lowered = str(value).lower()
    return any(token in lowered for token in ("your-", "example", "placeholder", "xxx"))


def is_teams_configured() -> bool:
    if not current_app.config.get("TEAMS_NOTIFICATIONS_ENABLED", False):
        return False

    required = [
        current_app.config.get("TEAMS_APP_ID"),
        current_app.config.get("TEAMS_APP_PASSWORD"),
    ]

    return all(not _is_placeholder(value) for value in required)


def _get_bot_token() -> str:
    if not is_teams_configured():
        raise RuntimeError("Teams notifications are not configured")

    now = time.time()
    if _TOKEN_CACHE["access_token"] and now < (_TOKEN_CACHE["expires_at"] - 60):
        return _TOKEN_CACHE["access_token"]

    import msal

    tenant_id = current_app.config.get("TEAMS_TENANT_ID", "botframework.com")
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    app = msal.ConfidentialClientApplication(
        current_app.config.get("TEAMS_APP_ID"),
        authority=authority,
        client_credential=current_app.config.get("TEAMS_APP_PASSWORD"),
    )

    result = app.acquire_token_for_client(scopes=BOT_SCOPE)
    token = result.get("access_token")
    if not token:
        raise RuntimeError(
            f"Failed to acquire bot token: {result.get('error_description', 'unknown error')}"
        )

    expires_in = int(result.get("expires_in", 3599))
    _TOKEN_CACHE["access_token"] = token
    _TOKEN_CACHE["expires_at"] = now + expires_in

    return token


def _build_message_payload(text: str, card: Optional[dict], bot_id: str, bot_name: str):
    payload = {
        "type": "message",
        "from": {"id": bot_id},
        "text": text,
    }

    if bot_name:
        payload["from"]["name"] = bot_name

    if card:
        payload["attachments"] = [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card,
            }
        ]

    return payload


def send_teams_message(conversation, text: str, card: Optional[dict] = None) -> bool:
    if not is_teams_configured():
        current_app.logger.info("Teams notification skipped: not configured")
        return False

    token = _get_bot_token()
    service_url = conversation.service_url.rstrip("/")
    url = f"{service_url}/v3/conversations/{conversation.conversation_id}/activities"

    payload = _build_message_payload(
        text=text,
        card=card,
        bot_id=conversation.bot_id,
        bot_name=conversation.bot_name,
    )

    import requests

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )

    if response.status_code not in (200, 201, 202):
        raise RuntimeError(
            f"Teams send failed: {response.status_code} {response.text}"
        )

    return True


def get_conversation_for_user(user):
    from app.models import TeamsConversation
    from app.extensions import db

    if not user or not user.teams_opt_in or not user.teams_account:
        return None

    conversation = TeamsConversation.query.filter_by(user_id=user.id).first()
    if conversation:
        return conversation

    conversation = TeamsConversation.query.filter_by(
        teams_user_principal=user.teams_account
    ).first()
    if conversation and conversation.user_id != user.id:
        conversation.user_id = user.id
        db.session.commit()

    return conversation


def send_card_to_user(user, card: dict, fallback_text: str) -> bool:
    conversation = get_conversation_for_user(user)
    if not conversation:
        current_app.logger.info("Teams notification skipped: no conversation for user")
        return False

    return send_teams_message(conversation, fallback_text, card)


def send_card_to_users(users: Iterable, card: dict, fallback_text: str) -> int:
    sent = 0
    for user in users:
        if not user.teams_opt_in:
            continue
        if not user.teams_account:
            continue
        try:
            if send_card_to_user(user, card, fallback_text):
                sent += 1
        except Exception as exc:
            current_app.logger.error(
                "Teams notification failed for %s: %s", user.email, exc
            )
    return sent


def build_action_open_url(title: str, url: str) -> dict:
    return {
        "type": "Action.OpenUrl",
        "title": title,
        "url": url,
    }


def build_action_submit(title: str, data: dict) -> dict:
    return {
        "type": "Action.Submit",
        "title": title,
        "data": data,
    }


def build_basic_card(title: str, lines: Iterable[str], actions: Optional[list] = None) -> dict:
    body = [
        {
            "type": "TextBlock",
            "text": title,
            "weight": "Bolder",
            "size": "Medium",
            "wrap": True,
        }
    ]

    for line in lines:
        body.append({"type": "TextBlock", "text": line, "wrap": True})

    card = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": body,
        "actions": actions or [],
        "msteams": {"width": "Full"},
    }

    return card


def build_help_card(app_url: str) -> dict:
    actions = [
        build_action_open_url("Open Timesheets", app_url),
        build_action_open_url("Create Timesheet", f"{app_url}#new"),
        build_action_open_url("Settings", f"{app_url}#settings"),
    ]
    lines = [
        "You can reply with:",
        "• help - Show this menu",
        "• status - View your timesheet list",
        "• submit - Open your current timesheet",
    ]
    return build_basic_card("Northstar Timesheets Bot", lines, actions)


def build_timesheet_card(title: str, week_label: str, body_lines: Iterable[str], app_url: str) -> dict:
    lines = [f"Week of {week_label}"] + list(body_lines)
    actions = [build_action_open_url("Open Timesheets", app_url)]
    return build_basic_card(title, lines, actions)


def build_admin_submission_card(timesheet, app_url: str) -> dict:
    totals = timesheet.calculate_totals()
    user_name = timesheet.user.display_name if timesheet.user else "Unknown"
    week_label = timesheet.week_start.strftime("%b %d, %Y")
    field_hours = sum(
        float(entry.hours)
        for entry in timesheet.entries
        if entry.hour_type == "Field"
    )

    body = [
        f"Employee: {user_name}",
        f"Total hours: {float(totals['total'])}",
        f"Field hours: {field_hours}",
    ]

    card = build_basic_card(
        "New Timesheet Submitted",
        [f"Week of {week_label}"] + body,
        actions=[
            build_action_submit(
                "Approve",
                {"action": "approve_timesheet", "timesheet_id": timesheet.id},
            ),
            build_action_submit(
                "Needs Attention",
                {"action": "reject_timesheet", "timesheet_id": timesheet.id},
            ),
            build_action_open_url("Open Admin", f"{app_url}#admin"),
        ],
    )

    card["body"].append(
        {
            "type": "Input.Text",
            "id": "reason",
            "isMultiline": True,
            "placeholder": "Optional reason for needs attention",
        }
    )

    return card
