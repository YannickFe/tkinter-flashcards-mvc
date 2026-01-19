from tkinter import Button, Frame, Label, Listbox, Scrollbar, StringVar


class DeckListView(Frame):
    """List decks with grouped actions for CRUD and navigation."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header = Label(self, text="Your Decks")
        self.header.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        self.deck_list = Listbox(self, exportselection=False)
        self.deck_list.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.deck_list.yview)
        self.deck_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=2, sticky="ns")

        self.create_btn = Button(self, text="New Deck")
        self.create_btn.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.edit_btn = Button(self, text="Edit Deck")
        self.edit_btn.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        self.open_btn = Button(self, text="Open Deck")
        self.open_btn.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.delete_btn = Button(self, text="Delete Deck")
        self.delete_btn.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        self.back_btn = Button(self, text="Back")
        self.back_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.message_var = StringVar()
        self.message_label = Label(self, textvariable=self.message_var, fg="red")
        self.message_label.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    def set_message(self, message: str) -> None:
        self.message_var.set(message)

    def clear_inputs(self) -> None:
        pass
