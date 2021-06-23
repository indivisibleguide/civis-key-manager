""" This file contains locking and persistence tools that can be used
    on a Flask server to manage Civis API keys.
"""
import uwsgi
import os
import redis

from file_persist import EncryptedPersister

REDIS_URL = os.getenv("REDIS_URL")


class UwsgiLock():
    def __init__(self, lock_level=0):
        self.lock_level = lock_level


    def acquire(self):
        uwsgi.lock(self.lock_level)


    def release(self):
        uwsgi.unlock(self.lock_level)


class RedisStore(EncryptedPersister):
    def __init__(self):
        self.r = redis.from_url(REDIS_URL, decode_responses=True)
        super().__init__()


    def _save_encrypted_key(self, keystr):
        self.r.save('key', keystr)


    def _load_encrypted_key(self):
        return r.get('key')
