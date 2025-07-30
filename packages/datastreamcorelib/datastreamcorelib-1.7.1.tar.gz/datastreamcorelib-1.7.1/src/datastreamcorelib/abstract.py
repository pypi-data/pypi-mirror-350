"""Abstract baseclasses so that different eventloop implementations have common API for the user."""

import enum
from abc import ABC, abstractmethod  # pylint: disable=E0611  # false positive
from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Union, Type, Set

from .binpackers import normalize_uri_topic_list


SOCKETHANDLER_SINGLETONS: Dict[Type["BaseSocketHandler"], "BaseSocketHandler"] = {}


class DecodeError(RuntimeError):
    """Could not decode the message"""


class TooFewPartsError(DecodeError, ValueError):
    """Too few parts in the raw ZMQ message"""


class BaseMessage(ABC):
    """Baseclass for all ZMQ message types."""

    def __post_init__(self) -> None:
        """Here just for inheritance."""

    @abstractmethod
    def zmq_encode(self) -> List[bytes]:
        """Encode as ZMQ multipart."""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def zmq_decode(cls, raw_parts: List[bytes]) -> "BaseMessage":
        """Decodes from raw multipart message into instance."""
        raise NotImplementedError()


@dataclass
class RawMessage(BaseMessage):
    """The rawest form of ZMQ message."""

    raw_parts: List[bytes] = field(compare=False, default_factory=list)

    def zmq_encode(self) -> List[bytes]:
        """Encode for ZMQ transmission, pass this to socket.send_multipart."""
        return self.raw_parts

    @classmethod
    def zmq_decode(cls, raw_parts: List[bytes]) -> "RawMessage":
        """Decode raw message into class instance"""
        return cls(raw_parts)


ZMQSocketUrisInputTypes = Union[bytes, str, Sequence[str], Sequence[bytes]]


class ZMQSocketType(enum.IntEnum):
    """
    Map our intended socket type and direction

    The ioloop and ZMQ library specific implementations will then use these to
    create correct type of socket via the low-level APIs
    """

    PUB = 1
    SUB = 2
    REQ = 3
    REP = 4


@dataclass(frozen=True)
class ZMQSocketDescription:
    """
    Describe socket address(es) and type

    Note that the "type" is our internal logical type, not the actual ZMQ type
    the underlying ZMQ library uses
    """

    socketuris: ZMQSocketUrisInputTypes
    sockettype: ZMQSocketType = field(default=ZMQSocketType.SUB)

    def __post_init__(self) -> None:
        """Cast the socket uris into tuple of utf-8 bytes"""
        object.__setattr__(self, "socketuris", tuple(normalize_uri_topic_list(self.socketuris)))


class ZMQSocket(ABC):  # pylint: disable=R0903
    """Type mixin for ZMQ socket implementations in the ioloop (for type checking use)."""

    @abstractmethod
    def subscribe(self, topic: bytes) -> None:
        """Subscribe to a topic"""
        raise NotImplementedError()

    @property
    @abstractmethod
    def closed(self) -> bool:
        """Tells if the socket is open or closed"""
        raise NotImplementedError()

    @abstractmethod
    def close(self) -> None:
        """Close the socket"""
        raise NotImplementedError()

    @abstractmethod
    def __hash__(self) -> int:
        """Sockets are used as parts of dict keys, they must be "hashable" """
        raise NotImplementedError()


@dataclass
class BaseSocketHandler(ABC):
    """Baseclass for IOLoop specific socket handling stuff."""

    _sockets_by_desc: Dict[ZMQSocketDescription, ZMQSocket] = field(default_factory=dict, init=False, repr=False)

    def _get_cached_socket(self, desc: ZMQSocketDescription) -> Union[ZMQSocket, None]:
        """Get socket from cache if it exists"""
        return self._sockets_by_desc.get(desc, None)

    def _set_cached_socket(self, desc: ZMQSocketDescription, sock: ZMQSocket) -> None:
        """Put socket to cache, sanity-checking things"""
        if desc in self._sockets_by_desc:
            if self._sockets_by_desc[desc] == sock:
                return
            raise RuntimeError("Trying to put a new socket over existing description: {}".format(desc))
        self._sockets_by_desc[desc] = sock

    @classmethod
    def instance(cls) -> "BaseSocketHandler":
        """Get a singleton"""
        global SOCKETHANDLER_SINGLETONS  # pylint: disable=W0603,W0602
        if cls not in SOCKETHANDLER_SINGLETONS:
            SOCKETHANDLER_SINGLETONS[cls] = cls()
        return SOCKETHANDLER_SINGLETONS[cls]

    @abstractmethod
    def get_socket(self, desc: ZMQSocketDescription) -> ZMQSocket:
        """Get socket by address, or bind new one."""
        raise NotImplementedError()

    def close_all_sockets(self) -> None:
        """Close all sockets"""
        for sock in self.open_sockets:
            sock.close()

    @property
    def open_sockets(self) -> Set[ZMQSocket]:
        """Get a set of all open sockets we have"""
        return set((sock for sock in self._sockets_by_desc.values() if not sock.closed))
