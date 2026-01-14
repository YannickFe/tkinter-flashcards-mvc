from __future__ import annotations

from random import Random
from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Session, relationship

from .storage import Base, SessionLocal


class DeckRecord(Base):
    """ORM table for decks (persisted in SQLite)."""
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    cards = relationship("CardRecord", back_populates="deck", cascade="all, delete-orphan")


class CardRecord(Base):
    """ORM table for cards belonging to a deck."""
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    score = Column(Integer, nullable=False, default=0)
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    deck = relationship("DeckRecord", back_populates="cards")


@dataclass
class DeckData:
    id: int
    name: str
    description: str


@dataclass
class CardData:
    id: int
    question: str
    answer: str
    score: int


class DeckService:
    def __init__(self, session_factory=SessionLocal):
        """Service layer for deck/card CRUD and study selection."""
        self._session_factory = session_factory
        self._rng = Random()

    def _session(self) -> Session:
        # Small helper to open a new SQLAlchemy session.
        return self._session_factory()

    def create_deck(self, user_id: int, name: str, description: str = "") -> DeckData:
        if not name:
            raise ValueError("Deck name is required.")
        with self._session() as session:
            deck = DeckRecord(name=name, description=description, user_id=user_id)
            session.add(deck)
            session.commit()
            session.refresh(deck)
            return DeckData(id=deck.id, name=deck.name, description=deck.description or "")

    def list_decks(self, user_id: int) -> List[DeckData]:
        with self._session() as session:
            decks = (
                session.query(DeckRecord)
                .filter(DeckRecord.user_id == user_id)
                .order_by(DeckRecord.name.asc())
                .all()
            )
            return [DeckData(id=d.id, name=d.name, description=d.description or "") for d in decks]

    def delete_deck(self, user_id: int, deck_id: int) -> None:
        with self._session() as session:
            deck = (
                session.query(DeckRecord)
                .filter(DeckRecord.id == deck_id, DeckRecord.user_id == user_id)
                .first()
            )
            if not deck:
                raise ValueError("Deck not found.")
            session.delete(deck)
            session.commit()

    def get_deck(self, user_id: int, deck_id: int) -> DeckData:
        with self._session() as session:
            deck = (
                session.query(DeckRecord)
                .filter(DeckRecord.id == deck_id, DeckRecord.user_id == user_id)
                .first()
            )
            if not deck:
                raise ValueError("Deck not found.")
            return DeckData(id=deck.id, name=deck.name, description=deck.description or "")

    def add_card(self, user_id: int, deck_id: int, question: str, answer: str) -> CardData:
        if not question or not answer:
            raise ValueError("Question and answer are required.")
        with self._session() as session:
            deck = (
                session.query(DeckRecord)
                .filter(DeckRecord.id == deck_id, DeckRecord.user_id == user_id)
                .first()
            )
            if not deck:
                raise ValueError("Deck not found.")
            card = CardRecord(
                question=question, answer=answer, score=0, deck_id=deck_id, user_id=user_id
            )
            session.add(card)
            session.commit()
            session.refresh(card)
            return CardData(id=card.id, question=card.question, answer=card.answer, score=card.score)

    def update_card(
        self, user_id: int, card_id: int, question: Optional[str] = None, answer: Optional[str] = None
    ) -> CardData:
        with self._session() as session:
            card = (
                session.query(CardRecord)
                .filter(CardRecord.id == card_id, CardRecord.user_id == user_id)
                .first()
            )
            if not card:
                raise ValueError("Card not found.")
            if question:
                card.question = question
            if answer:
                card.answer = answer
            session.commit()
            session.refresh(card)
            return CardData(id=card.id, question=card.question, answer=card.answer, score=card.score)

    def delete_card(self, user_id: int, card_id: int) -> None:
        with self._session() as session:
            card = (
                session.query(CardRecord)
                .filter(CardRecord.id == card_id, CardRecord.user_id == user_id)
                .first()
            )
            if not card:
                raise ValueError("Card not found.")
            session.delete(card)
            session.commit()

    def list_cards(self, user_id: int, deck_id: int) -> List[CardData]:
        with self._session() as session:
            cards = (
                session.query(CardRecord)
                .filter(CardRecord.deck_id == deck_id, CardRecord.user_id == user_id)
                .order_by(CardRecord.id.asc())
                .all()
            )
            return [
                CardData(id=c.id, question=c.question, answer=c.answer, score=c.score) for c in cards
            ]

    def update_score(self, user_id: int, card_id: int, delta: int) -> CardData:
        with self._session() as session:
            card = (
                session.query(CardRecord)
                .filter(CardRecord.id == card_id, CardRecord.user_id == user_id)
                .first()
            )
            if not card:
                raise ValueError("Card not found.")
            card.score = max(0, card.score + delta)
            session.commit()
            session.refresh(card)
            return CardData(id=card.id, question=card.question, answer=card.answer, score=card.score)

    def next_card_for_study(self, user_id: int, deck_id: int) -> Optional[CardData]:
        with self._session() as session:
            cards: List[CardRecord] = (
                session.query(CardRecord)
                .filter(CardRecord.deck_id == deck_id, CardRecord.user_id == user_id)
                .all()
            )
            if not cards:
                return None

            max_score = max(card.score for card in cards)
            # Weighted draw: lower scores get higher weight so weak cards surface more often.
            # Each weight is (max_score - current_score + 1) to avoid zeros and keep odds positive.
            weights = [max_score - card.score + 1 for card in cards]
            # choices returns a list of k picks (with replacement); k=1 here, so take the first pick.
            # The chance of each pick is proportional to its weight.
            choice = self._rng.choices(cards, weights=weights, k=1)[0]
            return CardData(
                id=choice.id, question=choice.question, answer=choice.answer, score=choice.score
            )

    def seed_sample(self, user_id: int) -> None:
        """Create a sample deck with cards for quick demos."""
        with self._session() as session:
            existing = (
                session.query(DeckRecord)
                .filter(DeckRecord.user_id == user_id, DeckRecord.name == "Sample Deck")
                .first()
            )
            if existing:
                return

            deck = DeckRecord(name="Sample Deck", description="Getting started", user_id=user_id)
            session.add(deck)
            session.commit()
            session.refresh(deck)

            cards = [
                CardRecord(
                    question="What is Tkinter?",
                    answer="A standard GUI library for Python.",
                    score=0,
                    deck_id=deck.id,
                    user_id=user_id,
                ),
                CardRecord(
                    question="What pattern does this app use?",
                    answer="MVC to separate models, views, and controllers.",
                    score=0,
                    deck_id=deck.id,
                    user_id=user_id,
                ),
            ]
            session.add_all(cards)
            session.commit()
