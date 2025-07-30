"""REQuest/REPly helpers"""

from typing import Callable, Any, Tuple, Optional, Sequence, List, Union, Dict
import inspect
import logging

from .datamessage import PubSubDataMessage
from .binpackers import uuid_to_b64
from .abstract import ZMQSocket, ZMQSocketUrisInputTypes, ZMQSocketDescription


LOGGER = logging.getLogger(__name__)
REQREP_DEFAULT_TIMEOUT = 5.0


class REQMixinBase:
    """Common REQuest helpers"""

    @classmethod
    def construct_command(cls, cmd: str, *args: Any, **kwargs: Any) -> PubSubDataMessage:
        """Helper to construct the command message"""
        msg = PubSubDataMessage(b"command")
        msg.data["command"] = [cmd] + list(args)
        msg.data["command_kwargs"] = kwargs
        return msg

    def _get_request_socket(self, sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes]) -> ZMQSocket:
        """Get the socket"""
        raise NotImplementedError("Must be implemented in the class to be mixed in")

    def _do_reqrep_blocking(
        self,
        sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes],
        msg: PubSubDataMessage,
        *,
        timeout: Optional[float] = None,
    ) -> PubSubDataMessage:
        """Do the actual REQuest and get the REPly (blocking context)"""
        raise NotImplementedError("Must be implemented in the class to be mixed in")

    async def _do_reqrep_async(
        self,
        sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes],
        msg: PubSubDataMessage,
        *,
        timeout: Optional[float] = None,
    ) -> PubSubDataMessage:
        """Do the actual REQuest and get the REPly (async context)"""
        raise NotImplementedError("Must be implemented in the class to be mixed in")

    def _sanity_check_reply(self, reply: PubSubDataMessage, expect_msgid_str: Optional[str]) -> bool:
        """Is the reply sane"""
        _ = self
        if "cmd_msgid" not in reply.data:
            LOGGER.error("reply does not specify cmd_msgid")
            LOGGER.debug("msg={}".format(reply))
            return False
        if expect_msgid_str and expect_msgid_str != reply.data["cmd_msgid"]:
            LOGGER.error("reply cmd_msgid mismatched ({} != {}".format(expect_msgid_str, reply.data["cmd_msgid"]))
            LOGGER.debug("msg={}".format(reply))
            return False
        if "exception" not in reply.data:
            LOGGER.error("reply does not specify exception")
            LOGGER.debug("msg={}".format(reply))
            return False
        if reply.data["exception"]:
            if "reason" not in reply.data:
                LOGGER.error("remote raised exception but did not provice reason")
            else:
                LOGGER.error("remote raised exception: {}".format(reply.data["reason"]))
            return False
        return True

    def send_command_blocking(
        self,
        sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes],
        cmd: str,
        *args: Any,
        **kwargs: Any,
    ) -> PubSubDataMessage:
        """Constructs and sends the command in blocking context to given socket, sanity-checks the reply.
        set_raise_on_insane=True to automatically raise an error if the reply is no good. set timeout=seconds
        for non-default timeout"""
        raise_on_insane = bool(kwargs.pop("raise_on_insane", False))
        timeout = float(kwargs.pop("timeout", REQREP_DEFAULT_TIMEOUT))
        cmd_msg = REQMixinBase.construct_command(cmd, *args, **kwargs)
        reply = self._do_reqrep_blocking(sockdef, cmd_msg, timeout=timeout)
        is_sane = self._sanity_check_reply(reply, uuid_to_b64(cmd_msg.messageid))
        if not is_sane and raise_on_insane:
            raise RuntimeError("Reply does not meet sanity-checks, see logs for details")
        return reply

    async def send_command_async(
        self,
        sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes],
        cmd: str,
        *args: Any,
        **kwargs: Any,
    ) -> PubSubDataMessage:
        """Constructs and sends the command in blocking context to given socket, sanity-checks the reply.
        set_raise_on_insane=True to automatically raise an error if the reply is no good. set timeout=seconds
        for non-default timeout"""
        raise_on_insane = kwargs.pop("raise_on_insane", False)
        timeout = kwargs.pop("timeout", REQREP_DEFAULT_TIMEOUT)
        cmd_msg = REQMixinBase.construct_command(cmd, *args, **kwargs)
        reply = await self._do_reqrep_async(sockdef, cmd_msg, timeout=timeout)
        is_sane = self._sanity_check_reply(reply, uuid_to_b64(cmd_msg.messageid))
        if not is_sane and raise_on_insane:
            raise RuntimeError("Reply does not meet sanity-checks, see logs for details")
        return reply


class REPMixinBase:
    """Common REPly helpers"""

    def resolve_command_method_and_args(
        self,
        msg: PubSubDataMessage,
        look_in: Optional[Sequence[Any]] = None,
        sdesc: Optional[ZMQSocketDescription] = None,
    ) -> Tuple[Callable[..., Any], Any, Dict[str, Any]]:
        """Resolve the method to use for message command, if optional look_in argument is given will look for the
        command method in the given classes in that order (defaults to [self])

        the optional sdesc argument is for implementors that want to do something based on the socket info
        """

        _ = sdesc
        LOGGER.debug("msg={}".format(msg))

        if "command" not in msg.data:
            raise RuntimeError("No command given")

        cmd_args = []
        if isinstance(msg.data["command"], str):
            cmd = msg.data["command"]
        else:
            cmd = msg.data["command"][0]
            cmd_args = msg.data["command"][1:]
        cmd_kwargs = msg.data.get("command_kwargs", {})

        if not look_in:
            look_in = [self]

        cmd_method: Optional[Callable[..., Any]] = None
        for instance in look_in:
            cmd_method = getattr(instance, cmd, None)
            if cmd_method:
                break
        if not cmd_method:
            raise RuntimeError("no such method {}".format(cmd))

        return cmd_method, cmd_args, cmd_kwargs

    async def handle_rep_async(
        self, msgparts: List[bytes], sdesc: Optional[ZMQSocketDescription] = None
    ) -> PubSubDataMessage:  # pylint: disable=R0912
        """Handle the incoming message and construct a reply, uses resolve_command_method_and_args to look
        for the method to actually handle the command

        the optional sdesc argument is for implementors that want to do something based on the socket info
        """
        reply = PubSubDataMessage(b"reply")
        try:
            msg = PubSubDataMessage.zmq_decode(msgparts)
            reply.data["cmd_msgid"] = uuid_to_b64(msg.messageid)

            cmd_method, cmd_args, cmd_kwargs = self.resolve_command_method_and_args(msg, None, sdesc)
            # Handle both coroutines and sync methods
            if inspect.iscoroutinefunction(cmd_method):
                response = await cmd_method(*cmd_args, **cmd_kwargs)
            else:
                response = cmd_method(*cmd_args, **cmd_kwargs)
            LOGGER.debug("{}({}, *, {}) returned {}".format(cmd_method, cmd_args, cmd_kwargs, response))
            reply.data.update(
                {
                    "failed": False,
                    "exception": False,
                    "reason": "",
                    "response": response,
                }
            )

        except Exception as exc:  # pylint: disable=W0703
            LOGGER.exception("Could not handle incoming message: {}".format(exc))
            reply.data.update({"failed": True, "exception": True, "reason": repr(exc)})
        return reply

    def handle_rep_blocking(
        self, msgparts: List[bytes], sdesc: Optional[ZMQSocketDescription] = None
    ) -> PubSubDataMessage:  # pylint: disable=R0912
        """blocking version of handle_rep_async, see that for details"""
        reply = PubSubDataMessage(b"reply")
        try:
            msg = PubSubDataMessage.zmq_decode(msgparts)
            reply.data["cmd_msgid"] = uuid_to_b64(msg.messageid)

            cmd_method, cmd_args, cmd_kwargs = self.resolve_command_method_and_args(msg, None, sdesc)
            if inspect.iscoroutinefunction(cmd_method):
                raise RuntimeError("{} is a coroutine and we are not capable of handling that".format(cmd_method))

            response = cmd_method(*cmd_args, **cmd_kwargs)
            LOGGER.debug("{}({}, *, {}) returned {}".format(cmd_method, cmd_args, cmd_kwargs, response))
            reply.data.update(
                {
                    "failed": False,
                    "exception": False,
                    "reason": "",
                    "response": response,
                }
            )

        except Exception as exc:  # pylint: disable=W0703
            LOGGER.exception("Could not handle incoming message: {}".format(exc))
            reply.data.update({"failed": True, "exception": True, "reason": repr(exc)})
        return reply
