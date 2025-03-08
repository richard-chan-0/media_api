from src.tkinter.rename_gui import DownloadFilesGui
from src.tkinter.tkinter_functions import *
from src.services.rename_media.rename_media import rename_files
from src.lib.service_constants import RENAME_FILES_TO_JELLY_COMICS
from src.lib.factories.factories import create_basic_service_args
from tkinter import *
from logging import getLogger
from json import dumps

logger = getLogger(__name__)


class RenameComicsGui:
    def __init__(self, root: Tk):
        self.__root = root
        self.__root.title("Rename Comics Utility")
        self.__base_gui = DownloadFilesGui(root)

        self.__story_name_text = None
        self.__story_name_row = 1
        self.__submit_button_row = 2

        self.__rename_mapping = None

    def __create_story_name_entry(self):
        """function to setup entry component to enter name for comic functions"""
        story_frame = create_frame(
            self.__root, self.__story_name_row, 0, self.__base_gui.DEFAULT_OPTIONS
        )
        create_label(
            story_frame,
            "Enter the Story Name:",
            row=0,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )
        text, _ = create_input_field(story_frame, 0)
        self.__story_name_text = text

    def __create_rename_mapping(self):
        """function that runs rename methods"""
        logger.info("retrieving service configurations")
        service_args = create_basic_service_args(
            self.__base_gui.directory_in, self.__base_gui.directory_out
        )
        service_args.story = get_widget_value(self.__story_name_text)
        logger.info("creating name mapping")

        self.__rename_mapping = self.__base_gui.service(service_args)
        mapping = dumps(self.__rename_mapping, indent=4)
        self.__base_gui.log_to_console(mapping)

    def __create_submit_button(self, root):
        """function to create button for generating name mapping"""
        create_button(
            root,
            button_text="Create New File Names",
            action=self.__create_rename_mapping,
            row_position=0,
            col_position=1,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )

    def __create_rename_button(self, root):
        create_button(
            root=root,
            button_text="Update Files",
            action=self.__update_files,
            row_position=0,
            col_position=2,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )

    def __create_action_buttons(self):
        """function to create frame and couple the buttons to the frame on gui"""
        frame = create_frame(
            self.__root,
            row=self.__submit_button_row,
            column=0,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )
        create_label(
            frame,
            "Run",
            row=0,
            options=self.__base_gui.DEFAULT_OPTIONS,
        )
        self.__create_submit_button(frame)
        self.__create_rename_button(frame)

    def __add_service_widgets(self):
        self.__create_story_name_entry()
        self.__create_action_buttons()

    def __update_files(self):
        """function to rename the files"""
        is_okay = create_confirmation_window(
            "Confirmation", "Are you sure you want to rename these files?"
        )

        if not is_okay:
            self.__base_gui.log_to_console("rename files aborted!")
            return

        logger.info("updating file names in system")
        self.__base_gui.log_to_console("renaming files!")
        rename_files(rename_mapping=self.__rename_mapping)

    def start(self):
        self.__base_gui.init_gui(RENAME_FILES_TO_JELLY_COMICS)
        self.__add_service_widgets()
        self.__root.mainloop()
