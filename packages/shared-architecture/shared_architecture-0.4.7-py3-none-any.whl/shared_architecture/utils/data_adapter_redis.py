from typing import List, Dict
from redis import Redis
from concurrent.futures import ThreadPoolExecutor
from prometheus_client import Counter
import time
import redis as redis_lib

# Prometheus Metrics
REDIS_BATCH_SUCCESS_COUNT = Counter('redis_bulk_operation_success_total', 'Total successful Redis bulk operations')
REDIS_BATCH_FAILURE_COUNT = Counter('redis_bulk_operation_failure_total', 'Total failed Redis bulk operations')

def retry_with_backoff(fn, retries=3, delay=1):
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay * (2 ** attempt))
            else:
                raise e

def ensure_same_slot(keys: List[str]):
    slots = {redis_lib.crc16(key) % 16384 for key in keys}
    if len(slots) > 1:
        raise ValueError("Keys span multiple Redis hash slots, which is not allowed in multi-key operations.")
    return True

def bulk_set(redis_client: Redis, key_value_pairs: Dict[str, str], parallel: bool = False, batch_size: int = 500, retry_attempts: int = 3, log_progress: bool = False, enforce_same_slot: bool = False):
    items = list(key_value_pairs.items())
    if enforce_same_slot:
        ensure_same_slot([key for key, _ in items])

    batches = [items[i:i + batch_size] for i in range(0, len(items), batch_size)]

    def commit_batch(batch):
        def _commit():
            pipeline = redis_client.pipeline()
            for key, value in batch:
                pipeline.set(key, value)
            pipeline.execute()
            if log_progress:
                print(f"Committed Redis batch of {len(batch)} keys.")
            REDIS_BATCH_SUCCESS_COUNT.inc()
        retry_with_backoff(_commit, retries=retry_attempts)

    if parallel:
        with ThreadPoolExecutor() as executor:
            list(executor.map(commit_batch, batches))
    else:
        for batch in batches:
            try:
                commit_batch(batch)
            except Exception as e:
                REDIS_BATCH_FAILURE_COUNT.inc()
                print(f"Redis batch failed: {e}")

def bulk_get(redis_client: Redis, keys: List[str], batch_size: int = 500, enforce_same_slot: bool = False) -> Dict[str, str]:
    if enforce_same_slot:
        ensure_same_slot(keys)

    result = {}
    batches = [keys[i:i + batch_size] for i in range(0, len(keys), batch_size)]

    for batch in batches:
        pipeline = redis_client.pipeline()
        for key in batch:
            pipeline.get(key)
        values = pipeline.execute()
        result.update(dict(zip(batch, values)))
    return result

def cluster_scan(redis_cluster_client, match="*", count=1000):
    """
    Iterate over all nodes in a Redis Cluster and perform SCAN on each.
    Requires the redis-py client with get_nodes() support.
    """
    try:
        for node in redis_cluster_client.get_nodes():
            node_client = redis_cluster_client.get_node_client(node)
            cursor = 0
            while True:
                cursor, keys = node_client.scan(cursor=cursor, match=match, count=count)
                for key in keys:
                    yield key
                if cursor == 0:
                    break
    except AttributeError:
        raise NotImplementedError("Cluster-wide scan requires client support for get_nodes() and get_node_client().")
