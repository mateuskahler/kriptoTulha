from tkinter import ttk, simpledialog
from typing import Callable


class TopMenu:
    def __init__(self,
                 parent: ttk.Frame,
                 request_save_file_callback: Callable[[], bool],
                 request_open_file_callback: Callable[[], bool],
                 add_item_callback: Callable[[str], None],
                 remove_item_callback: Callable[[], None]
                 ) -> None:
        self.parent = parent
        self.request_save_file_callback = request_save_file_callback
        self.request_open_file_callback = request_open_file_callback
        self.add_item_callback = add_item_callback

        frame = ttk.Frame(parent, padding="5 5 5 0")
        frame.grid(column=0, row=0, sticky="we")

        button_add_item = ttk.Button(
            frame, text='+', command=self.add_item)
        button_add_item.grid(column=0, row=0, sticky="we")

        button_del_item = ttk.Button(frame, text='-',
                                     command=remove_item_callback)
        button_del_item.grid(column=1, row=0, sticky="we")

        empty_space = ttk.Frame(frame)
        empty_space.grid(column=2, row=0, sticky="nsew")

        button_open_file = ttk.Button(frame, text='Load',
                                      command=self.open_file_action)
        button_open_file.grid(column=3, row=0, sticky="we")

        button_save_file = ttk.Button(frame, text='Save',
                                      command=self.save_file_action)
        button_save_file.grid(column=4, row=0, sticky="we")

        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=0)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=0)
        frame.columnconfigure(4, weight=0)
        frame.rowconfigure(0, weight=0)

    def open_file_action(self):
        self.request_open_file_callback()

    def save_file_action(self):
        self.request_save_file_callback()

    def add_item(self):
        title = simpledialog.askstring(
            parent=self.parent,
            title='New Item Title',
            prompt='Provide a title for the new item:')
        if title is None:
            return
        if len(title) == 0:
            return

        self.add_item_callback(title)
