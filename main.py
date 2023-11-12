from dotenv import load_dotenv
from src.utilities.os_functions import get_env, create_sub_directory
from src.services import return_service
from src.data_types.ServiceMetaData import ServiceMetaData
from src.exceptions.exceptions import ServiceError
import logging
import os

logger = logging.getLogger(__name__)

load_dotenv()


def main(utility_type):
    """main function for utility"""
    logger.info("retrieving service")
    service_meta_data: ServiceMetaData = return_service(utility_type)

    service = service_meta_data.service
    directory_in = service_meta_data.directory_in
    directory_out = service_meta_data.directory_out

    logger.info("creating missing directories")
    create_sub_directory(".", directory_in)
    create_sub_directory(".", directory_out)

    try:
        service(directory_in, directory_out)
    except ServiceError as err:
        logger.error(err)


if __name__ == "__main__":
    utility_type = os.getenv("UTILITY_TYPE")
    main(utility_type)
