from tkinter import Tk, ttk

from .top_menu import TopMenu
from .content_screen import ContentScreen


class MainFrame:
    def __init__(self, root_window: Tk,
                 save_file_callback: None,
                 open_file_callback: None):
        frame = ttk.Frame(root_window, padding="2 2 2 2")
        frame.grid(column=0, row=0, sticky="nsew")

        self.top_menu = TopMenu(frame,
                                save_file_callback,
                                open_file_callback,
                                None, None)

        self.content_screen = ContentScreen(frame)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=1)
