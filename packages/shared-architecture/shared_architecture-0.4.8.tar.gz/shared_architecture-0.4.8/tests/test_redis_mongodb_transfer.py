import pytest
from shared_architecture.utils.redis_mongodb_transfer import redis_to_mongodb, mongodb_to_redis

@pytest.fixture
def redis_client():
    from shared_architecture.connections.redis_client import get_redis_client
    return get_redis_client()

@pytest.fixture
def mongo_collection():
    from shared_architecture.connections.mongodb_client import get_mongo_client
    client = get_mongo_client()
    return client.get_collection("test_transfer_collection")

def test_redis_to_mongodb_transfer(redis_client, mongo_collection):
    redis_client.set("mongo_transfer_key1", "mongo_value1")
    redis_client.set("mongo_transfer_key2", "mongo_value2")

    keys = ["mongo_transfer_key1", "mongo_transfer_key2"]
    redis_to_mongodb(redis_client, mongo_collection, keys, batch_size=2, log_progress=True)

    assert mongo_collection.find_one({"redis_key": "mongo_transfer_key1"}) is not None
    assert mongo_collection.find_one({"redis_key": "mongo_transfer_key2"}) is not None

def test_mongodb_to_redis_transfer(redis_client, mongo_collection):
    mongo_collection.insert_many([
        {"redis_key": "mongo_back_key1", "value": "back_value1"},
        {"redis_key": "mongo_back_key2", "value": "back_value2"}
    ])

    mongodb_to_redis(mongo_collection, redis_client, "redis_key", "value", filter_query={}, batch_size=2, log_progress=True)

    assert redis_client.get("mongo_back_key1") is not None
    assert redis_client.get("mongo_back_key2") is not None
