from flask import Flask
from src.api.rename.routes import rename
from src.api.manage.routes import manage


def create_app():
    app = Flask("media utility")

    app.register_blueprint(rename)
    app.register_blueprint(manage)

    return app
