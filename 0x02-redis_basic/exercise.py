#!/usr/bin/env python3
"""
module containing class Cache
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        """ initializes data """
        self._redis = redis.Redis()
        self._redis.flushdb()

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
