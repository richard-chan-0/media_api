import os
from subprocess import run, PIPE
from typing import Iterable, Callable
from PIL import Image
from src.lib.exceptions.exceptions import FileSystemError
from src.lib.factories.factories import create_file
from src.lib.dataclasses import DirectoryFile, NameChangeRequest
import logging
from dotenv import load_dotenv
from zipfile import ZipFile
from pathlib import Path
from shutil import move

load_dotenv()

logger = logging.getLogger(__name__)

default_ignore_files = [".DS_Store", ".localized"]


def get_files(path: str, ignore_files=[]) -> Iterable[DirectoryFile]:
    """function to get list of files from a path"""
    logger.info(f"getting files from path: {path}")
    if not os.path.exists(path):
        raise FileSystemError(f"could not find: {path}")

    if is_file(path):
        filename = os.path.basename(path)
        file_path = os.path.normpath(path)
        return [create_file(filename, file_path)]

    with os.scandir(path) as entries:
        directory_files = [
            create_file(entry.name, entry.path)
            for entry in entries
            if os.path.isfile(entry.path)
            and entry.name not in [*ignore_files, *default_ignore_files]
        ]

        directory_files.sort(key=lambda entry: entry.name)

        return directory_files


def get_sorted_files(
    directory_in: str, sort_method=lambda entry: entry.name
) -> Iterable[DirectoryFile]:
    """function to get list of files from a directory and sort them"""
    logger.info(f"getting sorted files from directory: {directory_in}")
    directory_entries = get_files(directory_in)
    directory_entries.sort(key=sort_method)
    return directory_entries


def get_sub_directories(directory: str) -> Iterable[DirectoryFile]:
    """function to get list of files from a directory"""
    if not os.path.exists(directory):
        raise FileSystemError(f"could not find directory: {directory}")

    with os.scandir(directory) as entries:
        return [
            create_file(entry.name, entry.path)
            for entry in entries
            if os.path.isdir(entry.path)
        ]


def is_file_an_image(file_name: str) -> bool:
    """function to determine if file name is a image format"""
    return "png" in file_name or "jpg" in file_name


def is_compressed(file_name: str) -> bool:
    """function to determine if file name is compressed (.zip, .cbz)"""
    return ".cbz" in file_name or ".zip" in file_name


def get_images(directory: str) -> Iterable[DirectoryFile]:
    """function to get list of files from a directory with a image (jpg,png) extension"""
    return [file for file in get_files(directory) if is_file_an_image(file.name)]


def rename_page_images(
    directory_out: str, files: Iterable[DirectoryFile], name_function: Callable
):
    """rename image file in a directory"""
    story = os.getenv("STORY")
    chapter = os.getenv("CHAPTER")

    for page_number, file in enumerate(files):
        new_name = name_function(story, chapter, page_number)
        img = Image.open(file.path)
        new_path = create_new_file_path(directory_out, new_name)
        img.save(new_path)
        os.remove(file.path)


def rename_list_files(rename_mapping: NameChangeRequest):
    for change in rename_mapping.changes:
        try:
            logger.info("renaming file from %s to %s", change.old_path, change.new_path)
            os.rename(change.old_path, change.new_path)
        except FileNotFoundError | OSError as err:
            logger.error(err)
            raise FileSystemError(f"could not rename file: {change.old_path}")


def create_sub_directory(directory_out: str, sub_directory: str):
    """function to create a sub directory"""
    sub_directory_path = f"{directory_out}/{sub_directory}"
    if not os.path.exists(sub_directory_path):
        os.mkdir(sub_directory_path)
    return sub_directory_path


def move_file(old_path: str, new_path: str):
    """function to move a file by changing path"""
    if not os.path.exists(old_path):
        raise FileSystemError(f"could not find file with path: {old_path}")
    try:
        os.rename(old_path, new_path)
    except FileNotFoundError as err:
        logger.error(err)
        raise FileSystemError(f"could not move file to path: {new_path}")


def move_files(files_to_move: Iterable[DirectoryFile], destination_folder: str):
    """function to move several files into a single directory"""
    if not files_to_move:
        logger.info("no files given to move")
        return

    destination_paths = []

    for file in files_to_move:
        source = file.path
        destination = create_new_file_path(destination_folder, file.name)
        logger.info("moving file %s to path %s", file.name, destination)
        move_file(source, destination)
        destination_paths.append(destination)

    return destination_paths


def transfer_files(source_directory: str, destination_directory: str):
    """function to read files from source directory into destination directory"""
    source_files = get_files(source_directory)
    logger.info("moving files from %s to %s", source_directory, destination_directory)
    move_files(source_files, destination_directory)


def remove_directory(path: str):
    """function to remove directory and it's contents"""
    if not os.path.exists(path):
        raise FileSystemError(f"could not remove file: {path}")
    try:
        files = get_files(path)
        for file in files:
            os.remove(file.path)
        os.rmdir(path)
    except Exception as err:
        logger.error(err)
        raise FileExistsError(err)


def remove_file(path: str):
    """function to remove a file or directory"""
    try:
        os.remove(path)
    except Exception as err:
        logger.error(err)
        raise FileExistsError(err)


def get_env(env_var: str) -> str:
    """function to return environment variable"""
    return os.getenv(env_var)


def create_new_file_path(new_dir: str, file_name: str) -> str:
    """function to concat directory and file into new path"""
    return f"{new_dir}/{file_name}"


def run_shell_command(command: Iterable[str]):
    """runs a shell command given a list of arguments"""
    return run(command, stdout=PIPE, encoding="utf-8")


def is_dir(path: str):
    """function to determine if path is directory"""
    if not os.path.exists(path):
        raise FileExistsError("path does not exist")
    return os.path.isdir(path)


def is_file(path: str):
    """function to determine if path is directory"""
    if not os.path.exists(path):
        raise FileExistsError("path does not exist")
    return os.path.isfile(path)


def parse_path(path: str):
    """function to determine if path is directory"""
    if not os.path.exists(path):
        raise FileExistsError("path does not exist")
    return os.path.split(path)


def extract_zip_file_content(directory_in: str, zip_files: Iterable[DirectoryFile]):
    """function to extract all page files from chapter files"""
    page_number = 0
    for file in zip_files:
        logger.info("unzipping file: %s", file.name)
        if not is_compressed(file.name):
            continue
        with ZipFile(file.path, "r") as zip_ref:
            jpg_files = [f for f in zip_ref.namelist() if f.lower().endswith(".jpg")]
            jpg_files.sort()
            for jpg_file in jpg_files:
                new_name = (
                    f"0{page_number}.jpg" if page_number < 10 else f"{page_number}.jpg"
                )
                dest_path = os.path.join(directory_in, new_name)
                with zip_ref.open(jpg_file) as source, open(dest_path, "wb") as target:
                    target.write(source.read())
                page_number += 1


def create_zip_file(zip_file_path: str, files_to_zip: Iterable[DirectoryFile]):
    """function to zip a list of files"""
    with ZipFile(zip_file_path, "w") as zip:
        for file in files_to_zip:
            try:
                zip.write(file)
            except Exception as err:
                raise FileSystemError(err)

        logger.info("zip created with path %s", zip_file_path)


def join_path(*args):
    return os.path.join(*args)
