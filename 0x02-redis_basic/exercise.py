import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps

def count_calls(f: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        f (Callable): The method to be decorated.

    Returns:
        Callable: A wrapper function that increments the call count.
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        """
        Increments the count for the method each time it is called.
        """
        key = f.__qualname__
        self._redis.incr(key)  # Increment the call count in Redis
        return f(self, *args, **kwargs)  # Call the original method
    return wrapper

class Cache:
    """
    A simple caching system using Redis to store and retrieve data.

    Attributes:
        _redis (redis.Redis): An instance of the Redis client.
    """

    def __init__(self) -> None:
        """
        Initializes the Cache instance and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis and returns a unique key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: A unique key associated with the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)  # Store the data in Redis
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieves data from Redis and applies an optional conversion function.

        Args:
            key (str): The key associated with the data.
            fn (Optional[Callable]): A function to convert the retrieved data.

        Returns:
            Optional[Union[str, bytes, int, float]]: The retrieved and converted data, or None if not found.
        """
        value = self._redis.get(key)  # Get the value from Redis
        if value is None:
            return None
        return fn(value) if fn else value  # Convert using the provided function

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves data as a UTF-8 string from Redis.

        Args:
            key (str): The key associated with the data.

        Returns:
            Optional[str]: The decoded string, or None if not found.
        """
        return self.get(key, fn=lambda x: x.decode('utf-8'))  # Decode bytes to str

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves data as an integer from Redis.

        Args:
            key (str): The key associated with the data.

        Returns:
            Optional[int]: The converted integer, or None if not found.
        """
        return self.get(key, fn=lambda x: int(x))  # Convert bytes to int

