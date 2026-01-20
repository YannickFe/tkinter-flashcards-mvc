from controllers.card_form import CardFormController
from controllers.deck_detail import DeckDetailController
from controllers.deck_form import DeckFormController
from controllers.deck_list import DeckListController
from controllers.home import HomeController
from controllers.signin import SignInController
from controllers.signup import SignUpController
from controllers.study import StudyController
from models.main import MainModel
from models.user import UserService
from views.main import MainView


class MainController:
    def __init__(self, main_model: MainModel, main_view: MainView) -> None:
        # Root wiring: build controllers, then cross-link dependencies (list/detail/forms/study).
        self.main_view = main_view
        self.main_model = main_model
        self.signin_controller = SignInController(main_model, main_view)
        self.signup_controller = SignUpController(main_model, main_view)
        self.deck_list_controller = DeckListController(main_model, main_view)
        self.deck_detail_controller = DeckDetailController(main_model, main_view)
        self.study_controller = StudyController(main_model, main_view)
        self.deck_form_controller = DeckFormController(
            main_model, main_view, deck_list_controller=self.deck_list_controller
        )
        self.card_form_controller = CardFormController(
            main_model, main_view, deck_detail_controller=self.deck_detail_controller
        )
        self.home_controller = HomeController(
            main_model, main_view, deck_list_controller=self.deck_list_controller
        )

        # Cross-wire navigation and forms.
        self.deck_list_controller.set_detail_controller(self.deck_detail_controller)
        self.deck_list_controller.set_form_controller(self.deck_form_controller)
        self.deck_detail_controller.set_study_controller(self.study_controller)
        self.deck_detail_controller.set_card_form_controller(self.card_form_controller)
        self.study_controller.set_detail_controller(self.deck_detail_controller)

        # React to auth state changes (login/logout).
        self.main_model.auth.add_event_listener("auth_changed", self.auth_state_listener)

    def auth_state_listener(self, data: UserService) -> None:
        if data.is_logged_in:
            if data.current_user:
                self.main_model.decks.seed_sample(data.current_user.id)
            self.deck_list_controller.refresh()
            self.home_controller.update_view()
            self.main_view.switch("home")
        else:
            self.main_view.switch("signin")

    def start(self) -> None:
        # Here, you can do operations required before launching the gui, for example,
        # self.model.auth.load_auth_state()
        if self.main_model.auth.is_logged_in:
            self.main_view.switch("home")
        else:
            self.main_view.switch("signin")

        self.main_view.start_mainloop()
