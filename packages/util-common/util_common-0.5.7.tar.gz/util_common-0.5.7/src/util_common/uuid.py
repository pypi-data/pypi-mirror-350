"""
This module is deprecated.
Please use uuid_util.UUIDGenerator instead.
"""

import random
import uuid

import base58


def generate_short_uuid():
    # Generate a UUID1 (time-based UUID)
    raw_uuid = uuid.uuid1()

    # Convert the UUID to bytes
    uuid_bytes = raw_uuid.bytes

    # Encode the bytes to a base58 string
    base58_uuid = base58.b58encode(uuid_bytes)

    # Decode the base58 bytes to a string
    short_uuid = base58_uuid.decode('utf-8')

    return short_uuid


class UUID:
    """
    Warning: This class is deprecated.
    please use uuid_util.UUIDGenerator instead.
    """

    existed_uuid_set = set()
    retry_count = 0

    @staticmethod
    def get():
        return generate_short_uuid()

    @staticmethod
    def get_short(length=8, str_set=None):
        if not str_set:
            id = str(uuid.uuid4()).replace("-", "")[-length:]
        else:
            id = ''.join(random.choices(str_set, k=length))
        if id not in UUID.existed_uuid_set:
            UUID.existed_uuid_set.add(id)
            UUID.retry_count = 0
            return id
        else:
            UUID.retry_count += 1
            if UUID.retry_count > 5:
                raise Exception(
                    "Not enough uuids to use, try longer length or use get() instead of get_short()"
                )
            return UUID.get_short()
