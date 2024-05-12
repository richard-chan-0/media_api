from src.tkinter.rename_gui import DownloadFilesGui
from src.tkinter.tkinter_functions import *
from src.lib.data_types.service_constants import REZIP_CHAPTERS_TO_VOL_NAME
from src.services.rezip_cbz_files.rezip_chapters_to_vol import (
    rezip_chapters_to_vol,
)
from src.services.rename_media.name_functions import create_jellyfin_comic_name
from src.lib.factories.factories import create_basic_service_args
from tkinter import *
from logging import getLogger
from src.gui_controller import Gui
from src.lib.exceptions.exceptions import RezipChaptersToVolError

logger = getLogger(__name__)


class ReorganizeComicsGui(Gui):

    def __init__(self, root: Tk):
        self.__root = root
        self.__root.title("Reorganize Comics Utility")

        self.__base_gui = DownloadFilesGui(self.__root)
        self.__submit_button_row = 5

        self.__story_name_text = None
        self.__issue_number_text = None

    def __create_story_name_entry(self, root):
        """function to setup entry component for entering path of download folder"""
        create_label(
            root,
            "Comic Name:",
            row=0,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )
        create_label(
            root,
            "Issue Number:",
            row=1,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )

        text, _ = create_input_field(root, 0)
        self.__story_name_text = text
        text2, _ = create_input_field(root, 1)
        self.__issue_number_text = text2

    def __create_rename_button(self, root):
        create_button(
            root=root,
            button_text="Update Files",
            action=self.__update_files,
            row_position=0,
            col_position=2,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )

    def __create_action_buttons(self, root):
        """function to create frame and couple the buttons to the frame on gui"""
        create_label(
            root,
            "Run",
            row=self.__submit_button_row,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )
        frame = create_frame(
            root,
            row=self.__submit_button_row,
            column=COLUMN_COMPONENT,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )
        self.__create_rename_button(frame)

    def __add_service_widgets(self):
        service_frame = create_frame(
            self.__root, row=1, column=0, options=self.__base_gui.DEFAULT_OPTIONS
        )
        self.__create_story_name_entry(service_frame)
        self.__create_action_buttons(service_frame)

    def __update_files(self):
        """function to rename the files"""
        service_args = create_basic_service_args(
            self.__base_gui.directory_in, self.__base_gui.directory_out
        )
        service_args.volume_name = create_jellyfin_comic_name(
            issue=get_widget_value(self.__issue_number_text),
            story_name=get_widget_value(self.__story_name_text),
        )
        is_okay = create_confirmation_window(
            "Confirmation",
            f"Are you sure you want to remap these files to {service_args.volume_name}?",
        )

        if not is_okay:
            self.__base_gui.log_to_console("rename files aborted!")
            return

        logger.info("updating file names in system")
        self.__base_gui.log_to_console("creating volume...!")
        try:
            rezip_chapters_to_vol(service_args)
        except RezipChaptersToVolError as e:
            self.__base_gui.log_to_console(e)

    def __create_window(self):
        width = 900
        height = 450
        dimension = f"{width}x{height}"
        self.__root.geometry(dimension)
        self.__root.configure(bg=DownloadFilesGui.BACKGROUND_COLOR)

    def start(self):
        self.__create_window()
        self.__base_gui.init_gui(REZIP_CHAPTERS_TO_VOL_NAME)
        self.__add_service_widgets()
        self.__root.mainloop()
