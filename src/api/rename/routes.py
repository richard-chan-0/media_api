from flask import Blueprint, request
import logging
from src.api.rename.videos import get_jellyfin_video_names, update_video_names
from src.api.rename.comics import get_jellyfin_comic_names, update_comic_names
from src.lib.dataclasses.api import (
    video_request_schema,
    comic_request_schema,
    name_change_request_schema,
)
from src.lib.utilities.app_functions import convert_to_name_change_request

logger = logging.getLogger(__name__)
rename = Blueprint("rename", __name__, url_prefix="/rename")


@rename.route("/")
def hello_world():
    return "Rename Utility API"


@rename.route("/videos", methods=["GET", "POST"])
def rename_videos():
    if request.method == "GET":
        logger.info("Getting new names for videos...")
        video_request = video_request_schema.load(request.get_json())
        names = get_jellyfin_video_names(video_request)
        return convert_to_name_change_request(names)

    try:
        logger.info("Updating video names...")
        name_change_request = name_change_request_schema.load(request.get_json())
        update_video_names(name_change_request)
        return "Successfully renamed videos to Jellyfin format."
    except Exception as e:
        logger.error(f"Error renaming videos: {e}")
        return "Error renaming videos."


@rename.route("/comics", methods=["GET", "POST"])
def rename_comics():
    if request.method == "GET":
        logger.info("Getting new names for comics...")
        comic_request = comic_request_schema.load(request.get_json())
        names = get_jellyfin_comic_names(comic_request)
        return convert_to_name_change_request(names)

    try:
        logger.info("Updating comic names...")
        name_change_request = name_change_request_schema.load(request.get_json())
        update_comic_names(name_change_request)
        return "Successfully renamed comics to Jellyfin format."
    except Exception as e:
        logger.error(f"Error renaming comics: {e}")
        return "Error renaming comics."
