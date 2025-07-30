import pytest
from sqlalchemy.orm import Session
from shared_architecture.utils.data_adapter_timescaledb import process_bulk_insert, process_bulk_query
from shared_architecture.sqlalchemy_model_factory import generate_dynamic_model
from pydantic import BaseModel

# Define schema for testing
class TestSchema(BaseModel):
    symbol: str
    price: int

@pytest.fixture
def session():
    from shared_architecture.connections.timescaledb_client import get_timescaledb_session
    return get_timescaledb_session()

@pytest.fixture
def test_model():
    fields = {"symbol": "str", "price": "int"}
    return generate_dynamic_model("test_timescaledb_table", fields)

def test_process_bulk_insert_and_query(session: Session, test_model):
    data = [{"symbol": "AAPL", "price": 150}, {"symbol": "GOOGL", "price": 2800}]

    # Insert data
    process_bulk_insert(session, test_model, TestSchema, data)

    # Query data (adjust query as per your schema and test setup)
    query = f"SELECT * FROM {test_model.__tablename__}"
    results = process_bulk_query(session, query)

    assert isinstance(results, list)
