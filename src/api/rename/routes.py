from flask import Blueprint, request, jsonify
import logging
from src.api.rename.videos import (
    get_jellyfin_video_names_from_request,
)
from src.api.rename.comics import get_jellyfin_comic_names_from_request
from src.lib.dataclasses.api import (
    name_change_request_schema,
)
from src.lib.utilities.app_functions import (
    convert_to_name_change_request,
    check_request_schema,
)
from src.lib.utilities.os_functions import (
    rename_list_files,
    get_files,
    transfer_files,
    remove_file,
)
from src.lib.service_constants import INPUT_DIRECTORY, OUTPUT_DIRECTORY
from src.lib.utilities.os_functions import create_new_file_path

logger = logging.getLogger(__name__)
rename = Blueprint("rename", __name__, url_prefix="/rename")

function_map = {
    "videos": get_jellyfin_video_names_from_request,
    "comics": get_jellyfin_comic_names_from_request,
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
    input_directory_files = get_files(INPUT_DIRECTORY)
    output_directory_files = get_files(OUTPUT_DIRECTORY)
    return jsonify([*input_directory_files, *output_directory_files]), 200


@rename.route("/push", methods=["GET"])
def push_files():
    logger.info("pushing files to shared folder")
    transfer_files(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
    return "Successfully pushed files.", 200


@rename.route("/delete", methods=["POST"])
def delete_file():
    logger.info("deleting file")
    file = request.form["file-to-delete"]
    is_file_deleted = False
    for directory in [INPUT_DIRECTORY, OUTPUT_DIRECTORY]:
        delete_file_path = create_new_file_path(directory, file)
        logger.info(f"deleting file {delete_file_path}")
        try:
            remove_file(delete_file_path)
            is_file_deleted = True
            break
        except FileExistsError as err:
            logger.error(err)

    return (
        ("Successfully deleted file.", 200)
        if is_file_deleted
        else ("Could not delete file: File not found.", 404)
    )
