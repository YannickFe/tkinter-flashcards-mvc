# -*- coding: utf-8 -*-
import unittest

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from models.storage import Base
from models.user import UserRecord


__author__ = 'fenzl'


class DBTestCase(unittest.TestCase):
    """Base test case that provisions an in-memory SQLite DB and session factory."""

    engine: Engine
    session_factory: sessionmaker

    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///:memory:", future=True)
        self.session_factory = sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, future=True
        )
        Base.metadata.create_all(bind=self.engine)

    def tearDown(self) -> None:
        self.engine.dispose()

    def create_user(
            self, username: str = "test", full_name: str = "Test User", password_hash: str = "hash"
    ) -> int:
        """Helper to seed a user for tests; returns the user id."""
        with self.session_factory() as session:
            user = UserRecord(
                username=username,
                full_name=full_name,
                password_hash=password_hash,
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user.id
