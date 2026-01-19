from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Session, relationship

from models.storage import Base, SessionLocal


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

    def __repr__(self) -> str:
        desc = (self.description[:20] + "...") if len(self.description) > 20 else self.description
        return f"DeckData(id={self.id}, name={self.name!r}, desc={desc!r})"


@dataclass
class CardData:
    id: int
    question: str
    answer: str
    score: int

    def __repr__(self) -> str:
        question_preview = (self.question[:20] + "...") if len(self.question) > 20 else self.question
        return f"CardData(id={self.id}, q={question_preview!r}, score={self.score})"


class DeckService:
    def __init__(self, session_factory=SessionLocal):
        """Service layer for deck/card CRUD and study selection."""
        self._session_factory = session_factory
        self._rng = Random()

    def _session(self) -> Session:
        # Small helper to open a new SQLAlchemy session.
        return self._session_factory()

    def _log(self, message: str) -> None:
        print(f"[DeckService] {message}")

    def create_deck(self, user_id: int, name: str, description: str = "") -> DeckData:
        if not name:
            raise ValueError("Deck name is required.")  # Validation: avoid blank decks.
        with self._session() as session:
            deck = DeckRecord(name=name, description=description, user_id=user_id)
            session.add(deck)
            session.commit()
            session.refresh(deck)
            data = DeckData(id=deck.id, name=deck.name, description=deck.description or "")
            self._log(f"Created deck {data}")
            return data

    def update_deck(self, user_id: int, deck_id: int, name: str, description: str = "") -> DeckData:
        if not name:
            raise ValueError("Deck name is required.")
        with self._session() as session:
            deck = (
                session.query(DeckRecord)
                .filter(DeckRecord.id == deck_id, DeckRecord.user_id == user_id)
                .first()
            )
            if not deck:
                raise ValueError("Deck not found.")  # Missing or not owned by user.
            deck.name = name
            deck.description = description
            session.commit()
            session.refresh(deck)
            data = DeckData(id=deck.id, name=deck.name, description=deck.description or "")
            self._log(f"Updated deck {data}")
            return data

    def list_decks(self, user_id: int) -> List[DeckData]:
        with self._session() as session:
            decks = (
                session.query(DeckRecord)
                .filter(DeckRecord.user_id == user_id)
                .order_by(DeckRecord.name.asc())
                .all()
            )
            result = [DeckData(id=d.id, name=d.name, description=d.description or "") for d in decks]
            self._log(f"Fetched {len(result)} decks for user {user_id}")
            return result

    def delete_deck(self, user_id: int, deck_id: int) -> None:
        with self._session() as session:
            deck = (
                session.query(DeckRecord)
                .filter(DeckRecord.id == deck_id, DeckRecord.user_id == user_id)
                .first()
            )
            if not deck:
                raise ValueError("Deck not found.")  # No deck for this user.
            session.delete(deck)
            session.commit()
            self._log(f"Deleted deck id={deck_id} for user {user_id}")

    def get_deck(self, user_id: int, deck_id: int) -> DeckData:
        with self._session() as session:
            deck = (
                session.query(DeckRecord)
                .filter(DeckRecord.id == deck_id, DeckRecord.user_id == user_id)
                .first()
            )
            if not deck:
                raise ValueError("Deck not found.")
            data = DeckData(id=deck.id, name=deck.name, description=deck.description or "")
            self._log(f"Loaded deck {data}")
            return data

    def add_card(self, user_id: int, deck_id: int, question: str, answer: str) -> CardData:
        if not question or not answer:
            raise ValueError("Question and answer are required.")  # Validation guard.
        with self._session() as session:
            deck = (
                session.query(DeckRecord)
                .filter(DeckRecord.id == deck_id, DeckRecord.user_id == user_id)
                .first()
            )
            if not deck:
                raise ValueError("Deck not found.")  # No deck for this user.
            card = CardRecord(
                question=question, answer=answer, score=0, deck_id=deck_id, user_id=user_id
            )
            session.add(card)
            session.commit()
            session.refresh(card)
            data = CardData(id=card.id, question=card.question, answer=card.answer, score=card.score)
            self._log(f"Added card {data} to deck {deck_id}")
            return data

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
                raise ValueError("Card not found.")  # Missing or not owned by user.
            if question:
                card.question = question
            if answer:
                card.answer = answer
            session.commit()
            session.refresh(card)
            data = CardData(id=card.id, question=card.question, answer=card.answer, score=card.score)
            self._log(f"Updated card {data}")
            return data

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
            self._log(f"Deleted card id={card_id} for user {user_id}")

    def list_cards(self, user_id: int, deck_id: int) -> List[CardData]:
        with self._session() as session:
            cards = (
                session.query(CardRecord)
                .filter(CardRecord.deck_id == deck_id, CardRecord.user_id == user_id)
                .order_by(CardRecord.id.asc())
                .all()
            )
            result = [
                CardData(id=c.id, question=c.question, answer=c.answer, score=c.score) for c in cards
            ]
            self._log(f"Fetched {len(result)} cards for deck {deck_id} (user {user_id})")
            return result

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
            data = CardData(id=card.id, question=card.question, answer=card.answer, score=card.score)
            self._log(f"Updated score for card {data} (delta={delta})")
            return data

    def next_card_for_study(self, user_id: int, deck_id: int) -> Optional[CardData]:
        with self._session() as session:
            cards: List[CardRecord] = (
                session.query(CardRecord)
                .filter(CardRecord.deck_id == deck_id, CardRecord.user_id == user_id)
                .all()
            )
            if not cards:
                self._log(f"No cards available for study in deck {deck_id}")
                return None

            max_score = max(card.score for card in cards)
            # Weighted draw: lower scores get higher weight so weak cards surface more often.
            # Each weight is (max_score - current_score + 1) to avoid zeros and keep odds positive.
            weights = [max_score - card.score + 1 for card in cards]
            # choices returns a list of k picks (with replacement); k=1 here, so take the first pick.
            # The chance of each pick is proportional to its weight.
            choice = self._rng.choices(cards, weights=weights, k=1)[0]
            data = CardData(
                id=choice.id, question=choice.question, answer=choice.answer, score=choice.score
            )
            self._log(f"Selected next study card {data} from deck {deck_id}")
            return data

    def seed_sample(self, user_id: int) -> None:
        """Create a sample deck with cards for quick demos."""
        with self._session() as session:
            existing = (
                session.query(DeckRecord)
                .filter(DeckRecord.user_id == user_id, DeckRecord.name == "Sample Deck")
                .first()
            )
            if existing:
                self._log("Sample deck already exists; skipping seed")
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
            self._log(f"Seeded sample deck with {len(cards)} cards for user {user_id}")
