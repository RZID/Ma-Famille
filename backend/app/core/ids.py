"""Client-safe identifiers.

Internal PKs stay plain autoincrement integers (fast joins, FKs).
Anything handed to the client uses UUIDv7 (time-ordered, RFC 9562):
sortable, index-friendly, unlike random v4 GUIDs.

Implemented on stdlib only so `requires-python >= 3.11` holds
(`uuid.uuid7` only exists on newer interpreters).
"""

import secrets
import time
from uuid import UUID

_UUID_V7_VERSION = 0x7
_RFC4122_VARIANT = 0x2


def uuid7() -> UUID:
    unix_ms = time.time_ns() // 1_000_000
    rand_a = secrets.randbits(12)
    rand_b = secrets.randbits(62)
    value = (
        ((unix_ms & 0xFFFFFFFFFFFF) << 80)
        | (_UUID_V7_VERSION << 76)
        | ((rand_a & 0xFFF) << 64)
        | (_RFC4122_VARIANT << 62)
        | (rand_b & 0x3FFFFFFFFFFFFFFF)
    )
    return UUID(int=value)
