#!/usr/bin/env python3


"""main test"""

import time
import redis


get_page = __import__('web').get_page

url = 'http://google.com'
server = get_page(url)
server = get_page(url)
print(f"\n __________")
server = redis.Redis()
print(server.get(f'count:{url}'))
