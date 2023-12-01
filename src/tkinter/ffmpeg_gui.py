from tkinter import *
from src.data_types.media_types import MediaStream
from src.tkinter.tkinter_functions import *
from src.ffmpeg.ffmpeg_functions import *
from typing import Iterable
from src.tkinter.gui import Gui
from json import dumps
from src.exceptions.exceptions import ServiceError

from logging import getLogger

logger = getLogger(__name__)


class FfmpegGui(Gui):
    BACKGROUND_COLOR = "#101010"
    DEFAULT_OPTIONS = {"bg": BACKGROUND_COLOR, "highlightbackground": BACKGROUND_COLOR}

    def __init__(self):
        self.__root = Tk()
        self.__root.title("ffmpeg Utility")

        self.__file_entry_row = 0
        self.__inspect_file_button_row = 1
        self.__subtitles_dropdown_row = 2
        self.__audio_dropdown_row = 3
        self.__set_default_streams_row = 4

        self.__service_message_row = 100

        self.__file_entry_text = None

        self.__service_message = None
        self.__subtitles_list = []
        self.__audio_list = []

    def __create_window(self):
        width = 900
        height = 450
        dimension = f"{width}x{height}"
        self.__root.geometry(dimension)
        self.__root.configure(bg=self.BACKGROUND_COLOR)

    def __set_default_streams(self):
        self.__log_to_console("updating streams!")

    def __add_audio_component(self):
        create_label(
            self.__root,
            "Audio Streams",
            self.__audio_dropdown_row,
            self.DEFAULT_OPTIONS,
        )
        create_dropdown(
            self.__root,
            self.__audio_list,
            self.__audio_dropdown_row,
            lambda x: self.__log_to_console(f"selected {x}"),
        )

    def __add_subtitle_component(self):
        create_label(
            self.__root,
            "Subtitle Streams",
            self.__subtitles_dropdown_row,
            self.DEFAULT_OPTIONS,
        )
        create_dropdown(
            self.__root,
            self.__subtitles_list,
            self.__subtitles_dropdown_row,
            lambda x: self.__log_to_console(f"selected {x}"),
        )

    def create_options(self, options: Iterable[MediaStream]):
        return [f"{index}: {stream.language}" for index, stream in enumerate(options)]

    def __inspect_files(self):
        """function to inspect files and save streams"""
        path = self.__file_entry_text
        try:
            streams = get_media_streams(
                "/Users/richardchan/Macbook/projects/media_utility/images_out/My Hero Academia - UA Heroes Battle.mkv"
            )
        except ServiceError as se:
            self.__log_to_console(se)
            return

        stream_objs = parse_streams(streams)
        self.__subtitles_list = self.create_options(stream_objs["subtitle"])
        self.__audio_list = self.create_options(stream_objs["audio"])
        self.__log_to_console(stream_objs)
        self.__add_audio_component()
        self.__add_subtitle_component()
        create_buttoon(
            self.__root,
            "Set Defaults",
            self.__set_default_streams,
            self.__set_default_streams_row,
            1,
            self.DEFAULT_OPTIONS,
        )

    def __init_gui(self):
        """function to initialize the gui"""
        logger.info("configuring menu")
        self.__create_window()
        # TODO: create a field to enter file path or directory path (dir -> bulk) and (file -> individual)
        create_label(
            self.__root,
            "Enter a File/Directory",
            self.__file_entry_row,
            self.DEFAULT_OPTIONS,
        )
        self.__file_entry_text, _ = create_input_field(
            self.__root, self.__file_entry_row
        )
        # TODO: create a button that will 'read' the file with ffmpeg
        create_buttoon(
            self.__root,
            "Inspect File(s)",
            self.__inspect_files,
            self.__inspect_file_button_row,
            1,
        )

        self.__create_console_message()

    def __log_to_console(self, message):
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


# /Users/richardchan/Macbook/projects/media_utility/images_out/Episode S01E01.mkv
