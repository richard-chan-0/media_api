from src.exceptions.exceptions import ServiceError, OrganizeChaptersToVolError
from src.utilities.os_functions import get_files, get_organization_file
from json import load


def read_organization_file():
    """returns content of json organization file"""
    file = get_organization_file()
    return load(file)


def organize_chapters_to_vol(directory_in: str, directory_out: str):
    # TODO: read files in directory in
    files = get_files(directory=directory_in)

    # read organization file
    schema = read_organization_file()

    # TODO: write folders into directory_out
    return {}


def main(directory_in: str, directory_out: str):
    """main function for organizing files feature"""
    try:
        organize_chapters_to_vol(directory_in, directory_out)
    except OrganizeChaptersToVolError as err:
        print("error occurred when organizing files")
        raise ServiceError(err)
