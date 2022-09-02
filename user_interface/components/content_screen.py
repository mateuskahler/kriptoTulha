from tkinter import Frame, ttk

from .itens_navigation import ItemsNavigator
from .item_content_editor import ItemContentEditor


class ContentScreen:
    def __init__(self, parent: Frame) -> None:
        frame = ttk.Frame(parent, padding="5 0 5 5")
        frame.grid(column=0, row=1, sticky="nsew")

        self.items_navigator = ItemsNavigator(frame)
        self.content_frame = ItemContentEditor(frame)

        frame.columnconfigure(0, weight=2)
        frame.columnconfigure(1, weight=3)
        frame.rowconfigure(0, weight=1)
