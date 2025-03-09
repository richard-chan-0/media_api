from src.lib.dataclasses import VideoRequest, ServiceArguments, NameChangeRequest
from src.lib.utilities.os_functions import transfer_files, rename_list_files
from src.lib.service_constants import IMAGES_IN, IMAGES_OUT
from src.services.rename_media.rename_media import create_jellyfin_episodes_mapping


def get_jellyfin_video_names(request: VideoRequest):
    transfer_files(request.source, IMAGES_IN)

    return create_jellyfin_episodes_mapping(
        ServiceArguments(
            **{
                "directory_in": IMAGES_IN,
                "directory_out": IMAGES_OUT,
                "start_number": request.start_number,
                "season_number": request.season_number,
            }
        )
    )


def update_video_names(request_args: NameChangeRequest):
    rename_list_files(request_args)
