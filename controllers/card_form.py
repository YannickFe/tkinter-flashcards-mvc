from models.deck import CardData
from models.main import Model
from views.main import View


class CardFormController:
    def __init__(self, model: Model, view: View, deck_detail_controller):
        """Handle create/edit of cards via the card form view."""
        self.model = model
        self.view = view
        self.deck_detail_controller = deck_detail_controller
        self.frame = self.view.frames["card_form"]
        self.current_deck_id: int | None = None
        self.current_deck_name: str = ""
        self.current_card_id: int | None = None
        self._bind()

    def _require_user(self) -> int:
        """Guard against anonymous access and return user id."""
        user = self.model.auth.current_user
        if not user:
            raise ValueError("You must be signed in.")
        return user["id"]

    def _bind(self) -> None:
        self.frame.save_btn.config(command=self.save)
        self.frame.cancel_btn.config(command=self.cancel)

    def start_create(self, deck_id: int, deck_name: str) -> None:
        """Open the form in create mode."""
        self.current_deck_id = deck_id
        self.current_deck_name = deck_name
        self.current_card_id = None
        self.frame.set_title(f"Add Card to '{deck_name}'")
        self.frame.set_message("")
        self.frame.clear_inputs()
        self.view.switch("card_form")

    def start_edit(self, deck_id: int, deck_name: str, card: CardData) -> None:
        """Open the form in edit mode for an existing card."""
        self.current_deck_id = deck_id
        self.current_deck_name = deck_name
        self.current_card_id = card.id
        self.frame.set_title(f"Edit Card in '{deck_name}'")
        self.frame.set_message("")
        self.frame.clear_inputs()
        self.frame.question_input.insert("1.0", card.question)
        self.frame.answer_input.insert("1.0", card.answer)
        self.view.switch("card_form")

    def save(self) -> None:
        """Persist changes and return to deck detail."""
        question = self.frame.question_input.get("1.0", "end").strip()
        answer = self.frame.answer_input.get("1.0", "end").strip()
        if self.current_deck_id is None:
            self.frame.set_message("No deck selected.")
            return
        try:
            user_id = self._require_user()
            if self.current_card_id is None:
                self.model.decks.add_card(
                    user_id=user_id, deck_id=self.current_deck_id, question=question, answer=answer
                )
            else:
                self.model.decks.update_card(
                    user_id=user_id, card_id=self.current_card_id, question=question, answer=answer
                )
            self.deck_detail_controller.load_deck(self.current_deck_id)
            self.view.switch("deck_detail")
        except ValueError as exception:
            # Validation errors (empty fields) or missing auth/deck context.
            self.frame.set_message(str(exception))

    def cancel(self) -> None:
        self.view.switch("deck_detail")
