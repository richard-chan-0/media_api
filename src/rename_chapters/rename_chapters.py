from ..utilities.os_functions import rename_files, get_files


def main(directory_in, directory_out):
    """main logic for utility"""
    directory_entries = get_files(directory_in)
    files = [file.path for file in directory_entries]
    rename_files(directory_out, files)
