from flask import Blueprint, request
import logging
from src.api.rename.videos import get_jellyfin_video_names, update_video_names
from src.api.rename.comics import get_jellyfin_comic_names, update_comic_names

logger = logging.getLogger(__name__)
rename = Blueprint("rename", __name__, url_prefix="/rename")


@rename.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@rename.route("/videos", methods=["GET", "POST"])
def rename_videos():
    if request.method == "GET":
        logger.info("Getting new names for videos...")
        return get_jellyfin_video_names(request.get_json())

    try:
        logger.info("Updating video names...")
        update_video_names(request.get_json())
        return "Successfully renamed videos to Jellyfin format."
    except Exception as e:
        logger.error(f"Error renaming videos: {e}")
        return "Error renaming videos."


@rename.route("/comics", methods=["GET", "POST"])
def rename_comics():
    if request.method == "GET":
        logger.info("Getting new names for comics...")
        return get_jellyfin_comic_names(request.get_json())

    try:
        logger.info("Updating comic names...")
        update_comic_names(request.get_json())
        return "Successfully renamed comics to Jellyfin format."
    except Exception as e:
        logger.error(f"Error renaming comics: {e}")
        return "Error renaming comics."
