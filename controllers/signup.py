# -*- coding: utf-8 -*-
from tkinter import messagebox

from models.main import MainModel
from views.main import MainView


__author__ = 'fenzl, ahsan'


class SignUpController:
    def __init__(self, main_model: MainModel, main_view: MainView):
        self.main_model = main_model
        self.main_view = main_view
        self.frame = self.main_view.frames["signup"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.set_signup_command(self.signup)
        self.frame.set_signin_command(self.signin)

    def signin(self) -> None:
        self.main_view.switch(name="signin")

    def signup(self) -> None:
        data = {
            "fullname": self.frame.get_fullname(),
            "username": self.frame.get_username(),
            "password": self.frame.get_password(),
            "has_agreed": self.frame.get_has_agreed(),
        }
        if not data["has_agreed"]:
            messagebox.showerror("Sign Up Failed", "You must accept the Terms & Conditions.")
            return

        try:
            self.main_model.users.register_user(
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
        self.frame.clear_inputs()
        self.frame.focus_fullname()
