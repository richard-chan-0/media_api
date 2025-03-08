"""
requirements:
download directory
volume number
start number?
output directory
"""

from src.lib.data_types import VideoRequest, ServiceArguments
from src.lib.utilities.os_functions import transfer_files
from src.lib.data_types.service_constants import IMAGES_IN, IMAGES_OUT
from src.services.rename_media.rename_media import create_jellyfin_episodes_mapping


def videos(request_args):
    request = VideoRequest(**request_args)

    transfer_files(request.source, IMAGES_IN)

    return create_jellyfin_episodes_mapping(
        ServiceArguments(
            **{
                "directory_in": IMAGES_IN,
                "directory_out": IMAGES_OUT,
                "start_number": request.start_number,
                "season_number": request.volume_number,
            }
        )
    )
