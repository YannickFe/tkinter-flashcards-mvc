from typing import List, Optional
from tkinter import END, messagebox

from controllers.study import StudyController
from models.main import Model
from models.deck import CardData
from views.main import View


class DeckDetailController:
    def __init__(self, model: Model, view: View):
        self.model = model
        self.view = view
        self.frame = self.view.frames["deck_detail"]
        self.study_controller: StudyController | None = None
        self.current_deck_id: int | None = None
        self.current_cards: List[CardData] = []
        self._bind()

    def set_study_controller(self, controller: StudyController) -> None:
        self.study_controller = controller

    def _bind(self) -> None:
        """Bind deck detail actions."""
        self.frame.add_card_btn.config(command=self.add_card)
        self.frame.update_card_btn.config(command=self.update_card)
        self.frame.delete_card_btn.config(command=self.delete_card)
        self.frame.study_btn.config(command=self.start_study)
        self.frame.back_btn.config(command=self.back_to_decks)
        self.frame.cards_list.bind("<<ListboxSelect>>", self.on_card_select)

    def _require_user(self) -> int:
        user = self.model.auth.current_user
        if not user:
            raise ValueError("You must be signed in.")
        return user["id"]

    def load_deck(self, deck_id: int) -> None:
        """Load deck metadata and cards."""
        try:
            user_id = self._require_user()
            deck = self.model.decks.get_deck(user_id=user_id, deck_id=deck_id)
            self.current_deck_id = deck.id
            self.frame.set_title(deck.name)
            self.refresh_cards()
            self.frame.set_message("")
        except ValueError as exc:
            self.frame.set_message(str(exc))

    def refresh_cards(self) -> None:
        if self.current_deck_id is None:
            return
        try:
            user_id = self._require_user()
            cards = self.model.decks.list_cards(user_id=user_id, deck_id=self.current_deck_id)
            self.current_cards = cards
            self.frame.cards_list.delete(0, END)
            for card in cards:
                display = f"Q: {card.question[:30]}... | Score: {card.score}"
                self.frame.cards_list.insert(END, display)
            self.frame.set_message("")
        except ValueError as exc:
            self.frame.set_message(str(exc))

    def _selected_card(self) -> Optional[CardData]:
        selection = self.frame.cards_list.curselection()
        if not selection:
            return None
        index = selection[0]
        if index >= len(self.current_cards):
            return None
        return self.current_cards[index]

    def add_card(self) -> None:
        if self.current_deck_id is None:
            self.frame.set_message("No deck selected.")
            return
        question = self.frame.question_input.get("1.0", END).strip()
        answer = self.frame.answer_input.get("1.0", END).strip()
        try:
            user_id = self._require_user()
            self.model.decks.add_card(
                user_id=user_id, deck_id=self.current_deck_id, question=question, answer=answer
            )
            self.frame.clear_inputs()
            self.refresh_cards()
        except ValueError as exc:
            self.frame.set_message(str(exc))

    def update_card(self) -> None:
        card = self._selected_card()
        if not card:
            self.frame.set_message("Select a card to update.")
            return
        question = self.frame.question_input.get("1.0", END).strip()
        answer = self.frame.answer_input.get("1.0", END).strip()
        try:
            user_id = self._require_user()
            self.model.decks.update_card(
                user_id=user_id, card_id=card.id, question=question, answer=answer
            )
            self.refresh_cards()
        except ValueError as exc:
            self.frame.set_message(str(exc))

    def delete_card(self) -> None:
        card = self._selected_card()
        if not card:
            self.frame.set_message("Select a card to delete.")
            return
        if messagebox.askyesno("Delete Card", "Delete this card?"):
            try:
                user_id = self._require_user()
                self.model.decks.delete_card(user_id=user_id, card_id=card.id)
                self.refresh_cards()
            except ValueError as exc:
                self.frame.set_message(str(exc))

    def on_card_select(self, event) -> None:
        card = self._selected_card()
        if not card:
            return
        self.frame.question_input.delete("1.0", END)
        self.frame.question_input.insert("1.0", card.question)
        self.frame.answer_input.delete("1.0", END)
        self.frame.answer_input.insert("1.0", card.answer)

    def start_study(self) -> None:
        if not self.study_controller or self.current_deck_id is None:
            self.frame.set_message("Study controller unavailable.")
            return
        deck = self.model.decks.get_deck(
            user_id=self._require_user(), deck_id=self.current_deck_id
        )
        self.study_controller.start(deck_id=self.current_deck_id, deck_name=deck.name)
        self.view.switch("study")

    def back_to_decks(self) -> None:
        self.view.switch("deck_list")
