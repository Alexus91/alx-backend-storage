#!/usr/bin/env python3
""" connection with redis database """
import redis
from uuid import uuid4
from typing import Callable, Optional, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ count method """
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapped  """
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ memorize user actions"""
    method_key = method.__qualname__
    inp = method_key + ':inputs'
    outp = method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ function  wrapped """
        self._redis.rpush(inp, str(args))
        key = method(self, *args, **kwds)
        self._redis.rpush(outp, str(key))
        return key
    return wrapper


def replay(func: Callable) -> None:
    """ Display the history of calls for a particular function """
    method_key = func.__qualname__
    inp = method_key + ':inputs'
    outp = method_key + ':outputs'
    redis = method.__self__._redis
    count = redis.get(method_key).decode("utf-8")
    print("{} was called {} times:".format(method_key, count))
    ListInput = redis.lrange(inp, 0, -1)
    ListOutput = redis.lrange(outp, 0, -1)
    allData = list(zip(ListInput, ListOutput))
    for key, data in allData:
        attr, data = key.decode("utf-8"), data.decode("utf-8")
        print("{}(*{}) -> {}".format(method_key, attr, data))


class Cache:
    """
    store informations
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional
            [Callable] = None) -> Union[str, bytes, int, float]:
        data = self._redis.get(key)
        if (fn is not None):
            return fn(data)
        return data

    def get_str(self, data: str) -> str:
        return data.decode('utf-8')

    def get_int(self, data: str) -> int:
        return int(data)
