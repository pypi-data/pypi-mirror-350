import pytest
from shared_architecture.utils.redis_timescaledb_transfer import redis_to_timescaledb, timescaledb_to_redis
from shared_architecture.sqlalchemy_model_factory import generate_dynamic_model
from pydantic import BaseModel

@pytest.fixture
def redis_client():
    from shared_architecture.connections.redis_client import get_redis_client
    return get_redis_client()

@pytest.fixture
def session():
    from shared_architecture.connections.timescaledb_client import get_timescaledb_session
    return get_timescaledb_session()

@pytest.fixture
def test_model():
    fields = {"redis_key": "str", "value": "str"}
    return generate_dynamic_model("test_transfer_table", fields)

class TestSchema(BaseModel):
    redis_key: str
    value: str

def test_redis_to_timescaledb_transfer(redis_client, session, test_model):
    redis_client.set("transfer_key1", "transfer_value1")
    redis_client.set("transfer_key2", "transfer_value2")

    keys = ["transfer_key1", "transfer_key2"]
    redis_to_timescaledb(redis_client, session, test_model, keys, TestSchema, batch_size=2, log_progress=True)


def test_timescaledb_to_redis_transfer(redis_client, session, test_model):
    query = f"SELECT redis_key, value FROM {test_model.__tablename__}"
    timescaledb_to_redis(session, query, redis_client, "redis_key", "value", batch_size=2, log_progress=True)

    assert redis_client.get("transfer_key1") is not None
    assert redis_client.get("transfer_key2") is not None
