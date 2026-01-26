# -*- coding: utf-8 -*-
from models.deck import DeckService
from models.user import UserService


__author__ = 'fenzl, ahsan'


class MainModel:
    def __init__(self):
        self.users = UserService()
        self.decks = DeckService()
