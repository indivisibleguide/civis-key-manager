from datetime import datetime
import logging

from civis_key_manager.civis_api_key import CivisApiKey


class CivisKeyManager():
    def __init__(self, persist, lock_manager, days_replace=2, initial_key=None):
        self.persist = persist
        self.lock_manager = lock_manager
        self.days_replace = days_replace
        self.initial_key = initial_key
        self.__key = None

    def load_key(self):
        """Look for a persisted key. If none, use the supplied `initial_key`.

        Is called at the start of `key()`. Can be called on its own if
        you want to load the stored key.

        Does nothing if the key has already been loaded.
        """
        self.lock_manager.acquire()

        if self.__key is None:
            saved_key = self.persist.load_key()
            if saved_key is not None:
                logging.debug("Loaded key from saved key.")
                self.__key = saved_key
            elif isinstance(self.initial_key, str):
                logging.debug("Loaded key from initial key string.")
                self.__key = CivisApiKey(token=self.initial_key)
            elif isinstance(self.initial_key, CivisApiKey):
                logging.debug("Loaded key from initial key object.")
                self.__key = self.initial_key
            else:
                raise Exception("No valid Civis key found!")

        self.lock_manager.release()

    def update_key(self):
        logging.info("Requesting new key from civis.")

        client = self.__key.client()

        # Seconds * Minutes * Hours * Days = 30 Days in Seconds
        expires_time = 60 * 60 * 24 * 30
        current_timestamp = datetime.timestamp(datetime.now())
        name = f"automatedKeyAt{current_timestamp}"
        new_key = client.users.post_api_keys('me', expires_time, name)

        if new_key is not None:
            self.__key = CivisApiKey.from_civis(new_key)
            self.persist.save_key(self.__key)
            return self.__key
        else:
            # TODO: Handle key request failure better
            print("Bad key response")
            return None

    def key(self):
        self.load_key()

        self.lock_manager.acquire()

        key = None
        if self.__key.days_remaining() <= self.days_replace:
            logging.info("Current key soon to expire.")
            key = self.update_key()
        else:
            logging.debug(f"Current key valid for {self.__key.days_remaining()} days.")
            key = self.__key

        self.lock_manager.release()

        return key

    def client(self):
        """Get a Civis API Client with the current or updated key."""
        return self.key().client()
