# -*- coding: utf-8 -*-
import os
import redis
import json

class RedisCacheHandler:
    def __init__(self):
        self.host = os.getenv("REDIS_HOSTNAME")
        self.port = int(os.getenv("REDIS_PORT"))
        self.password = os.getenv("REDIS_PASSWORD")
        self.ttl = int(os.getenv("CACHE_TTL"))

        self.client = redis.StrictRedis(
            host=self.host,
            port=self.port,
            password=self.password,
            decode_responses=True
        )

    def set(self, key, value):
        """Set serialized value in Redis with a TTL."""
        serialized_value = json.dumps(value)
        self.client.setex(key, self.ttl, serialized_value)

    def get(self, key):
        """Get and deserialize value from Redis by key."""
        data = self.client.get(key)
        if data:
            return json.loads(data)
        return None

    def clear(self):
        """Clear all data in Redis."""
        self.client.flushdb()