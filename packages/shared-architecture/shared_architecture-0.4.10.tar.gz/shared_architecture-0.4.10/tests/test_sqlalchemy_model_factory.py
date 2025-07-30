from shared_architecture.utils.sqlalchemy_model_factory import generate_dynamic_model
from sqlalchemy.orm import Session
import pytest

@pytest.fixture
def session():
    from shared_architecture.connections.timescaledb_client import get_timescaledb_session
    return get_timescaledb_session()

def test_generate_dynamic_model(session: Session):
    fields = {"symbol": "str", "price": "int"}
    DynamicModel = generate_dynamic_model("dynamic_test_table", fields)

    instance = DynamicModel(symbol="AAPL", price=150)

    # Insert the instance
    session.add(instance)
    session.commit()

    # Query to check existence
    query_result = session.query(DynamicModel).filter_by(symbol="AAPL").first()
    assert query_result is not None
    assert query_result.symbol == "AAPL"
    assert query_result.price == 150