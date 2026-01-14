from models.main import Model
from views.main import View


class HomeController:
    def __init__(self, model: Model, view: View, deck_list_controller) -> None:
        self.model = model
        self.view = view
        self.deck_list_controller = deck_list_controller
        self.frame = self.view.frames["home"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.signout_btn.config(command=self.logout)
        self.frame.deck_btn.config(command=self.switch_to_decks)

    def logout(self) -> None:
        self.model.auth.logout()

    def switch_to_decks(self) -> None:
        self.deck_list_controller.refresh()
        self.view.switch("deck_list")

    def update_view(self) -> None:
        current_user = self.model.auth.current_user
        if current_user:
            name = current_user.get("full_name") or current_user["username"]
            self.frame.greeting.config(text=f"Welcome, {name}!")
        else:
            self.frame.greeting.config(text=f"")
