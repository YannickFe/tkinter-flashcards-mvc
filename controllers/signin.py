from tkinter import messagebox

from models.main import Model
from views.main import View


class SignInController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["signin"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.signin_btn.config(command=self.signin)
        self.frame.signup_btn.config(command=self.signup)

    def signup(self) -> None:
        self.view.switch("signup")

    def signin(self) -> None:
        username = self.frame.username_input.get()
        password = self.frame.password_input.get()
        try:
            self.model.auth.authenticate(username=username, password=password)
        except ValueError as exc:
            messagebox.showerror("Sign In Failed", str(exc))
            return

        self.frame.password_input.delete(0, last=len(password))
        messagebox.showinfo("Success", f"Signed in as {username}.")
