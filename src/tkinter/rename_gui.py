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
from src.tkinter.tkinter_functions import *
from typing import Iterable
from src.tkinter.gui import Gui

from logging import getLogger

logger = getLogger(__name__)


class RenameGui(Gui):
    def __init__(self):
        self.__root = Tk()

        self.__directory_in = None
        self.__directory_out = None
        self.__download_entry_row = 1
        self.__service_dropdown_row = 0
        self.__story_name_row = 2
        self.__numeric_dropdown_row = 2
        self.__submit_button_row = 3
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

        self.__service_dropdown = None
        self.__service_click = None
        self.__service_dropdown_button = None

        self.__selected_service = None

    def __create_window(self):
        width = 700
        height = 250
        dimension = f"{width}x{height}"
        self.__root.geometry(dimension)

    def __create_numeric_dropdown_menu(self):
        options = [i for i in range(15)]
        click, menu = create_dropdown(self.__root, options, self.__numeric_dropdown_row)
        self.__numeric_click = click
        self.__numeric_dropdown = menu

    def __create_numeric_dropdown_component(self):
        self.__numeric_label = create_label(
            self.__root, "Select Number for Volume/Season", self.__numeric_dropdown_row
        )
        self.__create_numeric_dropdown_menu()

    def __create_service_dropdown_menu(self, options):
        click, _ = create_dropdown(self.__root, options, self.__service_dropdown_row)
        self.__service_click = click
        # self.__service_dropdown = menu

    def __create_service_dropdown_component(self, options: Iterable[str]):
        create_label(self.__root, "Select Service", self.__service_dropdown_row)
        self.__create_service_dropdown_button()
        self.__create_service_dropdown_menu(options)

    def __cleanup(self):
        """function to clean up widgets from window"""
        widgets: Iterable[Widget] = [
            self.__numeric_dropdown,
            self.__numeric_label,
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

    def __add_download_widget(self):
        logger.info("adding download widget to window")
        self.__cleanup()
        self.__create_download_files_entry()

    def __add_service_widgets(self):
        if self.__selected_service == RENAME_FILES_TO_JELLY_EPISODES:
            self.__create_numeric_dropdown_component()

        elif (
            self.__selected_service == RENAME_FILES_TO_JELLY_COMICS
            or self.__selected_service == RENAME_TO_CLEANUP
        ):
            self.__create_story_name_entry()

    def __pull_files_from_download(self):
        self.__cleanup()
        self.__selected_service = self.__service_click.get()
        self.__configure_service(self.__selected_service)

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

    def __create_download_button(self):
        self.__download_button = create_buttoon(
            self.__root,
            "Pull Files",
            self.__pull_files_from_download,
            self.__download_entry_row,
        )

    def __create_service_dropdown_button(self):
        create_buttoon(
            self.__root,
            "Select Service",
            self.__add_download_widget,
            self.__service_dropdown_row,
        )

    def __create_submit_button(self):
        create_label(self.__root, "Submit Button", row=self.__submit_button_row)

        create_buttoon(
            self.__root,
            "Rename",
            self.__run_service,
            self.__submit_button_row,
        )

    def __create_download_files_entry(self):
        self.__download_label = create_label(
            self.__root, "Enter Download Directory: ", row=self.__download_entry_row
        )
        self.__create_download_button()

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

        self.__create_submit_button()
        self.__create_service_message()

    def __run_service(self):
        logger.info("retrieving service configurations")
        service_args = create_basic_service_args(
            self.__directory_in, self.__directory_out
        )
        service_args.season_number = get_widget_value(self.__numeric_click)
        service_args.story = get_widget_value(self.__story_name_text)
        try:
            logger.info("running service")
            self.__service(service_args)
            self.__update_service_message("Renaming Completed")
        except ServiceError as err:
            self.__update_service_message(str(err))

    def __update_service_message(self, message: str):
        self.__service_message.config(text=message)

    def __create_service_message(self):
        create_label(
            self.__root, text="Service Message", row=self.__service_message_row
        )

        options = {"background": "black"}
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
