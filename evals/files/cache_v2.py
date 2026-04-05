"""In-memory cache with TTL, max size, and LRU eviction — Version 2"""
import time
import threading
from collections import OrderedDict


class Cache:
    def __init__(self, max_size=1000, default_ttl=300):
        self._data = OrderedDict()
        self._lock = threading.Lock()
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._hits = 0
        self._misses = 0

    def get(self, key):
        with self._lock:
            if key not in self._data:
                self._misses += 1
                return None
            value, expires = self._data[key]
            if time.time() > expires:
                del self._data[key]
                self._misses += 1
                return None
            self._data.move_to_end(key)
            self._hits += 1
            return value

    def set(self, key, value, ttl=None):
        ttl = ttl or self.default_ttl
        with self._lock:
            if key in self._data:
                self._data.move_to_end(key)
            self._data[key] = (value, time.time() + ttl)
            while len(self._data) > self.max_size:
                self._data.popitem(last=False)

    def delete(self, key):
        with self._lock:
            self._data.pop(key, None)

    def clear(self):
        with self._lock:
            self._data.clear()
            self._hits = 0
            self._misses = 0

    def get_or_set(self, key, factory, ttl=None):
        value = self.get(key)
        if value is not None:
            return value
        value = factory()
        self.set(key, value, ttl)
        return value

    def cleanup(self):
        now = time.time()
        with self._lock:
            expired = [k for k, (v, exp) in self._data.items() if now > exp]
            for k in expired:
                del self._data[k]
        return len(expired)

    def stats(self):
        with self._lock:
            total = len(self._data)
            now = time.time()
            alive = sum(1 for v, exp in self._data.values() if now <= exp)
            total_requests = self._hits + self._misses
            hit_rate = self._hits / total_requests if total_requests else 0
            return {
                "total": total,
                "alive": alive,
                "expired": total - alive,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": round(hit_rate, 3),
                "max_size": self.max_size,
            }
