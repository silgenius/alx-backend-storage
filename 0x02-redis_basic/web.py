#!/usr/bin/env python3

"""
This script contains a `get_page` function that uses the requests
module to obtain the HTML content of a URL and returns it.
It also includes a decorator to count how many times a URL is requested,
storing the count in a Redis database.
"""

import requests
from functools import wraps
import redis

# Setup Redis server
server = redis.Redis()
server.flushdb()

def count_url(method):
    """
    Decorator that counts the number of times a URL is requested.

    Args:
        method: The function to be wrapped.

    Returns:
        Wrapper function that increments the URL count in Redis.
    """
    @wraps(method)
    def wrapper(url):
        url = str(url)
        server.incr(f'count:{url}')
        result = server.get(f'result:{url}')
        if result:
            return result.decode("utf-8")
        server.setex(f'result:{url}', 10, method(url))
        return method(url)
    return wrapper


@count_url
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content of the page as a string.
    """
    return requests.get(url).text
