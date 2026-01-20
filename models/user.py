from dataclasses import dataclass
from typing import Optional

from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.observable import ObservableModel
from models.storage import Base
from models.storage import SessionLocal, init_db


class UserRecord(Base):
    """ORM table for users (persisted in SQLite)."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)


@dataclass
class UserData:
    id: int
    username: str
    full_name: str

    def __repr__(self) -> str:
        return f"UserData(id={self.id}, username={self.username!r}, full_name={self.full_name!r})"


class UserService(ObservableModel):
    def __init__(self):
        super().__init__()
        init_db()
        self.is_logged_in = False
        self.current_user: UserData | None = None

    def _log(self, message: str) -> None:
        print(f"[UserService] {message}")

    def _hash_password(self, password: str) -> str:
        """Hash with bcrypt; salt is embedded in the returned hash."""
        hashed = hashpw(password.encode("utf-8"), gensalt())
        return hashed.decode("utf-8")

    def _verify_password(self, password: str, hashed: str) -> bool:
        """Check plaintext against stored bcrypt hash."""
        return checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

    def _get_session(self) -> Session:
        return SessionLocal()

    def register_user(self, username: str, full_name: str, password: str) -> UserData:
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

        user_data = UserData(id=user.id, username=user.username, full_name=user.full_name)
        self._log(f"Registered user {user_data}")
        self.login(user_data)
        return user_data

    def authenticate(self, username: str, password: str) -> UserData:
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

        user_data = UserData(id=user.id, username=user.username, full_name=user.full_name)
        self.login(user_data)
        return user_data

    def login(self, user: UserData) -> None:
        self.is_logged_in = True
        self.current_user = user
        self.trigger_event("auth_changed")
        self._log(f"Logged in user {user}")

    def logout(self) -> None:
        self.is_logged_in = False
        self.current_user = None
        self.trigger_event("auth_changed")
        self._log("Logged out")
