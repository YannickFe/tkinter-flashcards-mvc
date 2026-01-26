# -*- coding: utf-8 -*-
import unittest

from models.deck import DeckService
from tests.base import DBTestCase


__author__ = 'fenzl'


class DeckServiceTests(DBTestCase):
    """Exercise deck scoring/selection logic against an in-memory DB."""

    def setUp(self) -> None:
        super().setUp()
        self.service = DeckService(session_factory=self.session_factory)
        self.user = self.create_user(username="test", full_name="Test User")

    def test_score_updates_and_floors(self) -> None:
        deck = self.service.create_deck(user_id=self.user.id, name="Study")
        card = self.service.add_card(
            user_id=self.user.id, deck_id=deck.id, question="Q1", answer="A1"
        )

        increased = self.service.update_score(user_id=self.user.id, card_id=card.id, delta=1)
        self.assertEqual(increased.score, 1)

        decreased = self.service.update_score(user_id=self.user.id, card_id=card.id, delta=-5)
        self.assertEqual(decreased.score, 0)

    def test_weighted_selection_prefers_low_scores(self) -> None:
        deck = self.service.create_deck(user_id=self.user.id, name="Weights")
        low = self.service.add_card(
            user_id=self.user.id, deck_id=deck.id, question="Low", answer="A"
        )
        mid = self.service.add_card(
            user_id=self.user.id, deck_id=deck.id, question="Mid", answer="A"
        )
        high = self.service.add_card(
            user_id=self.user.id, deck_id=deck.id, question="High", answer="A"
        )

        # Adjust scores to drive weighting differences.
        self.service.update_score(user_id=self.user.id, card_id=mid.id, delta=3)
        self.service.update_score(user_id=self.user.id, card_id=high.id, delta=6)

        # Since next card is not deterministic, sample multiple times to verify weighting.
        # Remember the appearance counts to verify that the expected distribution is observed.
        counts = {low.id: 0, mid.id: 0, high.id: 0}
        for _ in range(200):
            card = self.service.next_card_for_study(user_id=self.user.id, deck_id=deck.id)
            if card:
                counts[card.id] += 1

        # We expect low-score cards to appear more frequently than higher-score cards.
        self.assertGreater(counts[low.id], counts[mid.id])
        self.assertGreater(counts[mid.id], counts[high.id])

    def test_next_card_none_when_empty(self) -> None:
        deck = self.service.create_deck(user_id=self.user.id, name="Empty")
        self.assertIsNone(
            self.service.next_card_for_study(user_id=self.user.id, deck_id=deck.id)
        )


if __name__ == "__main__":
    unittest.main()
