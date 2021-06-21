from cryptography.fernet import Fernet
import json
import os

from civis_api_key import CivisApiKey


class EncryptedFilePersister():
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


    def save_key(self, key, filename="key.cky"):
        raw_json = json.dumps(key.__dict__)

        fernet = Fernet(self.password)
        encrypted_json = fernet.encrypt(raw_json.encode())

        f = open(filename, "w")
        f.write(encrypted_json.decode())
        f.close()


    def load_key(self, filename="key.cky"):
        f = open(filename, "r")
        encrypted_json = f.readline()
        f.close()

        fernet = Fernet(self.password)
        decrypted_json = fernet.decrypt(encrypted_json.encode()).decode()
        key_data = json.loads(decrypted_json)

        return CivisApiKey.from_civis(key_data)


if __name__ == '__main__':
    print(EncryptedFilePersister.output_random_password())
