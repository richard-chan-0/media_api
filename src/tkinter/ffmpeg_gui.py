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
from json import dumps

from logging import getLogger

logger = getLogger(__name__)


class FfmpegGui(Gui):
    BACKGROUND_COLOR = "#101010"
    DEFAULT_OPTIONS = {"bg": BACKGROUND_COLOR, "highlightbackground": BACKGROUND_COLOR}

    def __init__(self):
        self.__root = Tk()
        self.__root.title("ffmpeg Utility")

        self.__service_message_row = 100

        self.__service_message = None

    def __create_window(self):
        width = 900
        height = 450
        dimension = f"{width}x{height}"
        self.__root.geometry(dimension)
        self.__root.configure(bg=self.BACKGROUND_COLOR)

    def __init_gui(self):
        """function to initialize the gui"""
        logger.info("configuring menu")
        self.__create_window()
        self.__create_console_message()

    def __log_to_console(self, message: str):
        """function to update the console window in gui to message"""
        self.__service_message.configure(state="normal")
        self.__service_message.delete(1.0, END)
        self.__service_message.insert(INSERT, message)
        self.__service_message.configure(state="disabled")

    def __create_console_message(self):
        """function to create the console window on gui"""
        create_label(
            self.__root,
            text="Console",
            row=self.__service_message_row,
            options=self.DEFAULT_OPTIONS,
        )

        options = {
            "background": "black",
            "width": "100",
            "height": "20",
        }
        self.__service_message = create_console_textbox(
            self.__root,
            options=options,
            row=self.__service_message_row,
            col=1,
        )

    def start(self):
        self.__init_gui()
        self.__root.mainloop()
