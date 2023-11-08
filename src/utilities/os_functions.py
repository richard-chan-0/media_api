import os
from ..rename_chapters.name_functions import generate_name
from typing import Iterable
from PIL import Image


def get_files(directory: str) -> Iterable:
    """function to get list of files"""
    with os.scandir(directory) as entries:
        return [entry for entry in entries]


def rename_files(directory_out, files):
    """rename files in a directory"""
    story = os.getenv("STORY")
    chapter = os.getenv("CHAPTER")

    for page_number, file in enumerate(files):
        new_name = generate_name(story, chapter, page_number)
        img = Image.open(file)
        img.save(f"{directory_out}/{new_name}")
        os.remove(file)


def get_organization_file():
    """returns the env variable for the json file to organize volumes and chapters"""
    return os.getenv("ORGANIZATION_FILE")


def make_sub_directory(directory_out: str, sub_directory: str):
    """function to create a sub directory"""
    sub_directory_path = f"{directory_out}/{sub_directory}"
    if not os.path.exists(sub_directory_path):
        os.mkdir(sub_directory_path)
    return sub_directory_path


def move_file(old_path: str, new_path: str):
    """function to move a file by changing path"""
    os.rename(old_path, new_path)
