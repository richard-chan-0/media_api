from posix import DirEntry
from src.data_types.DirectoryFile import DirectoryFile
from src.data_types.ServiceArguments import ServiceArguments
from src.data_types.media_types import AudioStream, SubtitleStream, AttachmentStream


def create_file(dir_entry: DirEntry):
    return DirectoryFile(dir_entry.name, dir_entry.path)


def create_file(name: str, path: str):
    return DirectoryFile(name, path)


def create_basic_service_args(directory_in: str, directory_out: str):
    return ServiceArguments(directory_in, directory_out)


def create_audio_stream(stream: dict):
    language = stream["tags"]["language"]
    is_default = bool(stream["disposition"]["default"])
    stream_number = stream["index"]
    return AudioStream(
        stream_number=stream_number, language=language, is_default=is_default
    )


def create_subtitle_stream(stream: dict):
    language = stream["tags"]["language"]
    is_default = bool(stream["disposition"]["default"])
    stream_number = stream["index"]
    return SubtitleStream(
        stream_number=stream_number, language=language, is_default=is_default
    )


def create_attachment_stream(stream: dict):
    stream_number = stream["index"]
    file_name = stream["tags"]["filename"]
    return AttachmentStream(stream_number, file_name)
