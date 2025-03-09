from flask import Flask
from src.api.rename.routes import rename


def create_app():
    app = Flask("media utility")

    app.register_blueprint(rename)

    return app
