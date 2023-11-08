from dotenv import load_dotenv
import os
from src.services import return_service
from src.data_types.ServiceMetaData import ServiceMetaData
from src.exceptions.exceptions import ServiceError

load_dotenv()

if __name__ == "__main__":
    utility_type = os.getenv("UTILITY_TYPE")

    service_meta_data: ServiceMetaData = return_service(utility_type)

    service = service_meta_data.service
    directory_in = service_meta_data.directory_in
    directory_out = service_meta_data.directory_out
    try:
        service(directory_in, directory_out)
    except ServiceError as err:
        print(err)
