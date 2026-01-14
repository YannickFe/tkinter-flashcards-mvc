from tkinter import Button, Entry, Frame, Label, Listbox, Scrollbar, StringVar, Text


class DeckDetailView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.title_var = StringVar()
        self.title_label = Label(self, textvariable=self.title_var)
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.cards_list = Listbox(self, exportselection=False)
        self.cards_list.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.cards_list.yview)
        self.cards_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=2, sticky="ns")

        self.question_label = Label(self, text="Question")
        self.question_label.grid(row=2, column=0, padx=10, sticky="w")
        self.question_input = Text(self, height=4, width=40)
        self.question_input.grid(row=2, column=1, padx=(0, 20), sticky="ew")

        self.answer_label = Label(self, text="Answer")
        self.answer_label.grid(row=3, column=0, padx=10, sticky="w")
        self.answer_input = Text(self, height=4, width=40)
        self.answer_input.grid(row=3, column=1, padx=(0, 20), sticky="ew")

        self.add_card_btn = Button(self, text="Add Card")
        self.add_card_btn.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.update_card_btn = Button(self, text="Update Card")
        self.update_card_btn.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        self.delete_card_btn = Button(self, text="Delete Card")
        self.delete_card_btn.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.study_btn = Button(self, text="Start Study")
        self.study_btn.grid(row=5, column=1, padx=10, pady=10, sticky="e")

        self.back_btn = Button(self, text="Back to Decks")
        self.back_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.message_var = StringVar()
        self.message_label = Label(self, textvariable=self.message_var, fg="red")
        self.message_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def set_title(self, name: str) -> None:
        self.title_var.set(f"Deck: {name}")

    def set_message(self, message: str) -> None:
        self.message_var.set(message)

    def clear_inputs(self) -> None:
        self.question_input.delete("1.0", "end")
        self.answer_input.delete("1.0", "end")
