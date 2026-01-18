import unittest

from models.deck import DeckService
from tests.base import DBTestCase


class DeckServiceTests(DBTestCase):
    """Exercise deck scoring/selection logic against an in-memory DB."""
    def setUp(self) -> None:
        super().setUp()
        self.service = DeckService(session_factory=self.session_factory)

        self.user_id = self.create_user(username="test", full_name="Test User")

    def test_score_updates_and_floors(self) -> None:
        deck = self.service.create_deck(self.user_id, "Study")
        card = self.service.add_card(self.user_id, deck.id, "Q1", "A1")

        increased = self.service.update_score(self.user_id, card.id, 1)
        self.assertEqual(increased.score, 1)

        decreased = self.service.update_score(self.user_id, card.id, -5)
        self.assertEqual(decreased.score, 0)

    def test_weighted_selection_prefers_low_scores(self) -> None:
        deck = self.service.create_deck(self.user_id, "Weights")
        low = self.service.add_card(self.user_id, deck.id, "Low", "A")
        mid = self.service.add_card(self.user_id, deck.id, "Mid", "A")
        high = self.service.add_card(self.user_id, deck.id, "High", "A")

        # Adjust scores to drive weighting differences.
        self.service.update_score(self.user_id, mid.id, 3)
        self.service.update_score(self.user_id, high.id, 6)

        counts = {low.id: 0, mid.id: 0, high.id: 0}
        for _ in range(200):
            card = self.service.next_card_for_study(self.user_id, deck.id)
            if card:
                counts[card.id] += 1

        self.assertGreater(counts[low.id], counts[mid.id])
        self.assertGreater(counts[mid.id], counts[high.id])

    def test_next_card_none_when_empty(self) -> None:
        deck = self.service.create_deck(self.user_id, "Empty")
        self.assertIsNone(self.service.next_card_for_study(self.user_id, deck.id))


if __name__ == "__main__":
    unittest.main()
