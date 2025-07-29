
import time
from typing import Any


class MemoryCache:

    GLOBAL_INVALIDATION_TIME = 3600  # 1 hour
    _instance = None
    @staticmethod
    def get_instance():
        if not MemoryCache._instance:
            MemoryCache._instance = MemoryCache()
        return MemoryCache._instance

    def __init__(self):
        self.cache = {}

    def set_item(self, prefix_key: str, value: Any, context: Any = None, ttl_seconds: int = GLOBAL_INVALIDATION_TIME):
        if context:
            context = str(context)
            prefix_key = f"{prefix_key}_{context}"

        self.cache[prefix_key] = {"value": value, "timestamp": time.time(), "ttl": ttl_seconds}


    def has_item(self, prefix_key: str, context: Any = None) -> bool:
        if context:
            context = str(context)
            prefix_key = f"{prefix_key}_{context}"

        return prefix_key in self.cache
    

    def get_item(self, prefix_key: str, context: Any = None) -> Any:
        if context:
            context = str(context)
            prefix_key = f"{prefix_key}_{context}"

        item = self.cache.get(prefix_key)
        invalidation_time = item["timestamp"] + item.get("ttl", MemoryCache.GLOBAL_INVALIDATION_TIME)
        if item and invalidation_time > time.time():
            return item["value"]
        return None

    def invalidate_item(self, prefix_key: str, context: Any = None):
        if context:
            context = str(context)
            prefix_key = f"{prefix_key}_{context}"

        self.cache.pop(prefix_key, None)
