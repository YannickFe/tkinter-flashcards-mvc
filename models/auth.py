import hashlib
import secrets
from typing import Optional, TypedDict, Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .base import ObservableModel
from .storage import SessionLocal, init_db
from .user import UserRecord


class User(TypedDict):
    username: str
    full_name: str


class Auth(ObservableModel):
    def __init__(self):
        super().__init__()
        init_db()
        self.is_logged_in = False
        self.current_user: Union[User, None] = None

    def _hash_password(self, password: str, salt: str) -> str:
        return hashlib.sha256(f"{salt}{password}".encode("utf-8")).hexdigest()

    def _get_session(self) -> Session:
        return SessionLocal()

    def register_user(self, username: str, full_name: str, password: str) -> User:
        if not username or not password or not full_name:
            raise ValueError("Full name, username, and password are required.")

        salt = secrets.token_hex(16)
        password_hash = self._hash_password(password, salt)
        with self._get_session() as session:
            user = UserRecord(
                username=username,
                full_name=full_name,
                password_hash=password_hash,
                password_salt=salt,
            )
            session.add(user)
            try:
                session.commit()
            except IntegrityError as exc:
                session.rollback()
                raise ValueError("Username already exists.") from exc
            session.refresh(user)

        self.login({"username": user.username, "full_name": user.full_name})
        return {"username": user.username, "full_name": user.full_name}

    def authenticate(self, username: str, password: str) -> User:
        if not username or not password:
            raise ValueError("Username and password are required.")

        with self._get_session() as session:
            user: Optional[UserRecord] = (
                session.query(UserRecord).filter(UserRecord.username == username).first()
            )

        if not user:
            raise ValueError("Invalid username or password.")

        password_hash = self._hash_password(password, user.password_salt)
        if password_hash != user.password_hash:
            raise ValueError("Invalid username or password.")

        self.login({"username": user.username, "full_name": user.full_name})
        return {"username": user.username, "full_name": user.full_name}

    def login(self, user: User) -> None:
        self.is_logged_in = True
        self.current_user = user
        self.trigger_event("auth_changed")

    def logout(self) -> None:
        self.is_logged_in = False
        self.current_user = None
        self.trigger_event("auth_changed")
