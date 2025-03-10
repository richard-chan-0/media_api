from flask import Blueprint, request, jsonify
import logging

logger = logging.getLogger(__name__)
manage = Blueprint("manage", __name__, url_prefix="/manage")


@manage.route("/")
def hello_world():
    return "Manage Media Utility API"
