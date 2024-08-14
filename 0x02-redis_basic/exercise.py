#!/usr/bin/env python3
"""
This module defines the Cache class for interacting with Redis to
store and retrieve data.
"""


import redis
import uuid
from typing import Union


class Cache:
    """
    The Cache class provides methods to interact with Redis for storing
    and retrieving data.
    """


    def __init__(self):
        """
        Initialize the Cache class.

        This method creates an instance of the Redis client and flushes the
        database to ensure a clean state.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]):data to be stored in Redis

        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
