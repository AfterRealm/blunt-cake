"""Simple in-memory cache with TTL — Version 1"""
import time
import threading

_cache = {}
_lock = threading.Lock()


def get(key):
    """Get a value from the cache. Returns None if expired or missing."""
    with _lock:
        if key not in _cache:
            return None
        value, expires = _cache[key]
        if time.time() > expires:
            del _cache[key]
            return None
        return value


def set(key, value, ttl=300):
    """Set a value with a TTL in seconds."""
    with _lock:
        _cache[key] = (value, time.time() + ttl)


def delete(key):
    """Delete a key from the cache."""
    with _lock:
        if key in _cache:
            del _cache[key]


def clear():
    """Clear all cached values."""
    global _cache
    with _lock:
        _cache = {}


def cleanup():
    """Remove all expired entries."""
    now = time.time()
    with _lock:
        expired = [k for k, (v, exp) in _cache.items() if now > exp]
        for k in expired:
            del _cache[k]
    return len(expired)


def stats():
    """Return cache statistics."""
    with _lock:
        total = len(_cache)
        now = time.time()
        alive = sum(1 for v, exp in _cache.values() if now <= exp)
        return {"total": total, "alive": alive, "expired": total - alive}
