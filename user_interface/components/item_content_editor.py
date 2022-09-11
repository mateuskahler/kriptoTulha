import tkinter as tk
from tkinter import Frame, ttk
from typing import Callable

from tulha import ItemsCompilation


class ItemContentEditor:
    def __init__(self, parent: Frame,
                 get_content_callback: Callable[[], ItemsCompilation]):
        self.get_content_callback = get_content_callback

        frame = ttk.Frame(
            parent, padding="5 5 5 5", style="EstiloY.TFrame")

        editable_field = ObservableText(frame, undo=True)
        editable_field.grid(column=0, row=0, sticky='nsew')
        editable_field.config(state='disabled')

        def enter_on_keypad(_):
            self.editable_field.insert(tk.INSERT, '\n')

        def modification_callback(_):
            pass

        editable_field.bind('<<TextModified>>', modification_callback)
        editable_field.bind('<KP_Enter>', enter_on_keypad)

        self.editable_field = editable_field

        frame.grid(column=1, row=0, sticky="nsew")

    def load_item_text(self, item_iid: int | None):
        if item_iid is None:
            self.editable_field.delete('1.0', 'end')
            self.editable_field.config(state='disabled')
        else:
            content = self.get_content_callback().get_item_by_id(item_iid).text

            self.editable_field.config(state='normal')
            self.editable_field.delete('1.0', 'end')
            self.editable_field.insert('end', content)


class ObservableText(tk.Text):
    '''
    Wrapper class to observe text modification
    based on
    https://stackoverflow.com/questions/40617515/python-tkinter-text-modified-callback
    https://stackoverflow.com/questions/65228477/text-doesnt-contain-any-characters-tagged-with-sel-tkinter
    '''

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        # cut/copy commands bound check
        if command == 'get' and \
            (args[0] == 'sel.first' and args[1] == 'sel.last') and \
                not self.tag_ranges('sel'):
            return ''

        # delete commands bound check
        if command == 'delete' and \
            (args[0] == 'sel.first' and args[1] == 'sel.last') and \
                not self.tag_ranges('sel'):
            return None

        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result
