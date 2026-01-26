# -*- coding: utf-8 -*-
from tkinter import Button, Frame, Label, StringVar


__author__ = 'fenzl'

class StudyView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.deck_title_var = StringVar()
        self.deck_title_label = Label(self, textvariable=self.deck_title_var)
        self.deck_title_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.question_var = StringVar()
        self.question_label = Label(self, textvariable=self.question_var, wraplength=400)
        self.question_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.answer_var = StringVar()
        self.answer_label = Label(self, textvariable=self.answer_var, wraplength=400)
        self.answer_label.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.show_answer_btn = Button(self, text="Show Answer")
        self.show_answer_btn.grid(row=3, column=0, padx=10, pady=5)

        self.memorized_btn = Button(self, text="Memorized")
        self.memorized_btn.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.not_memorized_btn = Button(self, text="Not Memorized")
        self.not_memorized_btn.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        self.back_btn = Button(self, text="Back to Deck")
        self.back_btn.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

        self.message_var = StringVar()
        self.message_label = Label(self, textvariable=self.message_var, fg="red")
        self.message_label.grid(row=7, column=0, padx=10, pady=5, sticky="ew")

    def set_message(self, message: str) -> None:
        self.message_var.set(message)

    def set_deck_title(self, name: str) -> None:
        self.deck_title_var.set(f"Studying: {name}")

    def clear_card(self) -> None:
        self.question_var.set("")
        self.answer_var.set("")
