#!/usr/bin/env python3
""" create a connection with redis database """
import redis
import uuid
from typing import Union, Callable
from functools import wraps


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(method: Callable) -> Callable:
        counts = {}

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            counts[key] = counts.get(key, 0) + 1
            self._redis.set(key, counts[key])
            return method(self, *args, **kwargs)

        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union
    [str, bytes, int, float, None]:
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=int)
