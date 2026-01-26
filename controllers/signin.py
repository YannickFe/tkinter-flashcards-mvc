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
        self.frame.signin_btn.config(command=self.signin)
        self.frame.signup_btn.config(command=self.signup)

    def signup(self) -> None:
        self.main_view.switch(name="signup")

    def signin(self) -> None:
        username = self.frame.username_input.get()
        password = self.frame.password_input.get()
        try:
            self.main_model.auth.authenticate(username=username, password=password)
        except ValueError as exception:
            messagebox.showerror("Sign In Failed", str(exception))
            return

        self.frame.password_input.delete(0, last=len(password))
        messagebox.showinfo("Success", f"Signed in as {username}.")
