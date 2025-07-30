from typing import Optional
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from shared_architecture.config import ConfigLoader
from shared_architecture.utils.logging_utils import log_info, log_error

DB_HOST = ConfigLoader.get("TIMESCALEDB_HOST", "localhost")
DB_PORT = ConfigLoader.get("TIMESCALEDB_PORT", "5432")
DB_NAME = ConfigLoader.get("TIMESCALEDB_DATABASE", "timescale")
DB_USER = ConfigLoader.get("TIMESCALEDB_USER", "postgres")
DB_PASSWORD = ConfigLoader.get("TIMESCALEDB_PASSWORD", "password")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class TimescaleDBClient:
    """Client for managing TimescaleDB connection lifecycle."""

    def __init__(self):
        db_url = DATABASE_URL
        self.engine = create_engine(db_url, pool_pre_ping=True)
        self.session_factory = sessionmaker(bind=self.engine, class_=Session, expire_on_commit=False)

    def get_session(self) -> Session:
        """Returns a new TimescaleDB session."""
        return self.session_factory()

    def close(self):
        """Closes the database engine."""
        if self.engine:
            self.engine.dispose()
            log_info("TimescaleDB connection closed.")

    def test_connection(self) -> bool:
        """Tests connectivity to the database."""
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
                return True
        except SQLAlchemyError as e:
            log_error(f"TimescaleDB test_connection failed: {e}")
            return False


_ts_client_instance: Optional[TimescaleDBClient] = None

def get_timescaledb_session() -> Session:
    """Returns a reusable session from the global TimescaleDB client."""
    global _ts_client_instance
    if _ts_client_instance is None:
        _ts_client_instance = TimescaleDBClient()
    return _ts_client_instance.get_session()

def close_timescaledb_session() -> None:
    """Closes the shared TimescaleDB session client."""
    global _ts_client_instance
    if _ts_client_instance is not None:
        _ts_client_instance.close()
        _ts_client_instance = None