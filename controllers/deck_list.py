from tkinter import messagebox
from typing import List, Optional

from controllers.deck_detail import DeckDetailController
from controllers.deck_form import DeckFormController
from controllers.utils import require_user_id
from models.deck import DeckData
from models.main import MainModel
from views.main import MainView


class DeckListController:
    def __init__(self, main_model: MainModel, main_view: MainView):
        """List decks for the current user and hand off to detail/form controllers."""
        self.main_model = main_model
        self.main_view = main_view
        self.frame = self.main_view.frames["deck_list"]
        self.detail_controller: DeckDetailController | None = None
        self.form_controller: DeckFormController | None = None
        self._decks: List[DeckData] = []
        self._bind()

    def set_detail_controller(self, controller: DeckDetailController) -> None:
        self.detail_controller = controller

    def set_form_controller(self, controller: DeckFormController) -> None:
        self.form_controller = controller

    def _bind(self) -> None:
        """Bind list view actions."""
        self.frame.create_btn.config(command=self.new_deck)
        self.frame.edit_btn.config(command=self.edit_deck)
        self.frame.open_btn.config(command=self.open_deck)
        self.frame.delete_btn.config(command=self.delete_deck)
        self.frame.back_btn.config(command=lambda: self.main_view.switch("home"))

    def refresh(self) -> None:
        """Reload decks for the current user."""
        self._decks = []
        self.frame.deck_list.delete(0, "end")
        try:
            user_id = require_user_id(self.main_model.auth)
            decks = self.main_model.decks.list_decks(user_id=user_id)
            self._decks = decks
            for deck in decks:
                self.frame.deck_list.insert("end", f"{deck.name} — {deck.description}")
            self.frame.set_message("")
        except ValueError as exception:
            # Missing auth or fetch failure; surface message to the list view.
            self.frame.set_message(str(exception))

    def _selected_deck(self) -> Optional[DeckData]:
        """Return the currently highlighted deck, or None."""
        selection = self.frame.deck_list.curselection()
        if not selection:
            return None
        index = selection[0]
        if index >= len(self._decks):
            return None
        return self._decks[index]

    def new_deck(self) -> None:
        """Open deck form in create mode."""
        if not self.form_controller:
            self.frame.set_message("Deck form unavailable.")
            return
        self.form_controller.start_create()

    def edit_deck(self) -> None:
        """Open deck form in edit mode for the selected deck."""
        deck = self._selected_deck()
        if not deck:
            self.frame.set_message("Select a deck to edit.")
            return
        if not self.form_controller:
            self.frame.set_message("Deck form unavailable.")
            return
        self.form_controller.start_edit(deck)

    def open_deck(self) -> None:
        """Load selected deck into detail view."""
        deck = self._selected_deck()
        if not deck:
            self.frame.set_message("Select a deck to open.")
            return
        if not self.detail_controller:
            self.frame.set_message("Deck detail controller unavailable.")
            return
        self.detail_controller.load_deck(deck.id)
        self.main_view.switch("deck_detail")

    def delete_deck(self) -> None:
        """Remove the selected deck after confirmation."""
        deck = self._selected_deck()
        if not deck:
            self.frame.set_message("Select a deck to delete.")
            return
        if messagebox.askyesno("Delete Deck", f"Delete '{deck.name}'?"):
            try:
                user_id = require_user_id(self.main_model.auth)
                self.main_model.decks.delete_deck(user_id=user_id, deck_id=deck.id)
                self.refresh()
            except ValueError as exception:
                # Deleting without auth or against a missing deck.
                self.frame.set_message(str(exception))
