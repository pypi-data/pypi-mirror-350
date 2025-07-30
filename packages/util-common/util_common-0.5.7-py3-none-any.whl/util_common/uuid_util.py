import random
import uuid

import base58

from util_common.singleton import SingletonMixin


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
    Warning: This class is not thread-safe.
    please use uuid_util.UUIDGenerator instead.
    """

    def __init__(self):
        self.existed_uuid_set = set()
        self.retry_count = 0

    def _check_retry_count(self):
        if self.retry_count > 5:
            raise Exception(
                "Not enough uuids to use, try longer length or use get() instead of get_short()"
            )

    def _check_existed_uuid(self, id, gen_fn, *args, **kwargs):
        if id in self.existed_uuid_set:
            self.retry_count += 1
            self._check_retry_count()
            return gen_fn(*args, **kwargs)
        else:
            self.existed_uuid_set.add(id)
            self.retry_count = 0
            return id

    def get(self):
        id = generate_short_uuid()
        return self._check_existed_uuid(id, generate_short_uuid)

    def get_short(self, length=8, str_set=None):
        if not str_set:
            id = str(uuid.uuid4()).replace("-", "")[-length:]
        else:
            id = ''.join(random.choices(str_set, k=length))
        return self._check_existed_uuid(id, self.get_short, length, str_set)


class UUIDGenerator(SingletonMixin, UUID):
    pass
