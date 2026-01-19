from tkinter import Tk
from views.theme import configure_theme


class Root(Tk):
    """
    Root class for initializing the main application window.

    This class extends the Tk class to provide an entry point for our GUI application.
     It initializes the main application window with specific dimensions,
     a title, and layout configuration.
    """
    def __init__(self):
        super().__init__()

        configure_theme(self)
        start_width = 500
        min_width = 400
        start_height = 300
        min_height = 250

        self.geometry(f"{start_width}x{start_height}")
        self.minsize(width=min_width, height=min_height)
        self.title("TKinter MVC Multi-frame GUI")
        # Give row/col 0 stretch weight so stacked frames fill and grow with the window.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
