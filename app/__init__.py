from flask import Flask
from flask_login import LoginManager, current_user
from .db import init_db

# login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object("config")

    # Initialize extensions
    # login_manager.init_app(app)
    # login_manager.login_view = "auth.login"

    # Initialize database
    init_db(app)

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.api import api_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    return app
