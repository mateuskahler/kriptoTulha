from tkinter import Frame, ttk

from tulha import ItemsCompilation

from .itens_navigation import ItemsNavigator
from .item_content_editor import ItemContentEditor


class ContentScreen:
    def __init__(self, parent: Frame) -> None:
        frame = ttk.Frame(parent, padding="5 0 5 5")
        frame.grid(column=0, row=1, sticky="nsew")

        self.items_navigator = ItemsNavigator(
            frame, self.get_content, self.item_selected)
        self.content_frame = ItemContentEditor(frame, self.get_content)

        self.content = ItemsCompilation()

    def get_content(self):
        return self.content

    def load_new_compilation(self, compilation: ItemsCompilation):
        self.content = compilation
        self.items_navigator.reset_visibility()

    def item_selected(self, item_iid: int | None):
        self.content_frame.load_item_text(item_iid)
