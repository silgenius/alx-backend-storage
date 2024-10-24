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
from requests.exceptions import RequestException

# Setup Redis server
server = redis.Redis()

def count_url(method):
    """
    Decorator that counts the number of times a URL is requested.

    Args:
        method: The function to be wrapped.

    Returns:
        Wrapper function that increments the URL count in Redis.
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        url = str(args[0])
        key = f'count:{url}'

        # Increment the count and set expiration in Redis
        server.incr(key)
        server.expire(key, 10)

        # Call the original method
        return method(*args, **kwargs)

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
    key = f'cache:{url}'
    cached_response = server.get(key)

    if cached_response:
        return cached_response.decode('utf-8')

    try:
        req = requests.get(url)  # Make a GET request to the URL
        req.raise_for_status()  # Raise an error for bad responses
        response = req.text  # Get the response text (HTML)

        # Cache the response in Redis
        server.setex(key, 10, response)

        return response  # Return the HTML content
    except RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return ""


