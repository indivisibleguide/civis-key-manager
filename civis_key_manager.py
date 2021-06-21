import civis
from datetime import datetime
import logging

from civis_api_key import CivisApiKey


class CivisKeyManager():
    def __init__(self, persist, lock_manager, days_replace=2, initial_key=None):
        self.persist = persist
        self.lock_manager = lock_manager
        self.days_replace = days_replace

        saved_key = persist.load_key()
        if saved_key is not None:
            self.__key = saved_key
        elif isinstance(initial_key, str):
            self.__key = CivisApiKey(token=initial_key)
        elif isinstance(initial_key, CivisApiKey):
            self.__key = initial_key


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


def main():
    #import code; code.interact(local=dict(globals(), **locals()))
    # client = civis.APIClient()
    # keys = client.users.list_api_keys('me')
    # key = CivisApiKey.from_civis(keys[0])

    # print(key.days_remaining())

    #persist = EncryptedFilePersister()
    #key = CivisApiKey(id=123, name="TestKey", token="boofarbar")

    #persist.save_key(key)

    key = persist.load_key()
    print(key.id)
    print(key.token)
    print(key.name)


if __name__ == '__main__':
    main()
