import os

from civis_key_manager.encrypted_services import EncryptedPersister


class EncryptedFilePersister(EncryptedPersister):
    """Save a key in an encrypted file.

    File location used:
    1. `filename` argument passed into constructor.
    2. `CIVIS_KEY_FILE` environmental variable.
    3. `key.cfy` file in the local directory.
    """

    def __init__(self, password=None, filename=None):
        if filename is None:
            env_filename = os.getenv('CIVIS_KEY_FILE')
            if env_filename is not None:
                self.filename = env_filename
            else:
                self.filename = "key.cky"
        else:
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
