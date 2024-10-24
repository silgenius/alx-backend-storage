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


def count_url(fn):
    """
    Decorator that counts the number of times a URL is requested.

    Args:
        fn: The function to be wrapped.

    Returns:
        Wrapper function that increments the URL count in Redis.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        url = str(args[0])
        key = f'count:{url}'
        server.incr(key)
        server.expire(key, 10)
        return fn(*args, **kwargs)
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
    req = requests.get(url)  # Make a GET request to the URL
    response = req.text  # Get the response text (HTML)
    return response  # Return the HTML content
