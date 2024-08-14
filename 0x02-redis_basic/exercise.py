#!/usr/bin/env python3
"""
Module defines the Cache class, decorators for counting method calls,
tracking call history, and a replay function to display the history of method
calls using Redis.
"""

import redis
import uuid
import functools
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be wrapped and counted.

    Returns:
        Callable: The wrapped method with added counting functionality.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = f"{method.__qualname__}:calls"
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method.

    Args:
        method (Callable): The method to be wrapped and tracked.

    Returns:
        Callable: The wrapped method with added history tracking functionality.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def replay(method: Callable):
    """
    Display the history of calls of a particular function.

    Args:
        method (Callable): The method whose history should be displayed.
    """
    redis_client = method.__self__._redis
    method_name = method.__qualname__

    input_key = f"{method_name}:inputs"
    output_key = f"{method_name}:outputs"

    inputs = redis_client.lrange(input_key, 0, -1)
    outputs = redis_client.lrange(output_key, 0, -1)

    print(f"{method_name} was called {len(inputs)} times:")

    for input_data, output_data in zip(inputs, outputs):
        input_str = input_data.decode("utf-8")
        output_str = output_data.decode("utf-8")
        print(f"{method_name}(*{input_str}) -> {output_str}")


class Cache:
    """
    The Cache class provides methods to interact with Redis for storing,
    retrieving, converting data, counting method calls, and tracking call
    history.
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) ->
    Union[str, bytes, int, float, None]:
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, lambda x: int(x))
