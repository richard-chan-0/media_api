from warnings import warn
from argparse import ArgumentParser
from src.lib.dataclasses.api import NameChange, NameChangeRequest
from marshmallow import ValidationError
from src.lib.exceptions.exceptions import BadSchemaError, RequestError, ServiceError
from src.lib.utilities.os_functions import join_path
from src.lib.service_constants import (
    INPUT_DIRECTORY,
    BAD_REQUEST_CODE,
    INTERNAL_SERVER_ERROR_CODE,
)
from flask import jsonify
import logging

logger = logging.getLogger(__name__)


def deprecate_function():
    warn("This function is deprecated", DeprecationWarning, stacklevel=2)


def read_dict(dict_path: str, dict_obj: dict):
    keys = dict_path.split(".")
    for key in keys:
        if not isinstance(dict_obj, dict):
            return

        value = dict_obj.get(key)
        if not value:
            return
        dict_obj = value

    return value


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(description="process media to go into server")
    parser.add_argument(
        "type",
        type=str,
        choices=["books", "videos", "reorganize"],
        help="media utility type",
    )
    return parser


def convert_to_name_change_request(rename_mapping: dict[str, str]):
    changes = [NameChange(old, new) for old, new in rename_mapping.items()]
    return NameChangeRequest(changes=changes)


def check_request_schema(schema, request):
    try:
        return schema.load(request.get_json())
    except ValidationError as e:
        raise BadSchemaError(f"Invalid request schema: {e}")


def get_files_from_request(request, file_key):
    files = request.files.getlist(file_key)
    logger.info("no files found in request")

    for file in files:
        file_path = join_path(INPUT_DIRECTORY, file.filename)
        try:
            file.save(file_path)
        except OSError as e:
            raise ServiceError(e)
