import os

from civis_key_manager.civis_key_manager import CivisKeyManager


def local_machine_key_manager(
    initial_key=None,
    days_replace=2,
    filename=None
):
    from civis_key_manager.file_services import EncryptedFilePersister
    from threading import Lock

    """Create a CivisKeyManager suitable for a development machine.

    Stores keys in an encrypted file on the hard drive. Uses thread safe,
    process unsafe locks for safety. This means that if multiple threads
    run at the same time, multiple keys could be requested.

    If not supplied, looks for an inital key in the `CIVIS_API_KEY`
    environmental variable.

    Stores the encrypted key in the location at the `CIVIS_KEY_FILE`
    environmental variable, or as `key.cfy` file in the local directory.
    For more documentation, see `file_services.EncryptedFilePersister`.

    Looks for an encryption password in the 'CIVIS_ENCRYPT_PASSWORD'
    environmental variable. For more documentation on generating a password,
    see `EncryptedFilePersister.output_random_password()`.
    """
    if initial_key is None:
        initial_key = os.getenv('CIVIS_API_KEY')

    return CivisKeyManager(
        EncryptedFilePersister(filename=filename),
        Lock(),
        days_replace=days_replace,
        initial_key=initial_key
    )


def flask_server_key_manager(initial_key=None, days_replace=2):
    from civis_key_manager.server_services import UwsgiLock, RedisStore

    return CivisKeyManager(
        RedisStore(),
        UwsgiLock(),
        days_replace=days_replace,
        initial_key=initial_key
    )
