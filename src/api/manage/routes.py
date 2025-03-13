from flask import Blueprint, request
import logging
from src.lib.utilities.app_functions import run_api_function
from src.api.manage.comics import rezip_chapters_to_volume

logger = logging.getLogger(__name__)
manage = Blueprint("manage", __name__, url_prefix="/manage")


@manage.route("/rezip")
def zip_chapters_to_vol():
    return run_api_function(rezip_chapters_to_volume, request)
