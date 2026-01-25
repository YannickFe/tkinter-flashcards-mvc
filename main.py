from controllers.main import MainController
from models.main import MainModel
from views.main import MainView


def main():
    main_model = MainModel()
    main_view = MainView()
    main_controller = MainController(main_model=main_model, main_view=main_view)
    main_controller.start()


if __name__ == "__main__":
    main()
