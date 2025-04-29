from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import register_user, authenticate_user, log_activity
from app.utils import login_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = authenticate_user(username, password)

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["is_admin"] = user.get("is_admin", False)
            log_activity(
                user["id"],
                "login",
                f"User logged in",
                request.headers.get("User-Agent"),
                request.remote_addr,
            )
            flash("Login successful!", "success")
            return redirect(url_for("main.dashboard"))
        flash("Invalid username or password", "danger")
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        email = request.form.get("email", "")

        if register_user(username, password, email):
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))
        flash("Username already exists", "danger")
    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    log_activity(
        session["user_id"],
        "logout",
        "User logged out",
        request.headers.get("User-Agent"),
        request.remote_addr,
    )
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))
