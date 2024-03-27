#!/usr/bin/env python3
"""
module containing class Cache
"""
import redis
import uuid
from typing import Union


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
