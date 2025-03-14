from posix import DirEntry
from src.lib.dataclasses import DirectoryFile, ServiceArguments
from src.lib.exceptions.exceptions import RequestError
from src.lib.dataclasses.api import VideoRequest, ComicRequest, NameChangeRequest


def create_file(dir_entry: DirEntry):
    return DirectoryFile(dir_entry.name, dir_entry.path)


def create_file(name: str, path: str):
    return DirectoryFile(name, path)


def create_basic_service_args(directory_in: str, directory_out: str):
    return ServiceArguments(directory_in, directory_out)


def create_service_arguments(args):
    return ServiceArguments(**args)


def create_video_request(request):
    try:
        return VideoRequest(**request.form)
    except TypeError as e:
        raise RequestError(e)


def create_comic_request(request):
    try:
        return ComicRequest(**request.form)
    except TypeError as e:
        raise RequestError(e)


# def create_name_change_request(request):
#     try:
#         return VideoRequest(**request.form)
#     except TypeError as e:
#         raise RequestError(e)
