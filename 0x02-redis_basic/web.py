#!/usr/bin/env python3

"""
contains a get_page function that uses the requests
module to obtain the HTML content of a URL and returns it
"""

import requests
from functools import wraps
import redis


# setup redis server
server = redis.Redis()
server.flushdb()


def count_url(fn):
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
    req = requests.get(url)
    response = req.text
    return response
