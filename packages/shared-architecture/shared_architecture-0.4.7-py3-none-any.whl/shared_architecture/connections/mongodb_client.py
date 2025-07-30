from pymongo import MongoClient
from shared_architecture.config.config_loader import config_loader

MONGO_HOST = config_loader.get("MONGODB_HOST", "localhost")
MONGO_PORT = int(config_loader.get("MONGODB_PORT", 27017))
MONGO_USER = config_loader.get("MONGODB_USER", "root")
MONGO_PASSWORD = config_loader.get("MONGODB_PASSWORD", "password")
MONGO_DB_NAME = config_loader.get("MONGODB_DATABASE", "default_db")


class MongoDBClient:
    def __init__(self):
        uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB_NAME}"
        self.client = MongoClient(uri)
        self.db = self.client[MONGO_DB_NAME]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        self.client.close()
    def health_check(self):
        try:
            self.client.admin.command('ping')
            return True
        except Exception:
            return False
# Singleton
_mongo_client = MongoDBClient()

def get_mongo_client():
    return _mongo_client

    except Exception:
        return False
