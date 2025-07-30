import pytest
from shared_architecture.utils.data_adapter_redis import bulk_set, bulk_get

@pytest.fixture
def redis_client():
    from shared_architecture.connections.redis_client import get_redis_client
    return get_redis_client()

def test_bulk_set_and_get(redis_client):
    data = {"key1": "value1", "key2": "value2"}

    # Perform bulk set
    bulk_set(redis_client, data, batch_size=2, log_progress=True)

    # Perform bulk get
    keys = list(data.keys())
    result = bulk_get(redis_client, keys, batch_size=2)

    # Assert results match expected values
    assert result["key1"] == b"value1"
    assert result["key2"] == b"value2"
