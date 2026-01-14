from models.auth import Auth
from models.deck import DeckService


class Model:
    def __init__(self):
        self.auth = Auth()
        self.decks = DeckService()
