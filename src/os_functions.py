import os
from .name_functions import generate_name
from PIL import Image


def get_files(directory):
    """function to get list of files"""
    with os.scandir(directory) as entries:
        return [entry.name for entry in entries]


def rename_files(directory_in, directory_out, files):
    """rename files in a directory"""
    story = os.getenv("STORY")
    chapter = os.getenv("CHAPTER")

    for page_number, file in enumerate(files):
        old = f"{directory_in}/{file}"
        new_name = generate_name(story, chapter, page_number)
        img = Image.open(old)
        img.save(f"{directory_out}/{new_name}")
        os.remove(old)
