from tkinter import Tk, ttk, simpledialog, messagebox, filedialog
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
        self.frame = frame

    def request_open_file_callback(self) -> bool:
        file_loaded_ok = False

        if self.has_the_content_changed():
            user_allows = self.propose_saving()
            if not user_allows:
                return False

        filetypes = (
            ('KryptoTulha files', '*.kryptoTulha'),
            ('All files', '*.*'))
        filename = filedialog.askopenfilename(
            title='Select File to Load',
            initialdir='.',
            filetypes=filetypes)

        try:
            if filename is not None:
                if len(filename) > 0:
                    file_loaded_ok = self.request_password_and_open(filename)

        except Exception as e:
            message = get_message_from_exception(e)
            messagebox.showerror(title='Error opening file',
                                 message=message)
            file_loaded_ok = False

        return file_loaded_ok

    def request_save_file_callback(self) -> bool:
        file_saved_ok = False
        try:
            filetypes = (
                ('KryptoTulha files', '*.kryptoTulha'),
                ('All files', '*.*'))
            filename = filedialog.asksaveasfilename(
                title='Select File to Save',
                initialdir='.',
                defaultextension='.kryptoTulha',
                filetypes=filetypes)

            if filename is not None:
                if len(filename) > 0:
                    file_saved_ok = self.request_password_and_save(filename)

        except Exception as e:
            message = get_message_from_exception(e)
            messagebox.showerror(title='Error saving file',
                                 message=message)
            file_saved_ok = False

        return file_saved_ok

    def request_password_and_open(self, filepath) -> bool:
        base_file_name = os.path.splitext(os.path.basename(filepath))[0]
        user_password = simpledialog.askstring(
            title='Password Required',
            prompt=f'Enter the password for \"{base_file_name}\"',
            show='*')
        if user_password is None:
            return False

        new_compilation, load_error = self.open_file_callback(
            filepath, user_password)

        if new_compilation is None:
            raise RuntimeError(
                f'File {base_file_name} does not contain valid content')

        if load_error is not None:
            messagebox.showwarning(title='Problems opening file',
                                   message=f'{load_error}')

        self.load_new_compilation(new_compilation)
        return True

    def request_password_and_save(self, filepath) -> bool:
        base_file_name = os.path.splitext(os.path.basename(filepath))[0]
        user_password = ask_password_twice_dialog(
            title=f'Saving \'{base_file_name}\'',
            minimun_password_length=RECOMMENDED_MINIMUN_PASSWORD_LENGTH)

        if user_password is None:
            return False

        content = self.content_screen.get_content()
        self.save_file_callback(content, filepath, user_password)

        return True

    def load_new_compilation(self, new_compilation: ItemsCompilation):
        self.content_screen.load_new_compilation(new_compilation)

    def has_the_content_changed(self) -> bool:
        return self.content_screen.has_the_content_changed()

    def propose_saving(self) -> bool:
        """
        Returns True if the user choose to discard or if the user
        choose to save and the save succeeded.
        """
        text = 'Would you like to save the current changes?'
        buttons = [' Save ', ' Cancel ', ' Discard Changes! ']
        save_id = 0
        cancel_id = 1
        discard_id = 2
        user_answer = simpledialog.SimpleDialog(
            master=self.frame,
            text=text,
            buttons=buttons,
            cancel=1,
            title="Save changes?").go()
        if user_answer == cancel_id:
            return False
        if user_answer == discard_id:
            return True
        if user_answer == save_id:
            return self.request_save_file_callback()


def get_message_from_exception(e: Exception):
    if hasattr(e, 'message'):
        return f'{e.message}'
    else:
        return f'{e}'
