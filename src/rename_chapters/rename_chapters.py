from ..utilities.os_functions import rename_files, get_files


def main(directory_in, directory_out):
    """main logic for utility"""
    files = get_files(directory_in)
    rename_files(directory_in, directory_out, files)
