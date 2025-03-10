from src.lib.dataclasses import VideoRequest, ServiceArguments, NameChangeRequest
from src.lib.utilities.os_functions import join_path
from src.lib.service_constants import IMAGES_IN, IMAGES_OUT
from src.services.rename_media.rename_media import create_jellyfin_episodes_mapping


def get_jellyfin_video_names_from_files(request):
    video_request = VideoRequest(**request.form)
    files = request.files.getlist("files")

    for file in files:
        file_path = join_path(IMAGES_IN, file.filename)
        file.save(file_path)

    return create_jellyfin_episodes_mapping(
        ServiceArguments(
            **{
                "directory_in": IMAGES_IN,
                "directory_out": IMAGES_OUT,
                "start_number": video_request.start_number,
                "season_number": video_request.season_number,
            }
        )
    )
