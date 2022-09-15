from tkinter import Toplevel, ttk


class AskTwice():
    """
    A simple widget (despite the long source code) that offers two fields asking
    for a password. Saves the passwords as the 'output' field if both inputs are
    valid and equal.

    Apart from the buttons, the widget is navigable by <Tab> and <Enter>, and
    cancelable by <Esc>.
    """

    def __init__(self, parent, title: str, minimun_password_length: int):
        self.minimun_password_length = minimun_password_length
        self.output: None | str = None
        self.parent = parent

        top_level = Toplevel(None)
        top_level.grid_columnconfigure(0, weight=1)
        top_level.grid_rowconfigure(0, weight=1)
        top_level.bind('<Escape>', lambda *_: self.cancel_and_quit())

        frame = ttk.Frame(top_level)
        frame.grid(column=0, row=0, sticky='nsew')

        # row 0
        emptySpace = ttk.Label(frame)
        emptySpace.grid(row=0, column=0, columnspan=5, sticky="nsew")

        # row 1
        emptySpace = ttk.Label(frame)
        emptySpace.grid(row=1, column=0, columnspan=1, sticky="nsew")
        emptySpace = ttk.Label(frame)
        emptySpace.grid(row=1, column=2, columnspan=1, sticky="nsew")
        emptySpace = ttk.Label(frame)
        emptySpace.grid(row=1, column=4, columnspan=1, sticky="nsew")

        input1Label = ttk.Label(frame, text="Choose a Password:")
        input1Label.configure(anchor='e')
        input1Label.grid(row=1, column=1, columnspan=1, sticky="nsew")

        input1_entry = ttk.Entry(frame, show='*')
        input1_entry.grid(row=1, column=3, columnspan=1, sticky="ew")
        input1_entry.bind(
            '<Return>', lambda *_: self.input1_entry.tk_focusNext().focus())
        self.input1_entry = input1_entry

        # row 2
        emptySpace = ttk.Label(frame)
        emptySpace.grid(row=2, column=0, columnspan=5, sticky="ew")

        # row 3
        emptySpace = ttk.Label(frame)
        emptySpace.grid(row=3, column=0, columnspan=1, sticky="nsew")
        emptySpace = ttk.Label(frame)
        emptySpace.grid(row=3, column=2, columnspan=1, sticky="nsew")
        emptySpace = ttk.Label(frame)
        emptySpace.grid(row=3, column=4, columnspan=1, sticky="nsew")

        input2Label = ttk.Label(frame, text="Repeat the Password:")
        input2Label.configure(anchor='e')
        input2Label.grid(row=3, column=1, columnspan=1, sticky="ew")

        input2_entry = ttk.Entry(frame, show='*')
        input2_entry.grid(row=3, column=3, columnspan=1, sticky="ew")
        input2_entry.bind(
            '<Return>', lambda *_: self.try_to_output())
        self.input2_entry = input2_entry

        # row 4
        validation_label = ttk.Label(frame, text='')
        validation_label.configure(anchor='center')
        validation_label.grid(row=4, column=0, columnspan=5, sticky="ew")
        self.validation_label = validation_label

        # row 5
        emptySpace = ttk.Label(frame)
        emptySpace.grid(row=5, column=0, columnspan=1, sticky="nsew")
        emptySpace = ttk.Label(frame)
        emptySpace.grid(row=5, column=2, columnspan=1, sticky="nsew")
        emptySpace = ttk.Label(frame)
        emptySpace.grid(row=5, column=4, columnspan=1, sticky="nsew")

        butOk = ttk.Button(
            frame, text="Ok", command=lambda *_: self.try_to_output())
        butOk.bind('<Return>', lambda *_: self.try_to_output())
        butOk.grid(row=5, column=1, sticky="nsew")

        butCancel = ttk.Button(frame, text="Cancel",
                               command=lambda *_: self.cancel_and_quit())
        butCancel.bind('<Return>', lambda *_: self.cancel_and_quit())
        butCancel.grid(row=5, column=3, sticky="nsew")

        # row 6
        emptySpace = ttk.Label(frame)
        emptySpace.grid(row=6, column=0, columnspan=5, sticky="ew")

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=2)
        frame.grid_columnconfigure(4, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_rowconfigure(3, weight=1)
        frame.grid_rowconfigure(4, weight=1)
        frame.grid_rowconfigure(5, weight=1)
        frame.grid_rowconfigure(6, weight=1)

        top_level.title(title)
        top_level.attributes('-topmost', True)

        top_level.protocol("WM_DELETE_WINDOW",
                           lambda *_: self.cancel_and_quit())

        self.top_level = top_level

        self.center_this_window()

        top_level.focus()
        input1_entry.focus()
        top_level.grab_set()

        self.top_level.wait_window(self.top_level)

    def try_to_output(self):
        if self.check_input_validity():
            self.validation_label.configure(text='Ok')
            self.output = self.input1_entry.get()
            self.top_level.destroy()

    def check_input_validity(self) -> bool:
        input1_value = self.input1_entry.get()
        input2_value = self.input2_entry.get()
        if len(input1_value) < self.minimun_password_length:
            self.validation_label.configure(text='password too small')
            self.reset_password_fields()
            return False
        elif input1_value != input2_value:
            self.validation_label.configure(text='passwords do not match')
            self.reset_password_fields()
            return False
        else:
            return True

    def reset_password_fields(self):
        self.input1_entry.delete(0, 'end')
        self.input2_entry.delete(0, 'end')
        self.input1_entry.focus()

    def cancel_and_quit(self):
        self.output = None
        self.top_level.destroy()

    def center_this_window(self):
        try:
            self.top_level.update_idletasks()
            x_start = int(self.parent.winfo_rootx())
            y_start = int(self.parent.winfo_rooty())
            x_avail = int(self.parent.winfo_width())
            y_avail = int(self.parent.winfo_height())
            x_needed = int(self.top_level.winfo_width())
            y_needed = int(self.top_level.winfo_height())

            x_position = int(x_start + (x_avail/2) - (x_needed/2))
            y_position = int(y_start + (y_avail/2) - (y_needed/2))

            self.top_level.geometry(f'+{x_position}+{y_position}')
        except Exception:
            pass


def ask_password_twice_dialog(parent, title: str,
                              minimun_password_length: int) -> str | None:
    """
    Opens a windows that asks for a password input in two fields.

    Returns the password as a string, or None if the user cancelled.
    """
    ask_window = AskTwice(parent, title, minimun_password_length)
    return ask_window.output
