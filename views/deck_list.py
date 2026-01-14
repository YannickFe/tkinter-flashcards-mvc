from tkinter import Button, Entry, Frame, Label, Listbox, Scrollbar, StringVar


class DeckListView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.header = Label(self, text="Your Decks")
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.name_label = Label(self, text="Name")
        self.name_label.grid(row=1, column=0, padx=10, sticky="w")
        self.name_input = Entry(self)
        self.name_input.grid(row=1, column=1, padx=(0, 20), sticky="ew")

        self.desc_label = Label(self, text="Description")
        self.desc_label.grid(row=2, column=0, padx=10, sticky="w")
        self.desc_input = Entry(self)
        self.desc_input.grid(row=2, column=1, padx=(0, 20), sticky="ew")

        self.deck_list = Listbox(self, exportselection=False)
        self.deck_list.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.deck_list.yview)
        self.deck_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=3, column=2, sticky="ns")

        self.create_btn = Button(self, text="Create Deck")
        self.create_btn.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.open_btn = Button(self, text="Open Deck")
        self.open_btn.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        self.delete_btn = Button(self, text="Delete Deck")
        self.delete_btn.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.back_btn = Button(self, text="Back")
        self.back_btn.grid(row=5, column=1, padx=10, pady=10, sticky="e")

        self.message_var = StringVar()
        self.message_label = Label(self, textvariable=self.message_var, fg="red")
        self.message_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def set_message(self, message: str) -> None:
        self.message_var.set(message)

    def clear_inputs(self) -> None:
        self.name_input.delete(0, "end")
        self.desc_input.delete(0, "end")
