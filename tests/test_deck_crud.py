# -*- coding: utf-8 -*-
import unittest

from models.deck import DeckService, CardData
from tests.base import DBTestCase


__author__ = 'fenzl'


class DeckCrudTests(DBTestCase):
    """Validate deck and card CRUD behavior and input validation."""

    def setUp(self) -> None:
        super().setUp()
        self.service = DeckService(session_factory=self.session_factory)
        self.user = self.create_user()

    def test_create_deck_requires_name(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create_deck(user_id=self.user.id, name="")

    def test_delete_deck_removes_cards(self) -> None:
        deck = self.service.create_deck(user_id=self.user.id, name="Has Cards")
        card = self.service.add_card(
            user_id=self.user.id, deck_id=deck.id, question="Q", answer="A"
        )
        self.assertIsInstance(card, CardData)

        self.service.delete_deck(user_id=self.user.id, deck_id=deck.id)
        cards = self.service.list_cards(user_id=self.user.id, deck_id=deck.id)
        self.assertEqual(cards, [])

    def test_update_card_preserves_missing_fields(self) -> None:
        deck = self.service.create_deck(user_id=self.user.id, name="Partial Update")
        card = self.service.add_card(
            user_id=self.user.id, deck_id=deck.id, question="Original Q", answer="Original A"
        )

        updated = self.service.update_card(
            user_id=self.user.id, card_id=card.id, question="New Q", answer=None
        )
        self.assertEqual(updated.question, "New Q")
        self.assertEqual(updated.answer, "Original A")

    def test_update_deck_changes_name_and_description(self) -> None:
        deck = self.service.create_deck(user_id=self.user.id, name="Old", description="Desc")
        updated = self.service.update_deck(
            user_id=self.user.id, deck_id=deck.id, name="New", description="New Desc"
        )
        self.assertEqual(updated.name, "New")
        self.assertEqual(updated.description, "New Desc")

    def test_add_card_requires_question_and_answer(self) -> None:
        deck = self.service.create_deck(user_id=self.user.id, name="Validation")
        with self.assertRaises(ValueError):
            self.service.add_card(
                user_id=self.user.id, deck_id=deck.id, question="", answer="A"
            )
        with self.assertRaises(ValueError):
            self.service.add_card(
                user_id=self.user.id, deck_id=deck.id, question="Q", answer=""
            )


if __name__ == "__main__":
    unittest.main()
