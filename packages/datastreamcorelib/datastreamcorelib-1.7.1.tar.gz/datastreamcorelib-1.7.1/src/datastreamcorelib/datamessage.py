"""Data messages."""

from typing import Any, Dict, List, Union
import uuid
import datetime
from dataclasses import dataclass, field
from copy import deepcopy
import sys

from .abstract import BaseMessage, TooFewPartsError
from .binpackers import msgpack_pack, msgpack_unpack, ensure_utf8, uuid_to_b64
from .pubsub import PubSubMessage


def utctimestamp() -> str:
    """Get the UTC timestamp in the way given version wants it"""
    if sys.version_info < (3, 11):
        return datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
    # pylint: disable=E1101 # only a problem in pre 3.11 versions
    return datetime.datetime.now(datetime.UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


@dataclass
class BaseDataMessage(BaseMessage):  # pylint: disable=W0223
    """Baseclass for all ZMQ DataMessage types."""

    messageid: uuid.UUID = field(default_factory=uuid.uuid4)
    data: Dict[Any, Any] = field(compare=False, default_factory=dict)

    def __post_init__(self) -> None:
        """Auto-add systemtime"""
        if not self.data:
            self.data["systemtime"] = utctimestamp()


@dataclass
class PubSubDataMessage(BaseDataMessage, PubSubMessage):
    """
    Data messages handled via pub/sub.

    The raw wire format for multipart is as follows:

        - topic: UTF-8 encoded string
        - message-id: UUIDv4 as binary
        - message-data: msgpack binary

    Rest of the parts are stored in the dataparts array and subclasses might do something
    with them but you should not access the dataparts array from outside or very unexpected results
    will follow."""

    dataparts: List[bytes] = field(default_factory=list, repr=False)
    _skip_auto_unpack: bool = field(default=False, repr=False)

    def __post_init__(self) -> None:
        """Auto-decode dataparts from init."""
        super().__post_init__()
        if not self._skip_auto_unpack:
            if len(self.dataparts) > 0:
                self.messageid = uuid.UUID(bytes=self.dataparts[0])
            if len(self.dataparts) > 1:
                self.data = msgpack_unpack(self.dataparts[1])

    @classmethod
    def zmq_decode(cls, raw_parts: List[bytes]) -> "PubSubDataMessage":
        """Decode raw message into class instance."""
        if len(raw_parts) < 3:
            raise TooFewPartsError("Need at least 3 message parts to decode into PubSubDataMessage")
        return cls(
            topic=raw_parts[0],
            dataparts=raw_parts[1:],
            messageid=uuid.UUID(bytes=raw_parts[1]),
            data=msgpack_unpack(raw_parts[2]),
            _skip_auto_unpack=True,
        )

    def zmq_encode(self) -> List[bytes]:
        """Encode for ZMQ transmission, pass this to socket.send_multipart."""
        if len(self.dataparts) < 2:
            self.dataparts = [b"", b""]
        self.dataparts[0] = self.messageid.bytes
        self.dataparts[1] = msgpack_pack(self.data)
        return super().zmq_encode()

    def copy_as(self, topic: Union[bytes, str]) -> "PubSubDataMessage":
        """Create a deep copy with new messageid and topic, auto-sets 'from_msgid' for tracking"""
        newmsg = deepcopy(self)
        newmsg.messageid = uuid.uuid4()
        newmsg.data["from_msgid"] = uuid_to_b64(self.messageid)
        newmsg.topic = ensure_utf8(topic)
        newmsg.data["systemtime"] = utctimestamp()
        return newmsg
