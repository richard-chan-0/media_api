from flask import Blueprint, request, jsonify
import logging
from src.lib.utilities.app_functions import get_files_from_request
from src.lib.utilities.name_functions import create_jellyfin_comic_name
from src.lib.service_constants import (
    IMAGES_IN,
    IMAGES_OUT,
    INTERNAL_SERVER_ERROR_CODE,
    BAD_REQUEST_CODE,
)
from src.lib.dataclasses.app import ServiceArguments
from src.services.manage_media.rezip_chapters_to_vol import rezip_chapters_to_vol
from src.lib.exceptions.exceptions import ServiceError

logger = logging.getLogger(__name__)
manage = Blueprint("manage", __name__, url_prefix="/manage")


@manage.route("/")
def hello_world():
    return "Manage Media Utility API"


@manage.route("/rezip")
def zip_chapters_to_vol():
    try:
        form = request.form
        volume_name = create_jellyfin_comic_name(
            issue=form["issue number"], story_name=form["story title"]
        )
        args = ServiceArguments(
            **{
                "directory_in": IMAGES_IN,
                "directory_out": IMAGES_OUT,
                "volume": volume_name,
            }
        )

        get_files_from_request(request, "files")
        rezip_chapters_to_vol(args)
        return f"files zipped into {volume_name}"
    except ServiceError as e:
        logger.error(e)
        return jsonify({"error": str(e)}), BAD_REQUEST_CODE
    except Exception as e:
        logger.error(e)
        return jsonify({"error": str(e)}), INTERNAL_SERVER_ERROR_CODE
