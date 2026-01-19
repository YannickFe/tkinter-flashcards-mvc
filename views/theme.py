from tkinter import ttk, Tk


def configure_theme(root: Tk) -> None:
    """Pick a simple built-in theme; prefer Aquativo/Adapta if present, else clam."""
    style = ttk.Style(root)
    preferred = ["aquativo", "Aquativo", "adapta", "Adapta", "clam"]
    available = style.theme_names()
    for candidate in preferred:
        if candidate in available:
            style.theme_use(candidate)
            break
    else:
        style.theme_use(available[0])

    # Make sure hierarchy is differentiable.
    style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))
    style.configure("Subheader.TLabel", font=("Helvetica", 12, "bold"))
