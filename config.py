import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "5neh_5hrut1_r1nk1"
    DATABASE = os.path.join(BASE_DIR, "db", "husktag.db")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf", "docx"}
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
