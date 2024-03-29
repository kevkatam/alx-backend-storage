#!/usr/bin/env python3
"""
module containing class Cache
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ decorator that returns a callable """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ increments key at every new instance of cache """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ decorator that stores the history of inputs and outputs """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ function that reurns value of the above method """
        key = method.__qualname__
        input_key = key + ":inputs"
        output_key = key + ":outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(func: Callable) -> None:
    """function to display the history of calls of a particular function"""
    history = func.__qualname__
    cache = redis.Redis()
    calls = cache.get(history).decode("utf-8")
    print(f"{history} was called {calls} times:")

    call_inputs = cache.lrange(history + ":inputs", 0, -1)
    call_outputs = cache.lrange(history + ":outputs", 0, -1)

    for input, output in zip(call_inputs, call_outputs):
        print(
            f"{history}(*{input.decode('utf-8')}) -> {output.decode('utf-8')}"
            )


class Cache:
    def __init__(self):
        """ initializes data """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ method that takes a data argument and returns a string """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        """ method that converts data to desiired standard """
        value = self._redis.get(key)
        if value is not None and fn is not None and callable(fn):
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """ method that parametrize Cache.get with the correct conversion
    function """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """ method that parametrize Cache.get with the correct conversion
            function """
        data = self
