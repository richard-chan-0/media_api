from flask import Blueprint, request, jsonify
import logging
from src.api.rename.videos import get_jellyfin_video_names, update_video_names
from src.api.rename.comics import get_jellyfin_comic_names, update_comic_names
from src.lib.dataclasses.api import (
    video_request_schema,
    comic_request_schema,
    name_change_request_schema,
)
from src.lib.utilities.app_functions import (
    convert_to_name_change_request,
    check_request_schema,
)
from src.lib.exceptions.exceptions import ServiceError
from src.lib.service_constants import BAD_REQUEST_CODE, INTERNAL_SERVER_ERROR_CODE

logger = logging.getLogger(__name__)
rename = Blueprint("rename", __name__, url_prefix="/rename")

function_map = {
    "videos": (video_request_schema, get_jellyfin_video_names, update_video_names),
    "comics": (comic_request_schema, get_jellyfin_comic_names, update_comic_names),
}


def rename_media(media_type):
    try:
        request_schema, get_name, update_name = function_map.get(media_type)
        if request.method == "GET":
            logger.info(f"Getting new names for {media_type}...")
            media_request = check_request_schema(request_schema, request)
            names = get_name(media_request)
            return jsonify(convert_to_name_change_request(names))

        logger.info(f"Updating {media_type} names...")
        name_change_request = check_request_schema(name_change_request_schema, request)
        update_name(name_change_request)
        return f"Successfully renamed {media_type} to Jellyfin format."
    except ServiceError as e:
        return str(e), BAD_REQUEST_CODE
    except Exception as e:
        logger.error(f"Error renaming {media_type}: {e}")
        return f"Error renaming {media_type}.", INTERNAL_SERVER_ERROR_CODE


@rename.route("/")
def hello_world():
    return "Rename Utility API"


@rename.route("/videos", methods=["GET", "POST"])
def rename_videos():
    return rename_media("videos")


@rename.route("/comics", methods=["GET", "POST"])
def rename_comics():
    return rename_media("comics")
