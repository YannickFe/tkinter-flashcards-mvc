from models.auth import Auth


def require_user_id(auth: Auth) -> int:
    """Return the current user id or raise if nobody is signed in."""
    user = auth.current_user
    if not user:
        raise ValueError("You must be signed in.")
    return user["id"]
