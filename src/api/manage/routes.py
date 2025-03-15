from flask import Blueprint, request
import logging
from src.api.manage.comics import run_create_volumes

logger = logging.getLogger(__name__)
manage = Blueprint("manage", __name__, url_prefix="/manage")


@manage.route("/volumes", methods=["POST"])
def create_volumes_from_chapters():
    return run_create_volumes(request)
