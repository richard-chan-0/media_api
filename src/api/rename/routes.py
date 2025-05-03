from flask import Blueprint, request, jsonify
import logging
from src.api.rename.videos import (
    get_jellyfin_video_names_from_files,
)
from src.api.rename.comics import get_jellyfin_comic_names_from_files
from src.lib.dataclasses.api import (
    name_change_request_schema,
)
from src.lib.utilities.app_functions import (
    convert_to_name_change_request,
    check_request_schema,
)
from src.lib.utilities.os_functions import rename_list_files, get_files, transfer_files
from src.lib.service_constants import INPUT_DIRECTORY, OUTPUT_DIRECTORY

logger = logging.getLogger(__name__)
rename = Blueprint("rename", __name__, url_prefix="/rename")

function_map = {
    "videos": get_jellyfin_video_names_from_files,
    "comics": get_jellyfin_comic_names_from_files,
}


def upload_media(media_type: str):
    logger.info(f"uploading {media_type}")
    names = function_map[media_type](request)
    return jsonify(convert_to_name_change_request(names)), 200


@rename.route("/process", methods=["POST"])
def rename_files():
    logger.info("renaming files")
    name_change_request = check_request_schema(name_change_request_schema, request)
    logger.info(name_change_request)
    rename_list_files(name_change_request)
    return "Successfully renamed files.", 200


@rename.route("/videos", methods=["POST"])
def upload_videos():
    return upload_media("videos")


@rename.route("/comics", methods=["POST"])
def upload_comics():
    return upload_media("comics")


@rename.route("/read", methods=["GET"])
def get_files_to_be_renamed():
    files = get_files(INPUT_DIRECTORY)
    return jsonify(files), 200


@rename.route("/push", methods=["GET"])
def push_files():
    logger.info("pushing files to shared folder")
    transfer_files(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    return "Successfully pushed files.", 200
