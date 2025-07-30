import os
from typing import Optional
from redis.cluster import RedisCluster
from redis.exceptions import RedisError
from shared_architecture.config.config_loader import config_loader

REDIS_CLUSTER_HOST = config_loader.get("REDIS_CLUSTER_HOST", "redis-cluster.default.svc.cluster.local")
REDIS_CLUSTER_PORT = int(config_loader.get("REDIS_CLUSTER_PORT", 6379))


class RedisClusterClient:
    def __init__(self, host: str = REDIS_CLUSTER_HOST, port: int = REDIS_CLUSTER_PORT):
        try:
            self.client = RedisCluster(
                host=host,
                port=port,
                decode_responses=True,
                skip_full_coverage_check=True
            )
        except RedisError as e:
            raise ConnectionError(f"Failed to connect to Redis Cluster at {host}:{port}") from e

    def get_client(self) -> RedisCluster:
        return self.client

    def close(self):
        if self.client:
            self.client.close()

    def health_check(self):
        try:
            self.client.ping()
            return True
        except Exception:
            return False
# Singleton pattern
_redis_cluster_client: Optional[RedisClusterClient] = None

def get_redis_client() -> RedisCluster:
    global _redis_cluster_client
    if _redis_cluster_client is None:
        _redis_cluster_client = RedisClusterClient()
    return _redis_cluster_client.get_client()
