from models.main import MainModel
from views.main import MainView


class HomeController:
    def __init__(self, main_model: MainModel, main_view: MainView, deck_list_controller) -> None:
        self.main_model = main_model
        self.main_view = main_view
        self.deck_list_controller = deck_list_controller
        self.frame = self.main_view.frames["home"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.signout_btn.config(command=self.logout)
        self.frame.deck_btn.config(command=self.switch_to_decks)

    def logout(self) -> None:
        self.main_model.auth.logout()

    def switch_to_decks(self) -> None:
        self.deck_list_controller.refresh()
        self.main_view.switch("deck_list")

    def update_view(self) -> None:
        current_user = self.main_model.auth.current_user
        if current_user:
            name = current_user.get("full_name") or current_user["username"]
            self.frame.greeting.config(text=f"Welcome, {name}!")
        else:
            self.frame.greeting.config(text=f"")
