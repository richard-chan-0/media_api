from tkinter import *
from src.services import get_services


class RenameGui:
    COLUMN_COMPONENT = "1"
    DEFAULT_PADDINGY = 5
    DEFAULT_PADDINGX = 5

    def __init__(self):
        self.__root = Tk()
        self.__submit_button_row = 3
        self.__submit_button = None
        self.__service_message = None

        self.__story_name_row = 2
        self.__story_name_entry = None

        self.__numeric_dropdown_row = 0
        self.__numeric_dropdown = None
        self.__numeric_click = None

        self.__service_dropdown_row = 1
        self.__service_dropdown = None
        self.__service_click = None

    def create_window(self):
        width = 700
        height = 250
        dimension = f"{width}x{height}"
        self.__root.geometry(dimension)

    def create_numeric_dropdown(self):
        self.create_label(
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

    def create_service_dropdown(self, options):
        self.create_label("Select Service", self.__service_dropdown_row)
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

    def create_submit_button(self):
        self.__submit_button = Button(
            self.__root, text="Rename!", default="active", command=self.show
        )
        self.__submit_button.grid(
            row=self.__submit_button_row,
            column=self.COLUMN_COMPONENT,
            pady=self.DEFAULT_PADDINGY,
            sticky=W,
        )

    def create_label(self, text, row, column="0"):
        label = Label(self.__root, text=text)
        label.grid(row=row, column=column, pady=self.DEFAULT_PADDINGY, sticky=W)
        return label

    def create_story_name_entry(self):
        self.create_label("Enter the Story Name:", row=self.__story_name_row)
        self.__story_name_entry = Entry(self.__root)
        self.__story_name_entry.grid(
            row=self.__story_name_row, column=self.COLUMN_COMPONENT, sticky=W
        )

    def config(self):
        self.create_window()

        services = get_services()
        options = [service for service in services.keys() if "rename" in service]
        self.create_service_dropdown(options)
        self.create_story_name_entry()
        self.create_numeric_dropdown()
        self.create_submit_button()
        self.create_label("Submit Button", row=self.__submit_button_row)

    def start(self):
        self.config()
        self.__root.mainloop()

    def show(self):
        requested_service = self.__service_click.get()
        message = f"starting {requested_service} service: renaming!"
        self.__service_message = self.create_label(message, row=5, column=1)
        self.__service_message.config(text=message)
