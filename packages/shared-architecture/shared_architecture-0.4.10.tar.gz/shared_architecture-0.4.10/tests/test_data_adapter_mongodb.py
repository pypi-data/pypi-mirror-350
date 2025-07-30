import pytest
from pymongo import MongoClient
from shared_architecture.utils.data_adapter_mongodb import bulk_insert, bulk_update

@pytest.fixture
def mongo_collection():
    from shared_architecture.connections.mongodb_client import get_mongo_client
    client = get_mongo_client()
    return client.get_collection("test_collection")

def test_bulk_insert_and_update(mongo_collection):
    documents = [{"_id": "doc1", "field": "value1"}, {"_id": "doc2", "field": "value2"}]

    # Perform bulk insert
    bulk_insert(mongo_collection, documents, batch_size=2, log_progress=True)

    # Prepare updates
    updates = [{"filter": {"_id": "doc1"}, "update": {"$set": {"field": "updated_value1"}}}]

    # Perform bulk update
    bulk_update(mongo_collection, updates, log_progress=True)

    # Verify updates
    updated_doc = mongo_collection.find_one({"_id": "doc1"})
    assert updated_doc["field"] == "updated_value1"
