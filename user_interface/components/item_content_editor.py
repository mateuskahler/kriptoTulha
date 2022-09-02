import tkinter as tk
from tkinter import Frame, ttk


class ItemContentEditor:
    def __init__(self, parent: Frame):
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

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        frame.grid(column=1, row=0, sticky="nsew")


class ObservableText(tk.Text):
    '''
    Wrapper class to observe text modification
    based on
    https://stackoverflow.com/questions/40617515/python-tkinter-text-modified-callback
    '''

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result
