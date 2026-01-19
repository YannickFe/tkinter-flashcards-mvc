import unittest

from models.deck import DeckService, CardData
from tests.base import DBTestCase


class DeckCrudTests(DBTestCase):
    """Validate deck and card CRUD behavior and input validation."""
    def setUp(self) -> None:
        super().setUp()
        self.service = DeckService(session_factory=self.session_factory)
        self.user_id = self.create_user()

    def test_create_deck_requires_name(self) -> None:
        with self.assertRaises(ValueError):
            self.service.create_deck(self.user_id, "")

    def test_delete_deck_removes_cards(self) -> None:
        deck = self.service.create_deck(self.user_id, "Has Cards")
        card = self.service.add_card(self.user_id, deck.id, "Q", "A")
        self.assertIsInstance(card, CardData)

        self.service.delete_deck(self.user_id, deck.id)
        cards = self.service.list_cards(self.user_id, deck.id)
        self.assertEqual(cards, [])

    def test_update_card_preserves_missing_fields(self) -> None:
        deck = self.service.create_deck(self.user_id, "Partial Update")
        card = self.service.add_card(self.user_id, deck.id, "Original Q", "Original A")

        updated = self.service.update_card(self.user_id, card.id, question="New Q", answer=None)
        self.assertEqual(updated.question, "New Q")
        self.assertEqual(updated.answer, "Original A")

    def test_update_deck_changes_name_and_description(self) -> None:
        deck = self.service.create_deck(self.user_id, "Old", "Desc")
        updated = self.service.update_deck(self.user_id, deck.id, "New", "New Desc")
        self.assertEqual(updated.name, "New")
        self.assertEqual(updated.description, "New Desc")

    def test_add_card_requires_question_and_answer(self) -> None:
        deck = self.service.create_deck(self.user_id, "Validation")
        with self.assertRaises(ValueError):
            self.service.add_card(self.user_id, deck.id, question="", answer="A")
        with self.assertRaises(ValueError):
            self.service.add_card(self.user_id, deck.id, question="Q", answer="")


if __name__ == "__main__":
    unittest.main()
