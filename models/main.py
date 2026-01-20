from models.deck import DeckService
from models.user import UserService


class MainModel:
    def __init__(self):
        self.auth = UserService()
        self.decks = DeckService()
