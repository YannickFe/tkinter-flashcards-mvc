from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///app.db"

# SQLite needs check_same_thread disabled because Tkinter callbacks run on the main thread
# but sessions may be created in different controller contexts.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, future=True, echo=False
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


def init_db() -> None:
    # Imported late to avoid circular imports
    from .user import UserRecord

    Base.metadata.create_all(bind=engine)
