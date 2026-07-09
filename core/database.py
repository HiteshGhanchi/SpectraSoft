"""
SpectraSoft — Database Configuration
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


def get_db_path() -> str:
    """
    Returns the path to data.db.

    - When running as a packaged .exe, puts it next to the .exe
    - When running as a script during development, puts it in the project root
    """
    if getattr(sys, "frozen", False):
        # Running as compiled .exe
        base_dir = os.path.dirname(sys.executable)
        # print(f"[DB DEBUG] Running as packaged executable.", flush=True)
    else:
        # Running as a script during development
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # print(f"[DB DEBUG] Running in development mode.", flush=True)

    db_path = os.path.join(base_dir, "data.db")
    # print(f"[DB DEBUG] Database path resolved to: {db_path}", flush=True)

    return db_path


DB_PATH = get_db_path()
DATABASE_URL = f"sqlite:///{DB_PATH}"

# print(f"[DB DEBUG] DATABASE_URL = {DATABASE_URL}", flush=True)


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


class Base(DeclarativeBase):
    pass


def init_db():
    """
    Creates all tables if they do not exist yet.

    Called once at application startup.
    Safe to call multiple times.
    It does not delete, overwrite, or reset existing data.
    """
    # print("[DB DEBUG] init_db() started.", flush=True)

    from core import models  # imported here to avoid circular imports

    # print("[DB DEBUG] Models imported successfully.", flush=True)
    # print("[DB DEBUG] Creating tables if not exists...", flush=True)

    Base.metadata.create_all(bind=engine)

    # print("[DB DEBUG] init_db() completed. Tables are ready.", flush=True)


def get_session():
    """
    Returns a new database session.

    Always close it when done:
        session = get_session()
        try:
            ...
        finally:
            session.close()
    """
    # print("[DB DEBUG] New database session created.", flush=True)
    return SessionLocal()