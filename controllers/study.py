from typing import Optional, TYPE_CHECKING

from controllers.utils import require_user_id
from models.deck import CardData
from models.main import MainModel
from views.main import MainView

if TYPE_CHECKING:
    from controllers.deck_detail import DeckDetailController


class StudyController:
    def __init__(self, main_model: MainModel, main_view: MainView):
        self.main_model = main_model
        self.main_view = main_view
        self.frame = self.main_view.frames["study"]
        self.deck_detail_controller: "DeckDetailController | None" = None
        self.current_deck_id: int | None = None
        self.current_deck_name: str = ""
        self.current_card: Optional[CardData] = None
        self._bind()

    def set_detail_controller(self, controller: "DeckDetailController") -> None:
        self.deck_detail_controller = controller

    def _bind(self) -> None:
        self.frame.show_answer_btn.config(command=self.show_answer)
        self.frame.memorized_btn.config(command=lambda: self.rate_card(1))
        self.frame.not_memorized_btn.config(command=lambda: self.rate_card(-1))
        self.frame.back_btn.config(command=self.back_to_deck)

    def start(self, deck_id: int, deck_name: str) -> None:
        self.current_deck_id = deck_id
        self.current_deck_name = deck_name
        self.frame.set_deck_title(deck_name)
        self.frame.set_message("")
        self.load_next_card()

    def load_next_card(self) -> None:
        if self.current_deck_id is None:
            self.frame.set_message("No deck selected.")
            return
        try:
            user_id = require_user_id(self.main_model.auth)
            card = self.main_model.decks.next_card_for_study(
                user_id=user_id, deck_id=self.current_deck_id
            )
            self.current_card = card
            if not card:
                self.frame.set_message("No cards to study in this deck.")
                self.frame.clear_card()
                return
            self.frame.set_message("")
            self.frame.question_var.set(f"Q: {card.question}")
            self.frame.answer_var.set("")
        except ValueError as exception:
            self.frame.set_message(str(exception))

    def show_answer(self) -> None:
        if not self.current_card:
            return
        self.frame.answer_var.set(f"A: {self.current_card.answer}")

    def rate_card(self, delta: int) -> None:
        if not self.current_card:
            self.frame.set_message("No card selected.")
            return
        if self.current_deck_id is None:
            self.frame.set_message("No deck selected.")
            return
        try:
            user_id = require_user_id(self.main_model.auth)
            updated = self.main_model.decks.update_score(
                user_id=user_id, card_id=self.current_card.id, delta=delta
            )
            self.frame.set_message(f"Updated score: {updated.score}")
            self.load_next_card()
        except ValueError as exception:
            self.frame.set_message(str(exception))

    def back_to_deck(self) -> None:
        # load the current deck so scores are updated
        if self.deck_detail_controller and self.current_deck_id is not None:
            try:
                self.deck_detail_controller.load_deck(self.current_deck_id)
            except ValueError as exception:
                self.frame.set_message(str(exception))
                return
        self.main_view.switch("deck_detail")
