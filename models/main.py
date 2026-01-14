from .auth import Auth
from .deck import DeckService


class Model:
    def __init__(self):
        self.auth = Auth()
        self.decks = DeckService()
