# -*- coding: utf-8 -*-
from tkinter import Button, Frame, Label, Listbox, Scrollbar, StringVar


__author__ = 'fenzl'


class DeckDetailView(Frame):
    """Deck detail view with card list and action controls."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_var = StringVar()
        self.title_label = Label(self, textvariable=self.title_var)
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Monospace font keeps columns aligned for padded question/score display.
        self.cards_list = Listbox(self, exportselection=False, font=("Courier New", 10))
        self.cards_list.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.scrollbar = Scrollbar(self, orient="vertical", command=self.cards_list.yview)
        self.cards_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=2, sticky="ns")

        self.add_card_btn = Button(self, text="Add Card")
        self.add_card_btn.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.update_card_btn = Button(self, text="Edit Card")
        self.update_card_btn.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        self.delete_card_btn = Button(self, text="Delete Card")
        self.delete_card_btn.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.study_btn = Button(self, text="Start Study")
        self.study_btn.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        self.back_btn = Button(self, text="Back to Decks")
        self.back_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.message_var = StringVar()
        self.message_label = Label(self, textvariable=self.message_var, fg="red")
        self.message_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def set_title(self, name: str) -> None:
        self.title_var.set(f"Deck: {name}")

    def set_message(self, message: str) -> None:
        self.message_var.set(message)

    def set_add_card_command(self, command) -> None:
        self.add_card_btn.config(command=command)

    def set_update_card_command(self, command) -> None:
        self.update_card_btn.config(command=command)

    def set_delete_card_command(self, command) -> None:
        self.delete_card_btn.config(command=command)

    def set_study_command(self, command) -> None:
        self.study_btn.config(command=command)

    def set_back_command(self, command) -> None:
        self.back_btn.config(command=command)

    def clear_cards(self) -> None:
        self.cards_list.delete(0, "end")

    def insert_card(self, display_text: str) -> None:
        self.cards_list.insert("end", display_text)

    def get_selected_index(self) -> int | None:
        selection = self.cards_list.curselection()
        if not selection:
            return None
        return selection[0]
