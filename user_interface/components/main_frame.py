from tkinter import Tk, ttk, simpledialog, messagebox
from typing import Callable
import os

from tulha import ItemsCompilation

from .top_menu import TopMenu
from .content_screen import ContentScreen


class MainFrame():
    def __init__(self, root_window: Tk,
                 save_file_callback: None,
                 open_file_callback:
                 Callable[[str, str],
                          tuple[ItemsCompilation | None, str | None]]):
        self.open_file_callback = open_file_callback

        frame = ttk.Frame(root_window, padding="2 2 2 2")
        frame.grid(column=0, row=0, sticky="nsew")

        self.top_menu = TopMenu(frame,
                                save_file_callback,
                                self.request_open_file_callback,
                                None, None)

        self.content_screen = ContentScreen(frame)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=1)

    def request_open_file_callback(self, filepath: str):
        try:
            self.request_password_and_open(filepath)

        except Exception as e:
            if hasattr(e, 'message'):
                message = e.message
            else:
                message = f'{e}'
            messagebox.showerror(title='Error opening file',
                                 message=f'{message}')

    def request_password_and_open(self, filepath):
        base_file_name = os.path.splitext(os.path.basename(filepath))[0]
        user_password = simpledialog.askstring(
            title='Password Required',
            prompt=f'Enter the password for \"{base_file_name}\"',
            show='*')
        if user_password is None:
            return

        new_compilation, errors = self.open_file_callback(
            filepath, user_password)

        if new_compilation is None:
            raise RuntimeError(
                f'File {base_file_name} does not contain valid content')

        self.load_new_compilation(new_compilation, errors)

    def load_new_compilation(self, new_compilation: ItemsCompilation,
                             errors: str | None):
        if errors is not None:
            messagebox.showwarning(title='Problems opening file',
                                   message=f'{errors}')

        self.content_screen.load_new_compilation(new_compilation)
