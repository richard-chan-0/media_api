from flask import Flask
from src.api.rename.routes import rename
from src.api.manage.routes import manage
from flask_cors import CORS


def create_app():
    app = Flask("media utility")

    app.register_blueprint(rename)
    app.register_blueprint(manage)

    CORS(app)
    return app
