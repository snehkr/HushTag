from flask import Blueprint, render_template, session, flash, redirect, url_for
from app.db import get_activity_logs, get_all_users
from app.utils import admin_required, login_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/logs")
@login_required
@admin_required
def view_logs():
    logs = get_activity_logs()
    return render_template("admin_logs.html", logs=logs)


@admin_bp.route("/users")
@login_required
@admin_required
def view_users():
    users = get_all_users()
    return render_template("admin_users.html", users=users)
