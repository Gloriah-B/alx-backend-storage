#!/usr/bin/env python3
"""
Main file to test get_page function with caching and access counting.
"""
from web import get_page

url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"

# Fetch the page content, counting accesses and caching the result
content = get_page(url)
print(content)

# Check the access count
import redis
redis_client = redis.Redis()
print(redis_client.get(f"count:{url}"))  # Output: b'1'

# Fetch the page again to test caching
content = get_page(url)
print(redis_client.get(f"count:{url}"))  # Output: b'2'

