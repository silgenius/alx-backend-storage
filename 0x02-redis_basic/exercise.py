#!/usr/bin/env python3

"""
This module provides a `Cache` class that utilizes Redis for caching data.
The class allows storing various types of data and retrieves them using a
unique key generated for each entry.
"""

import redis
import uuid
from typing import Union


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

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in the Redis database and
        returns a unique key associated with the stored data.
        """
        data_key = str(uuid.uuid4())
        self._redis.mset({data_key: data})
        return data_key
