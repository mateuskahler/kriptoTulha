from tulha import ItemsCompilation

from typing import Callable
import tkinter as tk

from .components import MainFrame


class KryptoTulhaUserInterface:
    """
    Graphical application to edit a ItemsCompilation
    """

    def __init__(self,
                 save_file_callback: None,
                 open_file_callback:
                 Callable[[str, str],
                          tuple[ItemsCompilation | None, str | None]]):
        """
        initial_state: ItemsCompilation to launch the application with
        save_file_callback: will be called when user requests to save
        open_file_callback: will be called when user requests to open a file.
            Receives the path and the password as arguments.

        After creating the instance, call the "assume_control" method
        to pass the flow of the program to the graphical interface.
        """
        self.original_state = None
        self.current_state = None
        self.save_file_callback = save_file_callback
        self.open_file_callback = open_file_callback

        self.open_dialog = None

    def assume_control(self):
        """
        Creates the graphical interface and takes control of the program until
        the user closes it.
        """
        window_root = tk.Tk()

        window_root.title('KryptoTulha')

        self.main_frame = MainFrame(
            window_root, self.save_file_callback, self.open_file_callback)

        window_root.columnconfigure(0, weight=1)
        window_root.rowconfigure(0, weight=1)

        window_root.protocol(
            'WM_DELETE_WINDOW', self.tries_to_close)

        self.window_root = window_root
        self.window_root.mainloop()

    def tries_to_close(self):
        if self.open_dialog is None:
            self.window_root.destroy()
