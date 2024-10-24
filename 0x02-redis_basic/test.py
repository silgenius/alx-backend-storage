#!/usr/bin/env python3


"""main test"""

get_page = __import__('web').get_page

url = 'http://slowwly.robertomurray.co.uk'
server = get_page('http://slowwly.robertomurray.co.uk')
print(server)
