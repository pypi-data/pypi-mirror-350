"""REQuest/REPly helpers"""

from typing import Union, Any, cast, Optional, Dict
import asyncio
import logging
import tempfile
from pathlib import Path
from dataclasses import dataclass, field

import zmq
from datastreamcorelib.abstract import ZMQSocketDescription, ZMQSocketType, ZMQSocketUrisInputTypes, ZMQSocket
from datastreamcorelib.datamessage import PubSubDataMessage
from datastreamcorelib.reqrep import REQMixinBase, REPMixinBase, REQREP_DEFAULT_TIMEOUT

from .zmqwrappers import Socket
from .service import SimpleServiceMixin, SimpleService


LOGGER = logging.getLogger(__name__)


@dataclass
class REQMixin(SimpleServiceMixin, REQMixinBase):
    """Mixin for making REQuests

    req_send_timeout is for the initial connection, use the timeout argument to send_command(_async) to control
    the timeout for waiting for reply.
    """

    req_send_timeout: float = field(default=1.0)
    _req_sock_locks: Dict[str, asyncio.Lock] = field(default_factory=dict)

    def _get_request_socket(self, sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes]) -> ZMQSocket:
        """Get the socket"""
        if isinstance(sockdef, ZMQSocket):
            return sockdef
        sdesc = ZMQSocketDescription(sockdef, ZMQSocketType.REQ)
        return self.psmgr.sockethandler.get_socket(sdesc)

    def _do_reqrep_blocking(
        self,
        sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes],
        msg: PubSubDataMessage,
        *,
        timeout: Optional[float] = None,
    ) -> PubSubDataMessage:
        raise TypeError("Not supported")

    async def _do_reqrep_async(
        self,
        sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes],
        msg: PubSubDataMessage,
        *,
        timeout: Optional[float] = None,
    ) -> PubSubDataMessage:
        """Do the actual REQuest and get the REPly (async context)"""
        if timeout is None:
            LOGGER.warning("Got None as timeout, this should not be happening")
            timeout = REQREP_DEFAULT_TIMEOUT
        sock = cast(Socket, self._get_request_socket(sockdef))
        if isinstance(sockdef, ZMQSocket):
            lock_key = str(hash(sock))
        else:
            lock_key = str(sockdef)
        if lock_key not in self._req_sock_locks:
            self._req_sock_locks[lock_key] = asyncio.Lock()
        async with self._req_sock_locks[lock_key]:
            try:
                await asyncio.wait_for(sock.send_multipart(msg.zmq_encode()), timeout=self.req_send_timeout)
                resp_parts = await asyncio.wait_for(sock.recv_multipart(), timeout=timeout)
                return PubSubDataMessage.zmq_decode(resp_parts)
            except (asyncio.TimeoutError, zmq.ZMQBaseError):
                sock.close()
                raise

    async def send_command(
        self,
        sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes],
        cmd: str,
        *args: Any,
        **kwargs: Any,
    ) -> PubSubDataMessage:
        """shorthand for send_command_async. sanity-checks the reply.
        set_raise_on_insane=True to automatically raise an error if the reply is no good. set timeout=seconds
        for non-default timeout"""
        return await self.send_command_async(sockdef, cmd, *args, **kwargs)


@dataclass
class REPMixin(SimpleServiceMixin, REPMixinBase):
    """Mixin for making REPlies

    rep_send_timeout is a timeout for sending the reply message, not for the time to handle the REQuest
    which is not currently wrapped in wait_for.
    """

    rep_send_timeout: float = field(default=1.0)

    def _resolve_default_rep_socket_uri(self) -> str:
        """Resolves the path for default PUB socket and sets it to PubSubManager"""
        pub_default = "ipc://" + str(Path(tempfile.gettempdir()) / self.configpath.name.replace(".toml", "_rep.sock"))
        if "zmq" in self.config and "rep_sockets" in self.config["zmq"]:
            pub_default = self.config["zmq"]["rep_sockets"]
        return pub_default

    async def _reply_task(self, sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes, None]) -> None:
        """Bind the given socket and start dealing with REQuests"""
        sdesc = None
        if isinstance(sockdef, ZMQSocket):
            sock = cast(Socket, sockdef)
        else:
            if sockdef is None:
                sockdef = self._resolve_default_rep_socket_uri()
            sdesc = ZMQSocketDescription(sockdef, ZMQSocketType.REP)
            sock = cast(Socket, self.psmgr.sockethandler.get_socket(sdesc))
        try:
            while not sock.closed:
                msgparts = await sock.recv_multipart()
                replymsg = await self.handle_rep_async(msgparts, sdesc)
                await asyncio.wait_for(sock.send_multipart(replymsg.zmq_encode()), timeout=self.rep_send_timeout)
            LOGGER.info("{} closed from under us".format(sock))
        except asyncio.CancelledError:
            LOGGER.debug("cancelled")
        finally:
            sock.close()

    def reload(self) -> None:
        """Load configs, restart sockets"""
        super().reload()
        # Create reply handler in the default uri
        if not self.tm.exists("DEFAULT_REP"):
            self.tm.create_task(self._reply_task(None), name="DEFAULT_REP")


@dataclass  # pylint: disable=R0901
class FullService(REPMixin, REQMixin, SimpleService):  # pylint: disable=R0901
    """Service with REQuest and REPly mixins applied"""
