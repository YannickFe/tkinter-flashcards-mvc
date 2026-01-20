from tkinter import messagebox

from models.main import MainModel
from views.main import MainView


class SignUpController:
    def __init__(self, main_model: MainModel, main_view: MainView):
        self.main_model = main_model
        self.main_view = main_view
        self.frame = self.main_view.frames["signup"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.signup_btn.config(command=self.signup)
        self.frame.signin_btn.config(command=self.signin)

    def signin(self) -> None:
        self.main_view.switch("signin")

    def signup(self) -> None:
        data = {
            "fullname": self.frame.fullname_input.get(),
            "username": self.frame.username_input.get(),
            "password": self.frame.password_input.get(),
            "has_agreed": self.frame.has_agreed.get(),
        }
        if not data["has_agreed"]:
            messagebox.showerror("Sign Up Failed", "You must accept the Terms & Conditions.")
            return

        try:
            self.main_model.auth.register_user(
                username=data["username"],
                full_name=data["fullname"],
                password=data["password"],
            )
        except ValueError as exception:
            messagebox.showerror("Sign Up Failed", str(exception))
            return

        self.clear_form()
        messagebox.showinfo("Success", "Account created and signed in.")
        
    
    def clear_form(self) -> None:
        fullname = self.frame.fullname_input.get()
        username = self.frame.username_input.get()
        password = self.frame.password_input.get()
        self.frame.fullname_input.delete(0, last=len(fullname))
        self.frame.fullname_input.focus()
        self.frame.username_input.delete(0, last=len(username))
        self.frame.password_input.delete(0, last=len(password))

        self.frame.has_agreed.set(False)
