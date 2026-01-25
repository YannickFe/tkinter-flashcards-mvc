from tkinter import END, messagebox
from typing import List, Optional, TYPE_CHECKING

from controllers.utils import require_user, truncate_and_pad
from models.deck import CardData
from models.main import MainModel
from views.main import MainView

if TYPE_CHECKING:
    from controllers.card_form import CardFormController
    from controllers.study import StudyController


class DeckDetailController:
    def __init__(self, main_model: MainModel, main_view: MainView):
        """Show cards for a deck and route add/edit/study actions to other controllers."""
        self.main_model = main_model
        self.main_view = main_view
        self.frame = self.main_view.frames["deck_detail"]
        self.study_controller: "StudyController | None" = None
        self.card_form_controller: "CardFormController | None" = None
        self.current_deck_id: int | None = None
        self.current_deck_name: str = ""
        self.current_cards: List[CardData] = []
        self._bind()

    def set_study_controller(self, controller: "StudyController") -> None:
        self.study_controller = controller

    def set_card_form_controller(self, controller: "CardFormController") -> None:
        self.card_form_controller = controller

    def _bind(self) -> None:
        """Bind deck detail actions."""
        self.frame.add_card_btn.config(command=self.add_card)
        self.frame.update_card_btn.config(command=self.update_card)
        self.frame.delete_card_btn.config(command=self.delete_card)
        self.frame.study_btn.config(command=self.start_study)
        self.frame.back_btn.config(command=self.back_to_decks)

    def load_deck(self, deck_id: int) -> None:
        """Load deck metadata and cards."""
        try:
            user = require_user(auth=self.main_model.auth)
            deck = self.main_model.decks.get_deck(user_id=user.id, deck_id=deck_id)
            self.current_deck_id = deck.id
            self.current_deck_name = deck.name
            self.frame.set_title(name=deck.name)
            self.refresh_cards()
            self.frame.set_message(message="")
        except ValueError as exception:
            # Typical issues: not signed in or deck not found for this user.
            self.frame.set_message(message=str(exception))

    def refresh_cards(self) -> None:
        """Reload cards into the list."""
        if self.current_deck_id is None:
            return
        try:
            user = require_user(auth=self.main_model.auth)
            cards = self.main_model.decks.list_cards(user_id=user.id, deck_id=self.current_deck_id)
            self.current_cards = cards
            self.frame.cards_list.delete(0, END)
            for card in cards:
                question_preview = truncate_and_pad(text=card.question, width=30)
                display = f"Q: {question_preview} | Score: {card.score}"
                self.frame.cards_list.insert(END, display)
            self.frame.set_message(message="")
        except ValueError as exception:
            # Likely missing auth or deck/cards no longer exist.
            self.frame.set_message(message=str(exception))

    def _selected_card(self) -> Optional[CardData]:
        """Return the selected card (or None)."""
        selection = self.frame.cards_list.curselection()
        if not selection:
            return None
        index = selection[0]
        if index >= len(self.current_cards):
            return None
        return self.current_cards[index]

    def add_card(self) -> None:
        if self.current_deck_id is None or not self.card_form_controller:
            self.frame.set_message(message="Card form unavailable.")
            return
        self.card_form_controller.start_create(
            deck_id=self.current_deck_id, deck_name=self.current_deck_name
        )

    def update_card(self) -> None:
        card = self._selected_card()
        if not card:
            self.frame.set_message(message="Select a card to edit.")
            return
        if self.current_deck_id is None or not self.card_form_controller:
            self.frame.set_message(message="Card form unavailable.")
            return
        self.card_form_controller.start_edit(
            deck_id=self.current_deck_id, deck_name=self.current_deck_name, card=card
        )

    def delete_card(self) -> None:
        card = self._selected_card()
        if not card:
            self.frame.set_message(message="Select a card to delete.")
            return
        if messagebox.askyesno("Delete Card", "Delete this card?"):
            try:
                user = require_user(auth=self.main_model.auth)
                self.main_model.decks.delete_card(user_id=user.id, card_id=card.id)
                self.refresh_cards()
            except ValueError as exception:
                # Missing auth or card already removed.
                self.frame.set_message(message=str(exception))

    def start_study(self) -> None:
        if not self.study_controller or self.current_deck_id is None:
            self.frame.set_message(message="Study controller unavailable.")
            return
        try:
            user = require_user(auth=self.main_model.auth)
            deck = self.main_model.decks.get_deck(user_id=user.id, deck_id=self.current_deck_id)
            self.study_controller.start(deck_id=self.current_deck_id, deck_name=deck.name)
            self.main_view.switch(name="study")
        except ValueError as exception:
            self.frame.set_message(message=str(exception))

    def back_to_decks(self) -> None:
        self.main_view.switch(name="deck_list")
