# -*- coding: utf-8 -*-
from tkinter import Button, Entry, Frame, Label, StringVar


__author__ = 'fenzl, ahsan'


class SignInView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = Label(self, text="Sign In with existing account")
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.username_var = StringVar()
        self.username_label = Label(self, text="Username")
        self.username_input = Entry(self, textvariable=self.username_var)
        self.username_label.grid(row=1, column=0, padx=10, sticky="w")
        self.username_input.grid(row=1, column=1, padx=(0, 20), sticky="ew")

        self.password_var = StringVar()
        self.password_label = Label(self, text="Password")
        self.password_input = Entry(self, show="*", textvariable=self.password_var)
        self.password_label.grid(row=2, column=0, padx=10, sticky="w")
        self.password_input.grid(row=2, column=1, padx=(0, 20), sticky="ew")

        self.signin_btn = Button(self, text="Sign In")
        self.signin_btn.grid(row=3, column=1, padx=0, pady=10, sticky="w")

        self.signup_option_label = Label(self, text="Don't have an account?")
        self.signup_btn = Button(self, text="Sign Up")
        self.signup_option_label.grid(row=4, column=1, sticky="w")
        self.signup_btn.grid(row=5, column=1, sticky="w")

    # Field accessors
    def get_username(self) -> str:
        return self.username_var.get()

    def set_username(self, value: str) -> None:
        self.username_var.set(value)

    def get_password(self) -> str:
        return self.password_var.get()

    def set_password(self, value: str) -> None:
        self.password_var.set(value)

    # Actions
    def set_signin_command(self, command) -> None:
        self.signin_btn.config(command=command)

    def set_signup_command(self, command) -> None:
        self.signup_btn.config(command=command)

    def clear_inputs(self) -> None:
        self.username_var.set("")
        self.password_var.set("")

    def focus_username(self) -> None:
        self.username_input.focus_set()
