from flask import Flask, jsonify
from src.api.rename.routes import rename
from src.api.manage.routes import manage
from flask_cors import CORS
from src.lib.exceptions.exceptions import ServiceError
from src.lib.service_constants import BAD_REQUEST_CODE, INTERNAL_SERVER_ERROR_CODE
import logging

logger = logging.getLogger(__name__)


def register_errors(app):

    @app.errorhandler(ServiceError)
    def handle_service_error(e):
        return jsonify({"error": str(e)}), BAD_REQUEST_CODE

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        return jsonify({"error": str(e)}), INTERNAL_SERVER_ERROR_CODE

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({"error": str(e)}), 405


def create_app():
    app = Flask("media utility")

    app.register_blueprint(rename)
    app.register_blueprint(manage)

    register_errors(app)

    CORS(app)
    return app
