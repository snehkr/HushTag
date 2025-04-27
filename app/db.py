import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask import g
import os
from config import Config


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(Config.DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Create tables if they don't exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                original_name TEXT NOT NULL,
                watermarked_name TEXT NOT NULL,
                watermark TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_type TEXT NOT NULL,
                description TEXT,
                ip_address TEXT,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """
        )

        # Create admin user if not exists
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                ("admin", generate_password_hash("admin"), True),
            )

        db.commit()


def register_user(username, password, email=None):
    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password, email),
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def authenticate_user(username, password):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    if user and check_password_hash(user["password"], password):
        return dict(user)
    return None


def insert_file(original_name, user_id, watermark, watermarked_name):
    db = get_db()
    db.execute(
        "INSERT INTO files (user_id, original_name, watermarked_name, watermark) VALUES (?, ?, ?, ?)",
        (user_id, original_name, watermarked_name, watermark),
    )
    db.commit()


def check_leak(watermark):
    db = get_db()
    file = db.execute(
        "SELECT user_id FROM files WHERE watermark = ?", (watermark,)
    ).fetchone()

    if file:
        user = db.execute(
            "SELECT username, email FROM users WHERE id = ?", (file["user_id"],)
        ).fetchone()
        return [user["username"], user["email"]] if user else None
    return None


def get_user_files(user_id):
    db = get_db()
    return db.execute(
        "SELECT id, original_name, watermarked_name, uploaded_at FROM files WHERE user_id = ? ORDER BY uploaded_at DESC",
        (user_id,),
    ).fetchall()


def log_activity(user_id, activity_type, description, ip_address=None, user_agent=None):
    db = get_db()
    db.execute(
        "INSERT INTO activity_logs (user_id, activity_type, description, ip_address, user_agent) VALUES (?, ?, ?, ?, ?)",
        (user_id, activity_type, description, ip_address, user_agent),
    )
    db.commit()


def get_activity_logs(limit=100):
    db = get_db()
    return db.execute(
        """SELECT a.*, u.username 
           FROM activity_logs a 
           LEFT JOIN users u ON a.user_id = u.id 
           ORDER BY a.created_at DESC 
           LIMIT ?""",
        (limit,),
    ).fetchall()


def get_all_users():
    db = get_db()
    return db.execute(
        "SELECT id, username, email, is_admin, created_at FROM users ORDER BY created_at DESC"
    ).fetchall()
