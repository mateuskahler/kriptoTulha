from tkinter import Tk, ttk, simpledialog, messagebox
from typing import Callable
import os

from tulha import ItemsCompilation

from .ask_password_twice import ask_password_twice_dialog
from .top_menu import TopMenu
from .content_screen import ContentScreen

RECOMMENDED_MINIMUN_PASSWORD_LENGTH = 6


class MainFrame():
    def __init__(self, root_window: Tk,
                 save_file_callback:
                 Callable[[ItemsCompilation, str, str], None],
                 open_file_callback:
                 Callable[[str, str],
                          tuple[ItemsCompilation | None, str | None]]):
        self.save_file_callback = save_file_callback
        self.open_file_callback = open_file_callback

        frame = ttk.Frame(root_window, padding="2 2 2 2")
        frame.grid(column=0, row=0, sticky="nsew")

        self.top_menu = TopMenu(frame,
                                self.request_save_file_callback,
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
            message = get_message_from_exception(e)
            messagebox.showerror(title='Error opening file',
                                 message=message)

    def request_save_file_callback(self, filepath: str):
        try:
            self.request_password_and_save(filepath)

        except Exception as e:
            message = get_message_from_exception(e)
            messagebox.showerror(title='Error saving file',
                                 message=message)

    def request_password_and_open(self, filepath):
        base_file_name = os.path.splitext(os.path.basename(filepath))[0]
        user_password = simpledialog.askstring(
            title='Password Required',
            prompt=f'Enter the password for \"{base_file_name}\"',
            show='*')
        if user_password is None:
            return

        new_compilation, load_error = self.open_file_callback(
            filepath, user_password)

        if new_compilation is None:
            raise RuntimeError(
                f'File {base_file_name} does not contain valid content')

        if load_error is not None:
            messagebox.showwarning(title='Problems opening file',
                                   message=f'{load_error}')

        self.load_new_compilation(new_compilation)

    def request_password_and_save(self, filepath):
        base_file_name = os.path.splitext(os.path.basename(filepath))[0]
        user_password = ask_password_twice_dialog(
            title=f'Saving \'{base_file_name}\'',
            minimun_password_length=RECOMMENDED_MINIMUN_PASSWORD_LENGTH)

        if user_password is None:
            return

        content = self.content_screen.get_content()

        self.save_file_callback(content, filepath, user_password)

    def load_new_compilation(self, new_compilation: ItemsCompilation):
        self.content_screen.load_new_compilation(new_compilation)


def get_message_from_exception(e: Exception):
    if hasattr(e, 'message'):
        return f'{e.message}'
    else:
        return f'{e}'
