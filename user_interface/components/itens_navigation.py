from copy import copy
import tkinter as tk
from tkinter import Frame, StringVar, ttk, font
from typing import Callable

from tulha import ItemsCompilation


class ItemsNavigator:
    def __init__(self, parent: Frame,
                 get_content_callback: Callable[[], ItemsCompilation],
                 has_item_been_modified_callback: Callable[[int], bool],
                 item_selected_callback: Callable[[int | None], None]):
        frame = ttk.Frame(parent, padding="0 5 5 5")
        frame.grid(column=0, row=0, sticky="nsew")

        self.serch_bar = ItemsSearchBar(frame)
        self.titles_list = ItemsTitleList(
            frame, get_content_callback,
            has_item_been_modified_callback,
            item_selected_callback)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=1)

    def reset_visibility(self):
        self.serch_bar.clear_search()
        self.titles_list.update_visible_list()

    def get_selected_item_iid(self) -> int | None:
        return self.titles_list.get_selected_item_iid()


class ItemsSearchBar:
    def __init__(self, parent: Frame):
        frame = ttk.Frame(parent, padding="0 0 0 0")
        frame.grid(column=0, row=0, sticky="nsew")

        search_titles_label = ttk.Label(frame, text='Search ', anchor='e')
        search_titles_label.grid(column=0, row=0, sticky="nsew")

        self.filter_text = StringVar()
        search_field = tk.Entry(
            frame, textvariable=self.filter_text)
        self.filter_text.trace_add(
            'write', lambda *args: self.atualiza_lista_visível())

        search_field.grid(column=1, row=0, sticky="nsew")
        self.search_field = search_field

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

    def clear_search(self):
        self.search_field.delete(0, 'end')


class ItemsTitleList:
    def __init__(self, parent: Frame,
                 get_content_callback: Callable[[], ItemsCompilation],
                 has_item_been_modified_callback: Callable[[int], bool],
                 item_selected_callback: Callable[[int | None], None]):
        self.get_content_callback = get_content_callback
        self.has_item_been_modified = has_item_been_modified_callback
        self.item_selected_callback = item_selected_callback

        self.iid_last_selected_item: int | None = None

        frame = ttk.Frame(parent, padding="0 5 0 0")
        frame.grid(column=0, row=1, sticky="nsew")

        titles_list = ttk.Treeview(frame, selectmode="browse")
        titles_list['columns'] = ('titles')
        titles_list.heading(0, text='Items')
        titles_list_scroll = tk.Scrollbar(frame, orient=tk.VERTICAL,
                                          command=titles_list.yview)
        titles_list_scroll.grid(column=1, row=0, sticky='ns')
        titles_list.configure(yscroll=titles_list_scroll.set)

        italic_font = copy(font.nametofont('TkTextFont'))
        italic_font.config(slant='italic', weight='bold')
        titles_list.tag_configure(
            'content_modified', font=italic_font)

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

    def tag_changed_items(self):
        for item_iid in self.get_content_callback().existing_ids():
            is_modified = self.has_item_been_modified(item_iid)
            if is_modified:
                self.titles_list.item(f'{item_iid}', tags='content_modified')
            else:
                self.titles_list.item(f'{item_iid}', tags='')
