from models.main import Model
from models.deck import DeckData
from views.main import View


class DeckFormController:
    def __init__(self, model: Model, view: View, deck_list_controller):
        self.model = model
        self.view = view
        self.deck_list_controller = deck_list_controller
        self.frame = self.view.frames["deck_form"]
        self.current_deck_id: int | None = None
        self._bind()

    def _require_user(self) -> int:
        user = self.model.auth.current_user
        if not user:
            raise ValueError("You must be signed in.")
        return user["id"]

    def _bind(self) -> None:
        self.frame.save_btn.config(command=self.save)
        self.frame.cancel_btn.config(command=self.cancel)

    def start_create(self) -> None:
        self.current_deck_id = None
        self.frame.set_title("Create Deck")
        self.frame.set_message("")
        self.frame.clear_inputs()
        self.view.switch("deck_form")

    def start_edit(self, deck: DeckData) -> None:
        self.current_deck_id = deck.id
        self.frame.set_title("Edit Deck")
        self.frame.set_message("")
        self.frame.clear_inputs()
        self.frame.name_input.insert(0, deck.name)
        self.frame.desc_input.insert(0, deck.description)
        self.view.switch("deck_form")

    def save(self) -> None:
        name = self.frame.name_input.get().strip()
        desc = self.frame.desc_input.get().strip()
        try:
            user_id = self._require_user()
            if self.current_deck_id is None:
                self.model.decks.create_deck(user_id=user_id, name=name, description=desc)
            else:
                self.model.decks.update_deck(
                    user_id=user_id, deck_id=self.current_deck_id, name=name, description=desc
                )
            self.deck_list_controller.refresh()
            self.view.switch("deck_list")
        except ValueError as exc:
            self.frame.set_message(str(exc))

    def cancel(self) -> None:
        self.view.switch("deck_list")
