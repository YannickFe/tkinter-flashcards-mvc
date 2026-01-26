# -*- coding: utf-8 -*-
from tkinter import messagebox

from models.main import MainModel
from views.main import MainView


__author__ = 'fenzl, ahsan'


class SignInController:
    def __init__(self, main_model: MainModel, main_view: MainView) -> None:
        self.main_model = main_model
        self.main_view = main_view
        self.frame = self.main_view.frames["signin"]
        self._bind()

    def _bind(self) -> None:
        """Binds controller functions with respective buttons in the view"""
        self.frame.set_signin_command(self.signin)
        self.frame.set_signup_command(self.signup)

    def signup(self) -> None:
        self.main_view.switch(name="signup")

    def signin(self) -> None:
        username = self.frame.get_username()
        password = self.frame.get_password()
        try:
            self.main_model.auth.authenticate(username=username, password=password)
        except ValueError as exception:
            messagebox.showerror("Sign In Failed", str(exception))
            return

        self.frame.clear_inputs()
        self.frame.focus_username()
        messagebox.showinfo("Success", f"Signed in as {username}.")
