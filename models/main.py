from models.auth import Auth
from models.deck import DeckService


class MainModel:
    def __init__(self):
        self.auth = Auth()
        self.decks = DeckService()
