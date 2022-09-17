import unicodedata

import tkinter as tk
from tkinter import StringVar, ttk, font
from typing import Callable
from thefuzz import fuzz

from tulha import ItemsCompilation

# Search biased towards latin alphabet
# (my personal use case, English and Portuguese)
SEARCH_BIAS_LATIN = True


class ItemsNavigator:
    def __init__(self, parent: ttk.Frame,
                 get_content_callback: Callable[[], ItemsCompilation],
                 has_item_been_modified_callback: Callable[[int], bool],
                 item_selected_callback: Callable[[int | None], None]):
        frame = ttk.Frame(parent, padding="0 5 5 5")
        frame.grid(column=0, row=0, sticky="nsew")

        self.titles_list = ItemsTitleList(
            frame, get_content_callback,
            has_item_been_modified_callback,
            item_selected_callback)
        self.serch_bar = ItemsSearchBar(
            frame,
            self.titles_list.update_ordering_criteria)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=1)

    def reset_visibility(self):
        self.serch_bar.clear_search()
        self.titles_list.update_visible_list()
        self.titles_list.tag_changed_items()

    def force_selection(self, item_iid: int):
        self.titles_list.force_selection(item_iid)

    def get_selected_item_iid(self) -> int | None:
        return self.titles_list.get_selected_item_iid()


class ItemsSearchBar:
    def __init__(self, parent: ttk.Frame,
                 update_search_text_callback: Callable[[str], None]):
        self.update_search_text_callback = update_search_text_callback

        frame = ttk.Frame(parent, padding="0 0 0 0")
        frame.grid(column=0, row=0, sticky="nsew")

        search_titles_label = ttk.Label(frame, text='Search ', anchor='e')
        search_titles_label.grid(column=0, row=0, sticky="nsew")

        self.filter_text = StringVar()
        search_field = ttk.Entry(
            frame, textvariable=self.filter_text)
        self.filter_text.trace_add(
            'write', self.search_modified)

        search_field.grid(column=1, row=0, sticky="nsew")
        self.search_field = search_field

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

    def clear_search(self):
        self.search_field.delete(0, 'end')

    def search_modified(self, *_):
        search_value = self.filter_text.get()
        self.update_search_text_callback(search_value)


class ItemsTitleList:
    def __init__(self, parent: ttk.Frame,
                 get_content_callback: Callable[[], ItemsCompilation],
                 has_item_been_modified_callback: Callable[[int], bool],
                 item_selected_callback: Callable[[int | None], None]):
        self.get_content_callback = get_content_callback
        self.has_item_been_modified = has_item_been_modified_callback
        self.item_selected_callback = item_selected_callback
        self.ordering_text = ''

        self.iid_last_selected_item: int | None = None

        frame = ttk.Frame(parent, padding="0 5 0 0")
        frame.grid(column=0, row=1, sticky="nsew")

        titles_list = self.create_title_list(frame)

        titles_list.bind('<<TreeviewSelect>>',
                         self.item_selected)
        titles_list.column('#0', width=0, stretch=tk.NO)

        titles_list.grid(column=0, row=0, sticky='nsew')

        self.titles_list = titles_list

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        frame.rowconfigure(0, weight=1)

    def item_selected(self, _):
        iid = self.get_selected_item_iid()
        if iid is not None:
            self.iid_last_selected_item = iid
        self.item_selected_callback(iid)

    def force_selection(self, item_iid: int):
        self.titles_list.selection_set(f'{item_iid}')

    def get_selected_item_iid(self) -> int | None:
        selected_items = self.titles_list.selection()
        if len(selected_items) == 0:
            return None
        else:
            return int(selected_items[0])

    def update_visible_list(self):
        content = self.get_content_callback()

        self.titles_list.delete(*self.titles_list.get_children())

        existing_ids = content.existing_ids()
        existing_ids.sort()

        for i in existing_ids:
            item = content.get_item_by_id(i)
            self.titles_list.insert(parent='', index='end', iid=f'{i}',
                                    text=f'iid{i}',
                                    values=(item.title, ))

        self.sort_items_by_search_text()

    def tag_changed_items(self):
        for item_iid in self.get_content_callback().existing_ids():
            is_modified = self.has_item_been_modified(item_iid)
            if is_modified:
                self.titles_list.item(f'{item_iid}', tags='content_modified')
            else:
                self.titles_list.item(f'{item_iid}', tags='')

    def create_title_list(self, parent_frame):
        titles_list = ttk.Treeview(parent_frame, selectmode="browse")

        titles_list['columns'] = ('titles')
        titles_list.heading(0, text='Items')
        titles_list_scroll = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL,
                                           command=titles_list.yview)
        titles_list_scroll.grid(column=1, row=0, sticky='ns')
        titles_list.configure(yscroll=titles_list_scroll.set)

        ttk_style = ttk.Style()
        default_font_name = ttk_style.configure(".", "font")
        item_modified_font = font.Font(font=font.nametofont(default_font_name))
        item_modified_font.config(slant='italic', weight='bold')

        titles_list.tag_configure(
            'content_modified', font=item_modified_font)

        font_linespace = item_modified_font.metrics('linespace')
        ttk_style.configure('Treeview', rowheight=int(font_linespace*1.1))

        return titles_list

    def update_ordering_criteria(self, search_text: str):
        ordering_text = self.ordering_text = unicodedata.normalize(
            'NFKD', search_text).casefold()

        if SEARCH_BIAS_LATIN:
            ordering_text = ordering_text.encode(
                encoding='ascii', errors='ignore').decode(encoding='utf-8')

        self.ordering_text = ordering_text

        self.sort_items_by_search_text()

    def sort_items_by_search_text(self):
        try:
            items_list = [(self.titles_list.set(i), i)
                          for i in self.titles_list.get_children('')]

            items_list.sort(
                key=lambda item: self.rate_title_similarity(*item),
                reverse=True)

            for position, (_, item_id) in enumerate(items_list):
                self.titles_list.move(f'{item_id}', '', position)

        except Exception:
            pass

    def rate_title_similarity(self, item_values, item_id) -> int:
        try:
            ordering_text = self.ordering_text
            if len(ordering_text) > 0:
                title = unicodedata.normalize(
                    'NFKD', item_values['titles']).casefold()

                if SEARCH_BIAS_LATIN:
                    title = title.encode(
                        encoding='ascii', errors='ignore').decode(
                            encoding='utf-8')

                return fuzz.partial_ratio(title, ordering_text)
            else:
                return int(item_id)

        except Exception:
            return 0
