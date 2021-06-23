""" This file contains locking and persistence tools that can be used
    on a Flask server to manage Civis API keys.
"""

import uwsgi
import os
import redis

REDIS_URL = os.getenv("REDIS_URL")


class UwsgiLock():
    def __init__(self, lock_level=0):
        self.lock_level = lock_level


    def acquire(self):
        uwsgi.lock(self.lock_level)


    def release(self):
        uwsgi.unlock(self.lock_level)


class RedisStore():
    def __init__(self):
        self.r = redis.from_url(REDIS_URL)
