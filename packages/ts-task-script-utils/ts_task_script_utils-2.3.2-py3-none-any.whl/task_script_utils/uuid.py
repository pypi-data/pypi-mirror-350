import os
from uuid import UUID as BaseUUID
from uuid import SafeUUID

# This implementation is taken from the proposed implementation for the python standard library:
# https://github.com/python/cpython/pull/121119/files#diff-890826c2d0ea55d3fae966dc9b1dae779bb25d4e1a9ef4acb42dc086c66ee290R755
# https://discuss.python.org/t/rfc-4122-9562-uuid-version-7-and-8-implementation/56725/12
_last_timestamp_v7 = None
_last_counter_v7 = 0  # 42-bit counter
_RFC_4122_VERSION_7_FLAGS = (7 << 76) | (0x8000 << 48)
_UINT_128_MAX = (1 << 128) - 1


class UUID(BaseUUID):  # Extend for backwards compatibility with older python versions
    @classmethod
    def _from_int(cls, value):
        """Create a UUID from an integer *value*. Internal use only."""
        assert 0 <= value <= _UINT_128_MAX, repr(value)
        self = object.__new__(cls)
        object.__setattr__(self, "int", value)
        object.__setattr__(self, "is_safe", SafeUUID.unknown)
        return self


def _uuid7():
    """Generate a UUID from a Unix timestamp in milliseconds and random bits.
    UUIDv7 objects feature monotonicity within a millisecond.
    """
    # --- 48 ---   -- 4 --   --- 12 ---   -- 2 --   --- 30 ---   - 32 -
    # unix_ts_ms | version | counter_hi | variant | counter_lo | random
    #
    # 'counter = counter_hi | counter_lo' is a 42-bit counter constructed
    # with Method 1 of RFC 9562, §6.2, and its MSB is set to 0.
    #
    # 'random' is a 32-bit random value regenerated for every new UUID.
    #
    # If multiple UUIDs are generated within the same millisecond, the LSB
    # of 'counter' is incremented by 1. When overflowing, the timestamp is
    # advanced and the counter is reset to a random 42-bit integer with MSB
    # set to 0.

    def get_counter_and_tail():
        # Default is byteorder="big" for >=3.11
        rand = int.from_bytes(os.urandom(10), byteorder="big")
        # 42-bit counter with MSB set to 0
        counter = (rand >> 32) & 0x1FF_FFFF_FFFF
        # 32-bit random data
        tail = rand & 0xFFFF_FFFF
        return counter, tail

    global _last_timestamp_v7
    global _last_counter_v7

    import time

    nanoseconds = time.time_ns()
    timestamp_ms = nanoseconds // 1_000_000

    if _last_timestamp_v7 is None or timestamp_ms > _last_timestamp_v7:
        counter, tail = get_counter_and_tail()
    else:
        if timestamp_ms < _last_timestamp_v7:
            timestamp_ms = _last_timestamp_v7 + 1
        # advance the 42-bit counter
        counter = _last_counter_v7 + 1
        if counter > 0x3FF_FFFF_FFFF:
            timestamp_ms += 1  # advance the 48-bit timestamp
            counter, tail = get_counter_and_tail()
        else:
            # Default is byteorder="big" for >=3.11
            tail = int.from_bytes(os.urandom(4), byteorder="big")

    _last_timestamp_v7 = timestamp_ms
    _last_counter_v7 = counter

    unix_ts_ms = timestamp_ms & 0xFFFF_FFFF_FFFF
    counter_msbs = counter >> 30
    counter_hi = counter_msbs & 0x0FFF  # keep 12 bits and clear variant bits
    counter_lo = counter & 0x3FFF_FFFF  # keep 30 bits and clear version bits

    int_uuid_7 = unix_ts_ms << 80
    int_uuid_7 |= counter_hi << 64
    int_uuid_7 |= counter_lo << 32
    int_uuid_7 |= tail & 0xFFFF_FFFF
    # by construction, the variant and version bits are already cleared
    int_uuid_7 |= _RFC_4122_VERSION_7_FLAGS
    return UUID._from_int(int_uuid_7)


def _uuid():
    """Abstraction layer for UUID generation

    This provides a fixed target for a fixture to patch, so that the UUID generation
    can be controlled in a test environment.
    """
    return _uuid7()


def uuid():
    """Generate a random UUID

    We are using UUID Version 7 for our random UUIDs.
    These are time-ordered, meaning that sequentially generated UUIDs are
    lexicographically sortable by creation time.

    For more details on UUID Version 7, see
    https://www.rfc-editor.org/rfc/rfc9562#name-uuid-version-7
    """
    return _uuid()
