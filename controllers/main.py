from controllers.card_form import CardFormController
from controllers.deck_detail import DeckDetailController
from controllers.deck_form import DeckFormController
from controllers.deck_list import DeckListController
from controllers.home import HomeController
from controllers.signin import SignInController
from controllers.signup import SignUpController
from controllers.study import StudyController
from models.auth import Auth
from models.main import Model
from views.main import View


class Controller:
    def __init__(self, model: Model, view: View) -> None:
        # Root wiring: build controllers, then cross-link dependencies (list/detail/forms/study).
        self.view = view
        self.model = model
        self.signin_controller = SignInController(model, view)
        self.signup_controller = SignUpController(model, view)
        self.deck_list_controller = DeckListController(model, view)
        self.deck_detail_controller = DeckDetailController(model, view)
        self.study_controller = StudyController(model, view)
        self.deck_form_controller = DeckFormController(
            model, view, deck_list_controller=self.deck_list_controller
        )
        self.card_form_controller = CardFormController(
            model, view, deck_detail_controller=self.deck_detail_controller
        )
        self.home_controller = HomeController(
            model, view, deck_list_controller=self.deck_list_controller
        )

        # Cross-wire navigation and forms.
        self.deck_list_controller.set_detail_controller(self.deck_detail_controller)
        self.deck_list_controller.set_form_controller(self.deck_form_controller)
        self.deck_detail_controller.set_study_controller(self.study_controller)
        self.deck_detail_controller.set_card_form_controller(self.card_form_controller)

        # React to auth state changes (login/logout).
        self.model.auth.add_event_listener("auth_changed", self.auth_state_listener)

    def auth_state_listener(self, data: Auth) -> None:
        if data.is_logged_in:
            if data.current_user:
                self.model.decks.seed_sample(data.current_user["id"])
            self.deck_list_controller.refresh()
            self.home_controller.update_view()
            self.view.switch("home")
        else:
            self.view.switch("signin")

    def start(self) -> None:
        # Here, you can do operations required before launching the gui, for example,
        # self.model.auth.load_auth_state()
        if self.model.auth.is_logged_in:
            self.view.switch("home")
        else:
            self.view.switch("signin")

        self.view.start_mainloop()
