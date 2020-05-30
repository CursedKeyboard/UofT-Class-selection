from tkinter import Tk
from tkinter.ttk import Frame
import tkinter as tk
from typing import List, Tuple
from functools import partial


def popup_duplicate_program():
    window = tk.Toplevel()

    label = tk.Label(window, text="This program already exists! Please add another program!")
    label.pack(fill='x', padx=40, pady=5)

    continue_button = tk.Button(window, text="Okay", command=window.destroy)
    continue_button.pack(fill='x')


def take_user_input(choices: List[Tuple[int, str]]) -> str:
    user_input_window = tk.Toplevel()
    label = tk.Label(master=user_input_window, text="Choose one of the following choices!")
    label.grid()
    courses = list()

    def set_class_choice(window: tk.Toplevel, chosen: Tuple[int, str], add_choice: list, lock: tk.IntVar):
        add_choice.append(chosen[1])
        window.destroy()
        lock.set(1)

    # var is required to wait until a button has been clicked
    var = tk.IntVar()
    for choice in choices:
        button_choice = tk.Button(master=user_input_window, text="{0}".format(choice[1]),
                                  command=partial(set_class_choice, user_input_window, choice, courses, var))
        button_choice.grid(row=1 + choice[0], column=0)

    user_input_window.grid_slaves(row=1)[0].waitvar(var)

    return courses


def special_message(message: str):
    special_message_window = tk.Toplevel()
    inform_label = tk.Label(master=special_message_window,
                            text="There are certain important messages for your program!")
    inform_label.pack(side='top')

    message_label = tk.Label(master=special_message_window, text=message)
    message_label.pack(side='top')

    continue_button = tk.Button(master=special_message_window, text="Okay", command=special_message_window.destroy)
    continue_button.pack(side='top')


def popup_duplicate_course(course_name: str):
    window = tk.Toplevel()

    label = tk.Label(window, text="{0} has already been added".format(course_name))
    label.pack(fill='x', padx=40, pady=5)

    continue_button = tk.Button(window, text="Okay", command=window.destroy)
    continue_button.pack(fill='x')


def course_not_found_popup(course_name: str):
    window = tk.Toplevel()

    label = tk.Label(window, text="The following course/courses no longer exists: {0}".format(course_name))
    label.pack()

    continue_button = tk.Button(window, text="Okay", command=window.destroy)
    continue_button.pack(fill='x')