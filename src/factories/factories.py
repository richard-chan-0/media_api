from posix import DirEntry
from src.data_types.system_files import DirectoryFile


def create_file(dir_entry: DirEntry):
    return DirectoryFile(dir_entry.name, dir_entry.path)


def create_file(name, path):
    return DirectoryFile(name, path)
