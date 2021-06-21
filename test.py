import os
import logging

from __init__ import local_machine_key_manager

logging.getLogger().setLevel(logging.DEBUG)


def test():
    initial_key = os.getenv('CIVIS_API_KEY')
    client = local_machine_key_manager(initial_key=initial_key).client()

    data = client.users.list_me()

    print(data)


if __name__ == '__main__':
    test()
