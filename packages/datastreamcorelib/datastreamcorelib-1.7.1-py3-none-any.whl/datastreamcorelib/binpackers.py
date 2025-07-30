"""Un/packing helpers."""

from typing import Any, List, Sequence, Union

import msgpack  # type: ignore  # Get rid of error: Cannot find implementation or library stub for module
from libadvian.binpackers import uuid_to_b64, b64_to_uuid, ensure_str, ensure_utf8, ensure_utf8_list, ensure_str_list


def msgpack_pack(indata: Any) -> bytes:
    """MsgPack packing with explicitly defined settings."""
    return msgpack.packb(indata, use_bin_type=True)  # type: ignore   # The module lacks hints


def msgpack_unpack(indata: bytes) -> Any:
    """MsgPack unpacking with explicitly defined settings."""
    return msgpack.unpackb(indata, raw=False)


def normalize_uri_topic_list(inval: Union[bytes, str, Sequence[str], Sequence[bytes]]) -> List[bytes]:
    """Normalize input to list of utf8 encoded bytes, convert input of bytes/str into single element"""
    if isinstance(inval, (str, bytes)):
        return [ensure_utf8(inval)]
    return ensure_utf8_list(inval)


# We need to explicitly export all names since we imported some from libadvian
__all__ = [
    "uuid_to_b64",
    "b64_to_uuid",
    "ensure_str",
    "ensure_utf8",
    "ensure_utf8_list",
    "ensure_str_list",
    "msgpack_pack",
    "msgpack_unpack",
    "normalize_uri_topic_list",
]
