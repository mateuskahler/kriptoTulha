import tkinter as tk
from tkinter import Frame, StringVar, ttk, font


class ItemsNavigator:
    def __init__(self, parent: Frame):
        frame = ttk.Frame(parent, padding="0 5 5 5")
        frame.grid(column=0, row=0, sticky="nsew")

        self.serch_bar = ItemsSearchBar(frame)
        self.titles_list = ItemsTitleList(frame)

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=0)
        frame.rowconfigure(1, weight=1)


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


class ItemsTitleList:
    def __init__(self, parent: Frame):
        self.callback_de_item_selecionado = None

        frame = ttk.Frame(parent, padding="0 5 0 0")
        frame.grid(column=0, row=1, sticky="nsew")

        titles_list = ttk.Treeview(frame, selectmode="browse")
        titles_list['columns'] = ('título')
        titles_list.heading(0, text='Item')
        titles_list_scroll = tk.Scrollbar(frame, orient=tk.VERTICAL,
                                          command=titles_list.yview)
        titles_list_scroll.grid(column=1, row=0, sticky='ns')
        titles_list.configure(yscroll=titles_list_scroll.set)
        titles_list.tag_configure('modificado', font=font.Font(slant='italic'))

        titles_list.bind('<<TreeviewSelect>>',
                         self.callback_de_item_selecionado)
        titles_list.column('#0', width=0, stretch=tk.NO)

        titles_list.grid(column=0, row=0, sticky='nsew')

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)
        frame.rowconfigure(0, weight=1)
