from cryptography.fernet import Fernet
from abc import ABC, abstractmethod
import json
import os

from civis_api_key import CivisApiKey


class EncryptedPersister(ABC):
    """This class stores Civis API Keys in an encrypted text file.

    By default, uses an encryption password from the env variable 'CIVIS_ENCRYPT_PASSWORD'
    """

    @staticmethod
    def output_random_password():
        """Print a random encryption password to the console.

        To get a password, run this file and copy-paste the output into the 'CIVIS_ENCRYPT_PASSWORD'
        environmental variable.
        """
        print(Fernet.generate_key())

    def __init__(self, password=None):
        if password is None:
            self.password = os.getenv('CIVIS_ENCRYPT_PASSWORD')
        else:
            self.password = password

    @abstractmethod
    def _save_encrypted_key(self, keystr):
        pass

    def save_key(self, key):
        raw_json = json.dumps(key.__dict__)

        fernet = Fernet(self.password)
        encrypted_json = fernet.encrypt(raw_json.encode())

        self._save_encrypted_key(encrypted_json.decode())

    @abstractmethod
    def _load_encrypted_key(self):
        pass

    def load_key(self):
        encrypted_json = self._load_encrypted_key()

        if encrypted_json is None:
            return None

        fernet = Fernet(self.password)
        decrypted_json = fernet.decrypt(encrypted_json.encode()).decode()
        key_data = json.loads(decrypted_json)

        return CivisApiKey.from_civis(key_data)


class EncryptedFilePersister(EncryptedPersister):
    def __init__(self, password=None, filename="key.cky"):
        self.filename = filename
        super().__init__(password)

    def _save_encrypted_key(self, keystr):
        f = open(self.filename, "w")
        f.write(keystr)
        f.close()

    def _load_encrypted_key(self):
        if not os.path.exists(self.filename):
            return None

        f = open(self.filename, "r")
        encrypted_json = f.readline()
        f.close()

        return encrypted_json


if __name__ == '__main__':
    print(EncryptedPersister.output_random_password())
