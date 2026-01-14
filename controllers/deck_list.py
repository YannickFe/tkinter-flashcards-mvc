from typing import List, Optional
from tkinter import messagebox

from controllers.deck_detail import DeckDetailController
from models.main import Model
from models.deck import DeckData
from views.main import View


class DeckListController:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.frame = self.view.frames["deck_list"]
        self.detail_controller: DeckDetailController | None = None
        self._decks: List[DeckData] = []
        self._bind()

    def set_detail_controller(self, controller: DeckDetailController) -> None:
        self.detail_controller = controller

    def _bind(self) -> None:
        """Bind list view actions."""
        self.frame.create_btn.config(command=self.create_deck)
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

    def create_deck(self) -> None:
        name = self.frame.name_input.get()
        description = self.frame.desc_input.get()
        try:
            user_id = self._require_user()
            self.model.decks.create_deck(user_id=user_id, name=name, description=description)
            self.frame.clear_inputs()
            self.refresh()
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
