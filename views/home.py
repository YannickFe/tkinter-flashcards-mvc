# -*- coding: utf-8 -*-
from tkinter import Frame, Label, Button


__author__ = 'fenzl, ahsan'


class HomeView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.header = Label(self, text="Home")
        self.header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.greeting = Label(self, text="")
        self.greeting.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.deck_btn = Button(self, text="Decks")
        self.deck_btn.grid(row=3, column=0, padx=10, pady=10)

        self.signout_btn = Button(self, text="Sign Out")
        self.signout_btn.grid(row=2, column=0, padx=10, pady=10)

    def set_greeting(self, text: str) -> None:
        self.greeting.config(text=text)

    def set_signout_command(self, command) -> None:
        self.signout_btn.config(command=command)

    def set_deck_command(self, command) -> None:
        self.deck_btn.config(command=command)
