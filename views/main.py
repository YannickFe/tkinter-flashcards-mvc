# -*- coding: utf-8 -*-
from tkinter import Frame
from typing import TypedDict

from views.card_form import CardFormView
from views.deck_detail import DeckDetailView
from views.deck_form import DeckFormView
from views.deck_list import DeckListView
from views.home import HomeView
from views.root import Root
from views.signin import SignInView
from views.signup import SignUpView
from views.study import StudyView


__author__ = 'fenzl, ahsan'

class Frames(TypedDict):
    # TypedDict keeps frame names & types explicit for type checkers; at runtime it's a dict.
    signup: SignUpView
    signin: SignInView
    home: HomeView
    deck_list: DeckListView
    deck_detail: DeckDetailView
    study: StudyView
    deck_form: DeckFormView
    card_form: CardFormView


class MainView:
    def __init__(self):
        # Root Tk window that hosts all frames.
        self.root = Root()
        self.frames: Frames = {}  # type: ignore

        # Instantiate all frames up front and stack them
        # We can switch to the new active one by raising it to the top
        self._add_frame(frame_class=SignUpView, name="signup")
        self._add_frame(frame_class=SignInView, name="signin")
        self._add_frame(frame_class=HomeView, name="home")
        self._add_frame(frame_class=DeckListView, name="deck_list")
        self._add_frame(frame_class=DeckDetailView, name="deck_detail")
        self._add_frame(frame_class=StudyView, name="study")
        self._add_frame(frame_class=DeckFormView, name="deck_form")
        self._add_frame(frame_class=CardFormView, name="card_form")

    def _add_frame(self, frame_class: type, name: str) -> None:
        if not issubclass(frame_class, Frame):
            raise ValueError(f"Frame '{name}' is not a subclass of tkinter.Frame.")
        if name in self.frames:
            raise ValueError(f"Frame '{name}' already exists.")
        # Params are valid, create the frame and add it to the dict
        self.frames[name] = frame_class(self.root)  # type: ignore
        self.frames[name].grid(row=0, column=0, sticky="nsew")  # type: ignore

    def switch(self, name: str) -> None:
        if not name in self.frames:
            raise ValueError(f"Frame '{name}' does not exist.")
        frame = self.frames[name]  # type: ignore
        # Raise the frame to the top to make it visible
        frame.tkraise()

    def start_mainloop(self) -> None:
        # Start the main Tk loop
        self.root.mainloop()
