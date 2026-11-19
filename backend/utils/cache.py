"""
Simple in-memory thread-safe TTL cache with bounded capacity and proactive eviction.
"""
import time
import threading
from typing import Any, Optional, Dict

class SimpleTTLCache:
    def __init__(self, ttl_seconds: int = 900, max_size: int = 1000):
        self.ttl = ttl_seconds
        self.max_size = max_size
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._cache.get(key)
            if not entry:
                return None
            if time.time() > entry["expiry"]:
                del self._cache[key]
                return None
            return entry["value"]

    def set(self, key: str, value: Any, custom_ttl: Optional[int] = None) -> None:
        duration = custom_ttl if custom_ttl is not None else self.ttl
        now = time.time()
        with self._lock:
            # If cache exceeds max size, purge expired items
            if len(self._cache) >= self.max_size:
                expired = [k for k, v in self._cache.items() if now > v["expiry"]]
                for k in expired:
                    del self._cache[k]
                
                # If still at or over capacity, remove oldest entry (FIFO)
                if len(self._cache) >= self.max_size:
                    oldest_key = next(iter(self._cache))
                    del self._cache[oldest_key]

            self._cache[key] = {
                "value": value,
                "expiry": now + duration
            }

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        with self._lock:
            return len(self._cache)
