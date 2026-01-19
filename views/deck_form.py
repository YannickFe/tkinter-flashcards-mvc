from tkinter import Frame, Label, Entry, Button, StringVar


class DeckFormView(Frame):
    """Simple form for deck name/description with save/cancel and inline message."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.title_var = StringVar()
        self.title_label = Label(self, textvariable=self.title_var)
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.name_label = Label(self, text="Name")
        self.name_label.grid(row=1, column=0, padx=10, sticky="w")
        self.name_input = Entry(self)
        self.name_input.grid(row=1, column=1, padx=(0, 20), pady=4, sticky="ew")

        self.desc_label = Label(self, text="Description")
        self.desc_label.grid(row=2, column=0, padx=10, sticky="w")
        self.desc_input = Entry(self)
        self.desc_input.grid(row=2, column=1, padx=(0, 20), pady=4, sticky="ew")

        self.save_btn = Button(self, text="Save")
        self.save_btn.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.cancel_btn = Button(self, text="Cancel")
        self.cancel_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.message_var = StringVar()
        self.message_label = Label(self, textvariable=self.message_var, fg="red")
        self.message_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def set_title(self, title: str) -> None:
        self.title_var.set(title)

    def set_message(self, message: str) -> None:
        self.message_var.set(message)

    def clear_inputs(self) -> None:
        self.name_input.delete(0, "end")
        self.desc_input.delete(0, "end")
