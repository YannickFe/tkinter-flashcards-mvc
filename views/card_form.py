from tkinter import Frame, Label, Text, Button, StringVar


class CardFormView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.title_var = StringVar()
        self.title_label = Label(self, textvariable=self.title_var)
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.question_label = Label(self, text="Question")
        self.question_label.grid(row=1, column=0, padx=10, sticky="w")
        self.question_input = Text(self, height=4, width=40)
        self.question_input.grid(row=1, column=1, padx=(0, 20), pady=4, sticky="ew")

        self.answer_label = Label(self, text="Answer")
        self.answer_label.grid(row=2, column=0, padx=10, sticky="w")
        self.answer_input = Text(self, height=4, width=40)
        self.answer_input.grid(row=2, column=1, padx=(0, 20), pady=4, sticky="ew")

        self.save_btn = Button(self, text="Save")
        self.save_btn.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.cancel_btn = Button(self, text="Cancel")
        self.cancel_btn.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.message_var = StringVar()
        self.message_label = Label(self, textvariable=self.message_var, fg="red")
        self.message_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    def set_title(self, title: str) -> None:
        self.title_var.set(title)

    def set_message(self, message: str) -> None:
        self.message_var.set(message)

    def clear_inputs(self) -> None:
        self.question_input.delete("1.0", "end")
        self.answer_input.delete("1.0", "end")
