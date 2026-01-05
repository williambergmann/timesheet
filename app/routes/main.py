"""
Main Routes

Landing page and static content routes.
"""

from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """
    Main application page.

    Renders the timesheet application. Redirects to login if not authenticated.
    """
    if "user" not in session:
        return redirect(url_for("auth.login"))

    return render_template("index.html", user=session["user"])


@main_bp.route("/health")
def health():
    """Health check endpoint for Docker/load balancers."""
    return {"status": "healthy"}, 200
