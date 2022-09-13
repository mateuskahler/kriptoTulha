from copy import deepcopy
from tkinter import ttk

from tulha import ItemsCompilation

from .itens_navigation import ItemsNavigator
from .item_content_editor import ItemContentEditor


class ContentScreen:
    def __init__(self, parent: ttk.Frame) -> None:
        frame = ttk.Frame(parent, padding="5 0 5 5")
        frame.grid(column=0, row=1, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        self.items_navigator = ItemsNavigator(
            frame, self.get_content, self.has_item_been_modified,
            self.item_selected)
        self.content_frame = ItemContentEditor(
            frame, self.get_content, self.item_edited)

        self.original_content = ItemsCompilation()
        self.content = ItemsCompilation()

    def get_content(self):
        return self.content

    def get_original_content(self):
        return self.original_content

    def overwrite_original_content_with_current(self):
        """
        Useful after saving files, when the temporary content is promoted to be
        considered the original reference.
        """
        self.original_content = deepcopy(self.content)
        self.items_navigator.titles_list.tag_changed_items()

    def load_new_compilation(self, compilation: ItemsCompilation):
        self.original_content = deepcopy(compilation)
        self.content = compilation
        self.items_navigator.reset_visibility()

    def item_selected(self, item_iid: int | None):
        self.content_frame.load_item_text(item_iid)

    def item_edited(self, new_content: str):
        item_iid = self.items_navigator.get_selected_item_iid()
        if item_iid is not None:
            self.content.change_text_of_item_by_id(item_iid, new_content)
        self.items_navigator.titles_list.tag_changed_items()

    def has_the_content_changed(self) -> bool:
        current_iids = self.content.existing_ids()
        original_iids = self.original_content.existing_ids()

        any_modified = any(self.has_item_been_modified(iid)
                           for iid in current_iids)
        any_missing = any(iid not in current_iids for iid in original_iids)
        any_new = any(iid not in original_iids for iid in current_iids)

        return any_modified or any_missing or any_new

    def has_item_been_modified(self, item_iid: int) -> bool:
        try:
            original_item = self.original_content.get_item_by_id(item_iid)
            current_item = self.content.get_item_by_id(item_iid)

            title_changed = original_item.title != current_item.title
            text_changed = original_item.text != current_item.text

            return title_changed or text_changed

        except KeyError:
            return True
