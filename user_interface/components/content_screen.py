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
        self.content_frame = ItemContentEditor(
            frame, self.get_content, self.item_edited)

        self.content = ItemsCompilation()

    def get_content(self):
        return self.content

    def load_new_compilation(self, compilation: ItemsCompilation):
        self.content = compilation
        self.items_navigator.reset_visibility()

    def item_selected(self, item_iid: int | None):
        self.content_frame.load_item_text(item_iid)

    def item_edited(self, new_content: str):
        item_iid = self.items_navigator.get_selected_item_iid()
        if item_iid is not None:
            self.content.change_text_of_item_by_id(item_iid, new_content)
