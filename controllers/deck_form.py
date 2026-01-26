# -*- coding: utf-8 -*-
from controllers.utils import require_user
from models.deck import DeckData
from models.main import MainModel
from views.main import MainView


__author__ = 'fenzl'


class DeckFormController:
    def __init__(self, main_model: MainModel, main_view: MainView, deck_list_controller):
        """Handle create/edit of decks via the deck form view."""
        self.main_model = main_model
        self.main_view = main_view
        self.deck_list_controller = deck_list_controller
        self.frame = self.main_view.frames["deck_form"]
        self.current_deck_id: int | None = None
        self._bind()

    def _bind(self) -> None:
        self.frame.set_save_command(self.save)
        self.frame.set_cancel_command(self.cancel)

    def start_create(self) -> None:
        """Open the form in create mode."""
        self.current_deck_id = None
        self.frame.set_title(title="Create Deck")
        self.frame.set_message(message="")
        self.frame.clear_inputs()
        self.main_view.switch(name="deck_form")

    def start_edit(self, deck: DeckData) -> None:
        """Open the form in edit mode for an existing deck."""
        self.current_deck_id = deck.id
        self.frame.set_title(title="Edit Deck")
        self.frame.set_message(message="")
        self.frame.clear_inputs()
        self.frame.set_name(deck.name)
        self.frame.set_description(deck.description)
        self.main_view.switch(name="deck_form")

    def save(self) -> None:
        """Persist changes and return to the deck list."""
        name = self.frame.get_name().strip()
        desc = self.frame.get_description().strip()
        try:
            user = require_user(auth=self.main_model.auth)
            if self.current_deck_id is None:
                self.main_model.decks.create_deck(user_id=user.id, name=name, description=desc)
            else:
                self.main_model.decks.update_deck(
                    user_id=user.id, deck_id=self.current_deck_id, name=name, description=desc
                )
            self.deck_list_controller.refresh()
            self.main_view.switch(name="deck_list")
        except ValueError as exception:
            # Validation or missing auth/user context; surface message on the form.
            self.frame.set_message(message=str(exception))

    def cancel(self) -> None:
        self.main_view.switch(name="deck_list")
