"""
Simple in-memory thread-safe TTL cache.
"""
import time
import threading
from typing import Any, Optional, Dict

class SimpleTTLCache:
    def __init__(self, ttl_seconds: int = 900):  # Default 15 minutes
        self.ttl = ttl_seconds
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
        with self._lock:
            self._cache[key] = {
                "value": value,
                "expiry": time.time() + duration
            }

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
