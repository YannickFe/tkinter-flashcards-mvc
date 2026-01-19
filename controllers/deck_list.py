from tkinter import messagebox
from typing import List, Optional

from controllers.deck_detail import DeckDetailController
from controllers.deck_form import DeckFormController
from models.deck import DeckData
from models.main import Model
from views.main import View


class DeckListController:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.frame = self.view.frames["deck_list"]
        self.detail_controller: DeckDetailController | None = None
        self.form_controller: DeckFormController | None = None
        self._decks: List[DeckData] = []
        self._bind()

    def set_detail_controller(self, controller: "DeckDetailController") -> None:
        self.detail_controller = controller

    def set_form_controller(self, controller: "DeckFormController") -> None:
        self.form_controller = controller

    def _bind(self) -> None:
        """Bind list view actions."""
        self.frame.create_btn.config(command=self.new_deck)
        self.frame.edit_btn.config(command=self.edit_deck)
        self.frame.open_btn.config(command=self.open_deck)
        self.frame.delete_btn.config(command=self.delete_deck)
        self.frame.back_btn.config(command=lambda: self.view.switch("home"))

    def _require_user(self) -> int:
        user = self.model.auth.current_user
        if not user:
            raise ValueError("You must be signed in.")
        return user["id"]

    def refresh(self) -> None:
        """Reload decks for the current user."""
        self._decks = []
        self.frame.deck_list.delete(0, "end")
        try:
            user_id = self._require_user()
            decks = self.model.decks.list_decks(user_id=user_id)
            self._decks = decks
            for deck in decks:
                self.frame.deck_list.insert("end", f"{deck.name} — {deck.description}")
            self.frame.set_message("")
        except ValueError as exc:
            self.frame.set_message(str(exc))

    def _selected_deck(self) -> Optional[DeckData]:
        selection = self.frame.deck_list.curselection()
        if not selection:
            return None
        index = selection[0]
        if index >= len(self._decks):
            return None
        return self._decks[index]

    def new_deck(self) -> None:
        if not self.form_controller:
            self.frame.set_message("Deck form unavailable.")
            return
        self.form_controller.start_create()

    def edit_deck(self) -> None:
        deck = self._selected_deck()
        if not deck:
            self.frame.set_message("Select a deck to edit.")
            return
        if not self.form_controller:
            self.frame.set_message("Deck form unavailable.")
            return
        self.form_controller.start_edit(deck)

    def open_deck(self) -> None:
        deck = self._selected_deck()
        if not deck:
            self.frame.set_message("Select a deck to open.")
            return
        if not self.detail_controller:
            self.frame.set_message("Deck detail controller unavailable.")
            return
        self.detail_controller.load_deck(deck.id)
        self.view.switch("deck_detail")

    def delete_deck(self) -> None:
        deck = self._selected_deck()
        if not deck:
            self.frame.set_message("Select a deck to delete.")
            return
        if messagebox.askyesno("Delete Deck", f"Delete '{deck.name}'?"):
            try:
                user_id = self._require_user()
                self.model.decks.delete_deck(user_id=user_id, deck_id=deck.id)
                self.refresh()
            except ValueError as exc:
                self.frame.set_message(str(exc))
