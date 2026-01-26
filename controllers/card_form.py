# -*- coding: utf-8 -*-
from controllers.utils import require_user
from models.deck import CardData
from models.main import MainModel
from views.main import MainView

__author__ = 'fenzl'

class CardFormController:
    def __init__(self, main_model: MainModel, main_view: MainView, deck_detail_controller):
        """Handle create/edit of cards via the card form view."""
        self.main_model = main_model
        self.main_view = main_view
        self.deck_detail_controller = deck_detail_controller
        self.frame = self.main_view.frames["card_form"]
        self.current_deck_id: int | None = None
        self.current_deck_name: str = ""
        self.current_card_id: int | None = None
        self._bind()

    def _bind(self) -> None:
        self.frame.save_btn.config(command=self.save)
        self.frame.cancel_btn.config(command=self.cancel)

    def start_create(self, deck_id: int, deck_name: str) -> None:
        """Open the form in create mode."""
        self.current_deck_id = deck_id
        self.current_deck_name = deck_name
        self.current_card_id = None
        self.frame.set_title(title=f"Add Card to '{deck_name}'")
        self.frame.set_message(message="")
        self.frame.clear_inputs()
        self.main_view.switch(name="card_form")

    def start_edit(self, deck_id: int, deck_name: str, card: CardData) -> None:
        """Open the form in edit mode for an existing card."""
        self.current_deck_id = deck_id
        self.current_deck_name = deck_name
        self.current_card_id = card.id
        self.frame.set_title(title=f"Edit Card in '{deck_name}'")
        self.frame.set_message(message="")
        self.frame.clear_inputs()
        self.frame.question_input.insert("1.0", card.question)
        self.frame.answer_input.insert("1.0", card.answer)
        self.main_view.switch(name="card_form")

    def save(self) -> None:
        """Persist changes and return to deck detail."""
        question = self.frame.question_input.get("1.0", "end").strip()
        answer = self.frame.answer_input.get("1.0", "end").strip()
        if self.current_deck_id is None:
            self.frame.set_message(message="No deck selected.")
            return
        try:
            user = require_user(auth=self.main_model.auth)
            if self.current_card_id is None:
                self.main_model.decks.add_card(
                    user_id=user.id, deck_id=self.current_deck_id, question=question, answer=answer
                )
            else:
                self.main_model.decks.update_card(
                    user_id=user.id, card_id=self.current_card_id, question=question, answer=answer
                )
            self.deck_detail_controller.load_deck(deck_id=self.current_deck_id)
            self.main_view.switch(name="deck_detail")
        except ValueError as exception:
            # Validation errors (empty fields) or missing auth/deck context.
            self.frame.set_message(message=str(exception))

    def cancel(self) -> None:
        self.main_view.switch(name="deck_detail")
