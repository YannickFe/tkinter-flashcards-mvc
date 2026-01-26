# -*- coding: utf-8 -*-
from models.deck import DeckService
from models.storage import init_db
from models.user import UserService


__author__ = 'fenzl, ahsan'


class MainModel:
    def __init__(self):
        # Ensure all mapped tables are created once at startup
        init_db()
        self.users = UserService()
        self.decks = DeckService()
