from typing import Optional, TypedDict, Union

import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.observable import ObservableModel
from models.storage import SessionLocal, init_db
from models.user import UserRecord


class User(TypedDict):
    id: int
    username: str
    full_name: str


class Auth(ObservableModel):
    def __init__(self):
        super().__init__()
        init_db()
        self.is_logged_in = False
        self.current_user: Union[User, None] = None

    def _hash_password(self, password: str) -> str:
        """Hash with bcrypt; salt is embedded in the returned hash."""
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    def _verify_password(self, password: str, hashed: str) -> bool:
        """Check plaintext against stored bcrypt hash."""
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

    def _get_session(self) -> Session:
        return SessionLocal()

    def register_user(self, username: str, full_name: str, password: str) -> User:
        if not username or not password or not full_name:
            raise ValueError("Full name, username, and password are required.")

        password_hash = self._hash_password(password)
        with self._get_session() as session:
            user = UserRecord(
                username=username,
                full_name=full_name,
                password_hash=password_hash,
            )
            session.add(user)
            try:
                session.commit()
            except IntegrityError as exception:
                session.rollback()
                raise ValueError("Username already exists.") from exception
            session.refresh(user)

        self.login({"id": user.id, "username": user.username, "full_name": user.full_name})
        return {"id": user.id, "username": user.username, "full_name": user.full_name}

    def authenticate(self, username: str, password: str) -> User:
        if not username or not password:
            raise ValueError("Username and password are required.")

        with self._get_session() as session:
            user: Optional[UserRecord] = (
                session.query(UserRecord).filter(UserRecord.username == username).first()
            )

        if not user:
            raise ValueError("Invalid username or password.")

        if not self._verify_password(password, user.password_hash):
            raise ValueError("Invalid username or password.")

        self.login({"id": user.id, "username": user.username, "full_name": user.full_name})
        return {"id": user.id, "username": user.username, "full_name": user.full_name}

    def login(self, user: User) -> None:
        self.is_logged_in = True
        self.current_user = user
        self.trigger_event("auth_changed")

    def logout(self) -> None:
        self.is_logged_in = False
        self.current_user = None
        self.trigger_event("auth_changed")
