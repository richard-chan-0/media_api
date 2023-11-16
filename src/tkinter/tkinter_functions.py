from tkinter import *
from typing import Iterable, Tuple, Callable

COLUMN_COMPONENT = "1"
COLUMN_BUTTON = "2"

DEFAULT_PADDINGY = 5
DEFAULT_PADDINGX = 5


def get_widget_value(widget: Variable):
    """function to get the value of tkinter variable"""
    return "" if not widget else widget.get()


def create_dropdown(
    root: Tk, options: Iterable[str], row_position
) -> Tuple[Variable, Widget]:
    """function to create tkinter dropdown menu"""
    dropdown_option = StringVar()
    dropdown_option.set(options[0])
    dropdown_menu = OptionMenu(root, dropdown_option, *options)
    dropdown_menu.grid(
        row=row_position,
        column=COLUMN_COMPONENT,
        pady=DEFAULT_PADDINGY,
        sticky=W,
    )
    return (dropdown_option, dropdown_menu)


def create_buttoon(root: Tk, button_text: str, action: Callable, row_position: str):
    """function to create a tkinter button"""
    button = Button(
        root,
        text=button_text,
        default="active",
        command=action,
    )
    button.grid(row=row_position, column=COLUMN_BUTTON, sticky=W)
    return button


def create_label(root: Tk, text: str, row: str, options: dict = {}, column: str = "0"):
    """function to create tkinter label"""
    label = Label(root, text=text, **options)
    label.grid(row=row, column=column, pady=DEFAULT_PADDINGY, sticky=W)
    return label


def destroy_widgets(widgets: Iterable[Widget]):
    """function to destroy widgets"""
    for widget in widgets:
        if widget:
            widget.destroy()


def create_input_field(root: Tk, row_position: str) -> Tuple[Variable, Widget]:
    """function to create tkinter input field"""
    input_field_text = StringVar()
    entry = Entry(root, textvariable=input_field_text)
    entry.grid(row=row_position, column=COLUMN_COMPONENT, sticky=W)
    return (input_field_text, entry)
