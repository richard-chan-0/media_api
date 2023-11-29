from tkinter import *
from src.services import (
    get_list_service,
    return_service,
    RENAME_FILES_TO_JELLY_EPISODES,
    RENAME_FILES_TO_JELLY_COMICS,
    RENAME_TO_CLEANUP,
)
from src.factories.factories import create_basic_service_args
from src.exceptions.exceptions import ServiceError
from src.utilities.os_functions import transfer_files
from src.rename_media.rename_media import rename_files
from src.tkinter.tkinter_functions import *
from typing import Iterable
from src.tkinter.gui import Gui

from logging import getLogger

logger = getLogger(__name__)


class RenameGui(Gui):
    def __init__(self):
        self.__root = Tk()
        self.__root.title("Media Utility")

        self.__directory_in = None
        self.__directory_out = None
        self.__download_entry_row = 1
        self.__service_dropdown_row = 0
        self.__story_name_row = 2
        self.__numeric_dropdown_row = 2
        self.__extension_dropdown_row = 3
        self.__submit_button_row = 4
        self.__service_message_row = 5

        self.__submit_button = None
        self.__service_message = None

        self.__download_label = None
        self.__download_text = None
        self.__download_entry = None
        self.__download_button = None

        self.__story_name_text = None
        self.__story_name_entry = None

        self.__story_name_button = None

        self.__numeric_label = None
        self.__numeric_dropdown = None
        self.__numeric_click = None

        self.__extension_label = None
        self.__extension_dropdown = None
        self.__extension_click = None

        self.__rename_mapping = None

        self.__numeric_options = [i for i in range(15)]
        self.__extension_options = ["mkv", "ass", "default.ass", "mp4"]

    def __create_window(self):
        width = 1000
        height = 250
        dimension = f"{width}x{height}"
        self.__root.geometry(dimension)

    def __create_numeric_dropdown_menu(self):
        click, menu = create_dropdown(
            self.__root,
            self.__numeric_options,
            self.__numeric_dropdown_row,
            command=lambda x: self.__update_service_message(f"you selected {x}"),
        )
        self.__numeric_click = click
        self.__numeric_dropdown = menu

    def __create_extension_dropdown_menu(self):
        click, menu = create_dropdown(
            self.__root,
            self.__extension_options,
            self.__extension_dropdown_row,
            command=lambda x: self.__update_service_message(f"you selected {x}"),
        )
        self.__extension_click = click
        self.__extension_dropdown = menu

    def __create_numeric_dropdown_component(self):
        self.__numeric_label = create_label(
            self.__root, "Volume/Season?", self.__numeric_dropdown_row
        )
        self.__create_numeric_dropdown_menu()

    def __create_extension_dropdown_component(self):
        self.__extension_label = create_label(
            self.__root, "File Output Type", self.__extension_dropdown_row
        )
        self.__create_extension_dropdown_menu()

    def __create_service_dropdown_menu(self, options):
        click, _ = create_dropdown(
            self.__root,
            options,
            self.__service_dropdown_row,
            command=self.__add_service_widgets,
        )

    def __create_service_dropdown_component(self, options: Iterable[str]):
        create_label(self.__root, "Service?", self.__service_dropdown_row)
        self.__create_service_dropdown_menu(options)

    def __cleanup(self):
        """function to clean up widgets from window"""
        widgets: Iterable[Widget] = [
            self.__numeric_dropdown,
            self.__numeric_label,
            self.__extension_label,
            self.__extension_dropdown,
            self.__story_name_button,
            self.__story_name_entry,
            self.__download_entry,
            self.__download_button,
            self.__download_label,
        ]
        destroy_widgets(widgets)

    def __configure_service(self, service_name: str):
        logger.info("configuring utility...")
        service_metadata = return_service(service_name)
        self.__directory_in = service_metadata.directory_in
        self.__directory_out = service_metadata.directory_out
        self.__service = service_metadata.service

    def __add_service_widgets(self, value):
        logger.info("adding download widget to window")
        self.__update_service_message(f"setting up {value} service")
        self.__configure_service(value)
        self.__cleanup()
        self.__create_download_files_entry()
        frame = create_frame(
            self.__root, row=self.__submit_button_row, column=COLUMN_COMPONENT
        )
        self.__create_download_button(frame)
        self.__create_submit_button(frame)
        self.__create_rename_button(frame)

        if value == RENAME_FILES_TO_JELLY_EPISODES:
            self.__create_numeric_dropdown_component()
            self.__create_extension_dropdown_component()

        elif value == RENAME_FILES_TO_JELLY_COMICS or value == RENAME_TO_CLEANUP:
            self.__create_story_name_entry()

    def __pull_files_from_download(self):
        download_path = get_widget_value(self.__download_text)
        if not download_path or not self.__directory_in:
            self.__update_service_message(
                "no download directory or destination directory set"
            )
            return

        try:
            transfer_files(download_path, self.__directory_in)
            self.__update_service_message("files have been pulled!")
            self.__add_service_widgets()
        except ServiceError as err:
            self.__update_service_message(str(err))

    def __create_download_button(self, root):
        self.__download_button = create_buttoon(
            root=root,
            button_text="Pull Files?",
            action=self.__pull_files_from_download,
            row_position=0,
            col_position=0,
        )

    def __create_rename_button(self, root):
        create_buttoon(
            root=root,
            button_text="Update Files",
            action=self.__update_files,
            row_position=0,
            col_position=2,
        )

    def __create_submit_button(self, root):
        create_label(self.__root, "Run", row=self.__submit_button_row)

        create_buttoon(
            root,
            button_text="Create New File Names",
            action=self.__create_rename_mapping,
            row_position=0,
            col_position=1,
        )

    def __create_download_files_entry(self):
        self.__download_label = create_label(
            self.__root, "Download Directory: ", row=self.__download_entry_row
        )

        text, entry = create_input_field(self.__root, self.__download_entry_row)
        self.__download_text = text
        self.__download_entry = entry

    def __create_story_name_entry(self):
        create_label(self.__root, "Enter the Story Name:", row=self.__story_name_row)
        text, entry = create_input_field(self.__root, self.__story_name_row)
        self.__story_name_text = text
        self.__story_name_entry = entry

    def __config(self):
        logger.info("configuring menu")
        self.__create_window()

        options = [service for service in get_list_service() if "rename" in service]
        self.__create_service_dropdown_component(options)
        self.__create_service_message()

    def __create_rename_mapping(self):
        """function that runs rename methods"""
        logger.info("retrieving service configurations")
        service_args = create_basic_service_args(
            self.__directory_in, self.__directory_out
        )
        service_args.season_number = get_widget_value(self.__numeric_click)
        service_args.story = get_widget_value(self.__story_name_text)
        service_args.extension = get_widget_value(self.__extension_click)
        logger.info("running service")

        self.__rename_mapping = self.__service(service_args)
        self.__update_service_message(self.__rename_mapping)

    def __update_files(self):
        is_okay = create_confirmation_window(
            "Confirmation", "Are you sure you want to rename these files?"
        )

        if not is_okay:
            self.__update_service_message("rename files aborted!")
            return

        self.__update_service_message("renaming files!")
        rename_files(rename_mapping=self.__rename_mapping)

    def __update_service_message(self, message: str):
        self.__service_message.config(text=message)

    def __create_service_message(self):
        create_label(self.__root, text="Console", row=self.__service_message_row)

        options = {"background": "black", "width": "50"}
        self.__service_message = create_label(
            self.__root,
            "",
            row=self.__service_message_row,
            column=COLUMN_COMPONENT,
            options=options,
        )

    def start(self):
        self.__config()
        self.__root.mainloop()
