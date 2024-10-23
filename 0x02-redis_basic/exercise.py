#!/usr/bin/env python3

"""
This module provides a `Cache` class that utilizes Redis for caching data.
The class allows storing various types of data and retrieves them using a
unique key generated for each entry.
"""

from functools import wraps
import redis
import uuid
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        increments the count for that key every time the method is called
        """
        if isinstance(self._redis, redis.Redis):
            key = method.__qualname__
            self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to keep track of history
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        append input arguemant and output result to a list
        """
        key = method.__qualname__
        self._redis.rpush(f'{key}:inputs', str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(f'{key}:outputs', result)
        return result
    return wrapper


class Cache:
    """
    The `Cache` class is responsible for managing a Redis connection
    and providing methods to store data in the Redis database.
    """

    def __init__(self):
        """
        Initializes a new instance of the `Cache` class.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in the Redis database and
        returns a unique key associated with the stored data.
        """
        data_key = str(uuid.uuid4())
        self._redis.mset({data_key: data})
        return data_key

    def get(self, key: str, fn=None):
        """
        Retrieves the value associated with the specified key from the
        Redis database. If the key does not exist, it returns `None`.
        If a callable function `fn` is provided, it will be applied
        to the retrieved data to convert it back to the desired format.
        """

        data = self._redis.get(key)
        if not data:
            return None

        if fn:
            return fn(data)
        return data

    def get_str(self, key):
        """
        Retrieves the value associated with the specified
        key as a UTF-8 string.
        """
        data = self._redis.get(key)
        if not data:
            return None
        return data.decode("utf-8")

    def get_int(self, key):
        """
        Retrieves the value associated with the specified key as an integer.
        """
        data = self._redis.get(key)
        if not data:
            return None
        return int(data)
