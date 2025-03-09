from warnings import warn
from argparse import ArgumentParser
from src.lib.dataclasses.api import NameChange, NameChangeRequest


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
    changes = [NameChange(old=old, new=new) for old, new in rename_mapping.items()]
    return NameChangeRequest(changes=changes)
