"""PUB/SUB related helpers."""

from typing import Any, Coroutine, Callable, Dict, List, Sequence, Tuple, Type, Union, Optional, cast
from abc import ABC, abstractmethod  # pylint: disable=E0611  # false positive
from dataclasses import dataclass, field
import logging
import uuid


from .abstract import (
    BaseMessage,
    BaseSocketHandler,
    ZMQSocket,
    ZMQSocketDescription,
    ZMQSocketType,
    ZMQSocketUrisInputTypes,
    TooFewPartsError,
)
from .binpackers import ensure_utf8, normalize_uri_topic_list


SUBSCRIPTIONMANAGER_SINGLETONS: Dict[Type["BaseSocketHandler"], "BasePubSubManager"] = {}
LOGGER = logging.getLogger(__name__)


class NoDefaultSocketError(RuntimeError):
    """We have no default socket defined"""


@dataclass
class PubSubMessage(BaseMessage):
    """
    Generic PUB/SUB messages.

    The raw wire format for multipart is as follows:

        - topic: UTF-8 encoded string
        - dataparts: rest of the parts

    Make sure all your dataparts are actually bytes or ZMQ will throw a hissy fit
    """

    topic: Union[bytes, str]
    dataparts: List[bytes] = field(default_factory=list)

    def __setattr__(self, key: Any, value: Any) -> None:
        """Ensure topic is always bytes in the end."""
        if key == "topic":
            value = ensure_utf8(value)
        super().__setattr__(key, value)

    @classmethod
    def zmq_decode(cls, raw_parts: List[bytes]) -> "PubSubMessage":
        """Decode raw message into class instance."""
        if len(raw_parts) < 2:
            raise TooFewPartsError("Need at least 2 message parts to decode into PubSubMessage")
        return cls(raw_parts[0], raw_parts[1:])

    def zmq_encode(self) -> List[bytes]:
        """Encode for ZMQ transmission, pass this to socket.send_multipart."""
        return [ensure_utf8(self.topic)] + self.dataparts


# Aliases for readability
SubscriptionCBType = Callable[["Subscription", PubSubMessage], None]
SubscriptionAsyncCBType = Callable[["Subscription", PubSubMessage], Coroutine[Any, Any, None]]
DecoderFailCBType = Callable[["Subscription", List[bytes], Exception], None]
DecoderFailAsyncCBType = Callable[["Subscription", List[bytes], Exception], Coroutine[Any, Any, None]]
TopicsInputTypes = ZMQSocketUrisInputTypes


@dataclass(frozen=True)
class Subscription:  # pylint: disable=R0902
    """
    Wrapper for subscriptions, passed to the SubscriptionManagers subscribe method.

        - socketuris: either single socket address as bytes or string or a list of addresses
        - topics: either single topic as bytes or string or a list of topics
        - callback: the callback to call when message is received, it will get copy of this subscription and the
          decoded message (see `decoder_class` below)
        - decoder_class: A class to decode the raw ZMQ multipart message into something nicer, PubSubMessage by default
        - metadata: a dictionary you can use to pass arbitrary metadata to your callback, empty dict by default.
        - failure_callback: callback for decoder failure, get's copy of this subscription and the raw ZMQ message list
        - isasync: boolean, should we use the async or "normal" dispatch

    NOTE: We will automagically convert socket addresses and topics to UTF-8 since topics MUST anyway always
    be binary and PyZMQ bindings will convert socket address strings to bytes internally if str is supplied.
    See `ensure_utf8` and `ensure_utf8_list` on how to make values for comparison from strings you might want to use
    """

    socketuris: ZMQSocketUrisInputTypes
    topics: TopicsInputTypes
    callback: Union[SubscriptionCBType, SubscriptionAsyncCBType]
    decoder_class: Type[PubSubMessage] = field(default=PubSubMessage)
    metadata: Dict[Any, Any] = field(default_factory=dict)
    failure_callback: Union[DecoderFailCBType, DecoderFailAsyncCBType, None] = field(default=None)
    trackingid: uuid.UUID = field(default_factory=uuid.uuid4)
    isasync: bool = field(default=False)

    def __post_init__(self) -> None:
        """Ensure sockets and topics are lists in the end."""
        for key in ("socketuris", "topics"):
            value = tuple(normalize_uri_topic_list(getattr(self, key)))
            object.__setattr__(self, key, value)

    def zmq_decode_and_dispatch(self, msgparts: List[bytes]) -> None:
        """Decode and dispatch the message."""
        # TODO: how to catch decoding errors in less horrible manner
        if self.isasync:
            LOGGER.error("isasync is set to True and we have blocking dispatch, things probably break soon")
        try:
            message = self.decoder_class.zmq_decode(msgparts)
            if not self.callback:
                raise RuntimeError("callback is None, this definitely should not happen")
            self.callback(self, message)
        except Exception as exc:
            if self.failure_callback:
                self.failure_callback(self, msgparts, exc)
            # TODO: instead of re-raisin just log it ??
            raise exc

    async def zmq_decode_and_dispatch_async(self, msgparts: List[bytes]) -> None:
        """Decode and dispatch the message."""
        # TODO: how to catch decoding errors in less horrible manner
        if not self.isasync:
            LOGGER.error("isasync is set to False and we have async dispatch, things probably break soon")
        try:
            message = self.decoder_class.zmq_decode(msgparts)
            if not self.callback:
                raise RuntimeError("callback is None, this definitely should not happen")
            coro = self.callback(self, message)
            if coro:
                await coro
            else:
                LOGGER.error("callback did not return a coroutine, things probably seemed to work but this is WRONG")
        except Exception as exc:
            if self.failure_callback:
                coro = self.failure_callback(self, msgparts, exc)
                if coro:
                    await coro
                else:
                    LOGGER.error("failure_callback did not return a coroutine, this is WRONG")
            # TODO: instead of re-raisin just log it ??
            raise exc


# Alias for readability
SubscriptionMKType = Tuple[ZMQSocket, bytes]


@dataclass
class BasePubSubManager(ABC):
    """
    Manage subscriptions, the actual sockethandler implementation will take care of opening sockets
    as needed.
    """

    handlerklass: Type[BaseSocketHandler] = field(repr=False)
    subscriptions: List[Subscription] = field(default_factory=list, init=False)
    sockethandler: BaseSocketHandler = field(init=False)
    default_pub_socket: Optional[ZMQSocket] = field(init=False, default=None)
    _socket_topic_map: Dict[SubscriptionMKType, List[Subscription]] = field(
        default_factory=dict, init=False, repr=False
    )

    def __post_init__(self) -> None:
        """Instantiate the sockethandler"""
        self.sockethandler = self.handlerklass.instance()

    @classmethod
    def instance(cls, handlerklass: Type[BaseSocketHandler]) -> "BasePubSubManager":
        """Get a singleton"""
        global SUBSCRIPTIONMANAGER_SINGLETONS  # pylint: disable=W0603,W0602
        if handlerklass not in SUBSCRIPTIONMANAGER_SINGLETONS:
            SUBSCRIPTIONMANAGER_SINGLETONS[handlerklass] = cls(handlerklass)
        return SUBSCRIPTIONMANAGER_SINGLETONS[handlerklass]

    def subscribe(self, sub: Subscription) -> None:
        """Add the subscription to our handlers."""
        sdesc = ZMQSocketDescription(sub.socketuris, ZMQSocketType.SUB)
        sock = self.sockethandler.get_socket(sdesc)
        # Make sure mypy knows about __post_init__ of the subscription
        topics = cast(Sequence[bytes], sub.topics)
        for topic in topics:
            sock.subscribe(topic)
            mapkey = (sock, topic)
            if mapkey not in self._socket_topic_map:
                self._socket_topic_map[mapkey] = []
            self._socket_topic_map[mapkey].append(sub)
        self.subscriptions.append(sub)

    def publish(self, msg: PubSubMessage, sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes, None] = None) -> None:
        """Publish a message, optionally take a socket definition of where to publish"""
        if isinstance(sockdef, ZMQSocket):
            return self._publish_actual(msg, sockdef)

        if sockdef is None:
            if not self.default_pub_socket:
                raise NoDefaultSocketError()
            return self._publish_actual(msg, self.default_pub_socket)

        sdesc = ZMQSocketDescription(sockdef, ZMQSocketType.PUB)
        sock = self.sockethandler.get_socket(sdesc)
        return self._publish_actual(msg, sock)

    @abstractmethod
    def _publish_actual(self, msg: PubSubMessage, sock: ZMQSocket) -> None:
        """Implementation for actually handling the send"""
        raise NotImplementedError()

    def raw_zmq_callback(self, sock: ZMQSocket, msgparts: List[bytes]) -> None:
        """Find the corresponding subscriptions and dispatch."""
        topic = msgparts[0]

        match_found = False
        socket_topics = (mkey[1] for mkey in self._socket_topic_map if mkey[0] == sock)
        for stopic in socket_topics:
            if not topic.startswith(stopic):
                continue
            match_found = True
            mapkey = (sock, stopic)
            # TODO: check for empty subscription list and log error ??
            for subscription in self._socket_topic_map[mapkey]:
                subscription.zmq_decode_and_dispatch(msgparts)

        if not match_found:
            # TODO: Log error
            pass

    async def raw_zmq_callback_async(self, sock: ZMQSocket, msgparts: List[bytes]) -> None:
        """Find the corresponding subscriptions and dispatch."""
        topic = msgparts[0]

        match_found = False
        socket_topics = (mkey[1] for mkey in self._socket_topic_map if mkey[0] == sock)
        for stopic in socket_topics:
            if not topic.startswith(stopic):
                continue
            match_found = True
            mapkey = (sock, stopic)
            # TODO: check for empty subscription list and log error ??
            for subscription in self._socket_topic_map[mapkey]:
                if not subscription.isasync:
                    # support also non-async dispatch
                    subscription.zmq_decode_and_dispatch(msgparts)
                else:
                    await subscription.zmq_decode_and_dispatch_async(msgparts)

        if not match_found:
            # TODO: Log error
            return
