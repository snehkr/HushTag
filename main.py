import os
from flask import Flask
from app import create_app


app = create_app()
app.secret_key = "5neh_5hrut1_r1nk1"


if __name__ == "__main__":
    host = app.config.get("HOST", "0.0.0.0")
    port = app.config.get("PORT", 5000)
    debug = app.config.get("DEBUG", True)

    app.run(host=host, port=port, debug=debug)
