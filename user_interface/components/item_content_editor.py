import tkinter as tk
from tkinter import Frame, ttk
from typing import Callable

from tulha import ItemsCompilation


class ItemContentEditor:
    def __init__(self, parent: Frame,
                 get_content_callback: Callable[[], ItemsCompilation],
                 item_edited_callback):
        self.get_content_callback = get_content_callback
        self.item_edited_callback = item_edited_callback

        frame = ttk.Frame(
            parent, padding="5 5 5 5", style="EstiloY.TFrame")

        editable_field = ObservableText(frame, undo=True)
        editable_field.grid(column=0, row=0, sticky='nsew')
        editable_field.config(state='disabled')

        def enter_on_keypad(_):
            self.editable_field.insert(tk.INSERT, '\n')

        editable_field.bind('<<TextModified>>', self.item_modified)
        editable_field.bind('<KP_Enter>', enter_on_keypad)

        self.editable_field = editable_field

        frame.grid(column=1, row=0, sticky="nsew")

    def load_item_text(self, item_iid: int | None):
        # unbind text modification event, so the load does not trigger
        # unnecessary callbacks (the load modifies the content)
        self.editable_field.unbind('<<TextModified>>')
        self.editable_field.config(state='normal')

        if item_iid is None:
            self.editable_field.delete('1.0', 'end')
            self.editable_field.config(state='disabled')
        else:
            content = self.get_content_callback().get_item_by_id(item_iid).text
            self.editable_field.delete('1.0', 'end')
            self.editable_field.insert('1.0', content)

        self.editable_field.edit_reset()
        self.editable_field.bind('<<TextModified>>', self.item_modified)

    def item_modified(self, _):
        content = self.editable_field.get("1.0", "end-1c")
        self.item_edited_callback(content)


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
        try:
            result = self.tk.call(cmd)
        except Exception:
            result = None
        else:
            if command in ("insert", "delete", "replace"):
                self.event_generate("<<TextModified>>")
        finally:
            return result
