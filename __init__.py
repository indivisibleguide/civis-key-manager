from civis_key_manager import CivisKeyManager
from file_persist import EncryptedFilePersister
from threading import Lock


def local_machine_key_manager(initial_key=None, days_replace=2):
    """Create a CivisKeyManager suitable for a development machine.

    Stores keys in an encrypted file on the hard drive. Uses thread safe,
    process unsafe locks for safety. This means that if multiple threads
    run at the same time, multiple keys could be requested.

    Looks for an encryption password in the 'CIVIS_ENCRYPT_PASSWORD'
    environmental variable. For more documentation on generating a password,
    see `EncryptedFilePersister.output_random_password()`.
    """
    return CivisKeyManager(
        EncryptedFilePersister(),
        Lock(),
        days_replace=days_replace,
        initial_key=initial_key
    )


def flask_server_key_manager(initial_key=None, days_replace=2):
    from server_services import UwsgiLock, RedisStore

    return CivisKeyManager(
        RedisStore(),
        UwsgiLock(),
        days_replace=days_replace,
        initial_key=initial_key
    )
