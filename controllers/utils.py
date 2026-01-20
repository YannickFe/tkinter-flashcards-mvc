from models.auth import Auth


def require_user_id(auth: Auth) -> int:
    """Return the current user id or raise if nobody is signed in."""
    user = auth.current_user
    if not user:
        raise ValueError("You must be signed in.")
    return user["id"]


def truncate_and_pad(text: str, width: int) -> str:
    """Clamp text to width with ellipsis and pad to fixed size."""
    if len(text) > width:
        text = text[: max(0, width - 3)] + "..."
    return text.ljust(width)
