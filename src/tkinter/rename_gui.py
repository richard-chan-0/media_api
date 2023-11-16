from tkinter import *
from src.services import (
    get_services,
    RENAME_FILES_TO_JELLY_EPISODES,
    RENAME_FILES_TO_JELLY_COMICS,
)
from src.factories.factories import create_basic_service_args
from src.exceptions.exceptions import ServiceError
from src.utilities.os_functions import transfer_files
from logging import getLogger

logger = getLogger(__name__)


class RenameGui:
    COLUMN_COMPONENT = "1"
    COLUMN_BUTTON = "2"

    DEFAULT_PADDINGY = 5
    DEFAULT_PADDINGX = 5

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

        self.__download_text = None
        self.__download_entry = None
        self.__download_button = None

        self.__story_name_text = None
        self.__story_name_entry = None

        self.__story_name_button = None

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

    def __create_numeric_dropdown(self):
        self.__create_label(
            "Select Number for Volume/Season", self.__numeric_dropdown_row
        )
        options = [i for i in range(15)]
        self.__numeric_click = StringVar()
        self.__numeric_click.set(options[0])
        self.__numeric_dropdown = OptionMenu(
            self.__root, self.__numeric_click, *options
        )
        self.__numeric_dropdown.grid(
            row=self.__numeric_dropdown_row,
            column=self.COLUMN_COMPONENT,
            pady=self.DEFAULT_PADDINGY,
            sticky=W,
        )

    def __create_service_dropdown(self, options):
        self.__create_label("Select Service", self.__service_dropdown_row)
        self.__service_click = StringVar()
        self.__service_click.set(options[0])
        self.__service_dropdown = OptionMenu(
            self.__root, self.__service_click, *options
        )
        self.__service_dropdown.grid(
            row=self.__service_dropdown_row,
            column=self.COLUMN_COMPONENT,
            pady=self.DEFAULT_PADDINGY,
            sticky=W,
        )

    def __cleanup(self):
        widgets = [
            self.__numeric_dropdown,
            self.__story_name_button,
            self.__story_name_entry,
            self.__download_entry,
            self.__download_button,
        ]
        for widget in widgets:
            if widget:
                widget.destroy()

    def __configure_service(self, service_name):
        logger.info("configuring utility...")
        service_metadata = get_services()[service_name]
        self.__directory_in = service_metadata.directory_in
        self.__directory_out = service_metadata.directory_out
        self.__service = service_metadata.service

    def __add_service_widgets(self):
        self.__cleanup()
        self.__selected_service = self.__service_click.get()
        self.__configure_service(self.__selected_service)
        if self.__selected_service == RENAME_FILES_TO_JELLY_EPISODES:
            self.__create_numeric_dropdown()

        elif self.__selected_service == RENAME_FILES_TO_JELLY_COMICS:
            self.__create_story_name_entry()

        self.__create_download_files_entry()
        self.__create_download_button()

    def __pull_files_from_download(self):
        download_path = self.__get_widget_value(self.__download_text)
        if not download_path or not self.__directory_in:
            self.__update_service_message(
                "no download directory or destination directory set"
            )
            return

        try:
            transfer_files(download_path, self.__directory_in)
            self.__update_service_message("files have been pulled!")
        except ServiceError as err:
            self.__update_service_message(str(err))

    def __create_download_button(self):
        self.__download_button = Button(
            self.__root,
            text="Pull Files",
            default="active",
            command=self.__pull_files_from_download,
        )
        self.__download_button.grid(
            row=self.__download_entry_row, column=self.COLUMN_BUTTON
        )

    def __create_service_dropdown_button(self):
        self.__service_dropdown_button = Button(
            self.__root,
            text="Select Service",
            default="active",
            command=self.__add_service_widgets,
        )
        self.__service_dropdown_button.grid(
            row=self.__service_dropdown_row, column=self.COLUMN_BUTTON
        )

    def __create_submit_button(self):
        self.__submit_button = Button(
            self.__root, text="Rename!", default="active", command=self.__run_service
        )
        self.__submit_button.grid(
            row=self.__submit_button_row,
            column=self.COLUMN_COMPONENT,
            pady=self.DEFAULT_PADDINGY,
            sticky=W,
        )

    def __create_label(self, text, row, column="0"):
        label = Label(self.__root, text=text)
        label.grid(row=row, column=column, pady=self.DEFAULT_PADDINGY, sticky=W)
        return label

    def __create_download_files_entry(self):
        self.__create_label("Enter Download Directory: ", row=self.__download_entry_row)
        self.__download_text = StringVar()
        self.__download_entry = Entry(self.__root, textvariable=self.__download_text)
        self.__download_entry.grid(
            row=self.__download_entry_row, column=self.COLUMN_COMPONENT, sticky=W
        )

    def __create_story_name_entry(self):
        self.__create_label("Enter the Story Name:", row=self.__story_name_row)
        self.__story_name_text = StringVar()
        self.__story_name_entry = Entry(
            self.__root, textvariable=self.__story_name_text
        )
        self.__story_name_entry.grid(
            row=self.__story_name_row, column=self.COLUMN_COMPONENT, sticky=W
        )

    def __config(self):
        self.__create_window()

        services = get_services()
        options = [service for service in services.keys() if "jellyfin" in service]
        self.__create_service_dropdown(options)
        self.__create_service_dropdown_button()

        self.__create_submit_button()
        self.__create_label("Submit Button", row=self.__submit_button_row)
        self.__create_service_message()

    def start(self):
        self.__config()
        self.__root.mainloop()

    def __get_widget_value(self, widget):
        return "" if not widget else widget.get()

    def __run_service(self):
        service_args = create_basic_service_args(
            self.__directory_in, self.__directory_out
        )
        service_args.season_number = self.__get_widget_value(self.__numeric_click)
        service_args.story = self.__get_widget_value(self.__story_name_text)
        try:
            self.__update_service_message("running service")
        except ServiceError as err:
            self.__update_service_message(str(err))

    def __update_service_message(self, message):
        self.__service_message.config(text=message)

    def __create_service_message(self):
        self.__create_label(text="Service Message", row=self.__service_message_row)

        self.__service_message = self.__create_label(
            "", row=self.__service_message_row, column=self.COLUMN_COMPONENT
        )
