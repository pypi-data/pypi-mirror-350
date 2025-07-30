from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from shared_architecture.config.config_loader import config_loader

DB_HOST = config_loader.get("TIMESCALEDB_HOST", "localhost")
DB_PORT = config_loader.get("TIMESCALEDB_PORT", "5432")
DB_NAME = config_loader.get("TIMESCALEDB_DATABASE", "timescale")
DB_USER = config_loader.get("TIMESCALEDB_USER", "postgres")
DB_PASSWORD = config_loader.get("TIMESCALEDB_PASSWORD", "password")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class TimescaleDBClient:
    def __init__(self):
        try:
            self.engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        except SQLAlchemyError as e:
            raise ConnectionError(f"Failed to connect to TimescaleDB at {DATABASE_URL}") from e

    def get_session(self):
        return self.SessionLocal()

    def close(self):
        self.engine.dispose()
    def health_check(self):
        try:
            with self.get_session() as session:
                session.execute("SELECT 1")
            return True
        except Exception:
            return False

# Singleton pattern
_timescaledb_client = TimescaleDBClient()

def get_timescaledb_session():
    return _timescaledb_client.get_session()
