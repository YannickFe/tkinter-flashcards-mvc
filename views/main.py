from typing import TypedDict

from .deck_list import DeckListView
from .deck_detail import DeckDetailView
from .root import Root
from .home import HomeView
from .signin import SignInView
from .signup import SignUpView
from .study import StudyView


class Frames(TypedDict):
    # TypedDict keeps frame names & types explicit for type checkers; at runtime it's a dict.
    signup: SignUpView
    signin: SignInView
    home: HomeView
    deck_list: DeckListView
    deck_detail: DeckDetailView
    study: StudyView


class View:
    def __init__(self):
        # Root Tk window that hosts all frames.
        self.root = Root()
        self.frames: Frames = {}  # type: ignore

        # Instantiate all frames up front and stack them
        # We can switch to the new active one by raising it to the top
        self._add_frame(SignUpView, "signup")
        self._add_frame(SignInView, "signin")
        self._add_frame(HomeView, "home")
        self._add_frame(DeckListView, "deck_list")
        self._add_frame(DeckDetailView, "deck_detail")
        self._add_frame(StudyView, "study")

    def _add_frame(self, Frame, name: str) -> None:
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def switch(self, name: str) -> None:
        frame = self.frames[name]
        # Raise the frame to the top to make it visible
        frame.tkraise()

    def start_mainloop(self) -> None:
        # Start the main Tk loop
        self.root.mainloop()
