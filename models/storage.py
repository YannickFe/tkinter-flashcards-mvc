# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

__author__ = 'fenzl'

DATABASE_URL = "sqlite:///app.db"

# SQLite needs check_same_thread disabled because Tkinter callbacks run on the main thread,
# but sessions may be created in different controller contexts.
# Using check_same_thread allows multiple threads to use this connection.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, future=True, echo=False
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
# Create a base class for all mapped classes to inherit from
# Enables declarative table definitions using class attributes
Base = declarative_base()


def init_db() -> None:
    # Base.metadata (from declarative_base) collects all mapped tables above; create_all builds them in SQLite if missing.
    Base.metadata.create_all(bind=engine)
