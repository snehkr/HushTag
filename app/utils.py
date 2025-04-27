from functools import wraps
from flask import flash, redirect, url_for, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or not session.get("is_admin", False):
            flash("Admin access required.", "danger")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)

    return decorated_function
