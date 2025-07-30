"""Implementations for the Abstract Base Classes from datastreamcorelib"""

from typing import cast, Any, Iterable, Dict, Callable, Awaitable, Union, Optional
from dataclasses import dataclass, field
import asyncio
import logging


import zmq
import zmq.asyncio
from datastreamcorelib.abstract import ZMQSocket, ZMQSocketType, BaseSocketHandler, ZMQSocketDescription
from datastreamcorelib.pubsub import (
    Subscription,
    BasePubSubManager,
    PubSubMessage,
    NoDefaultSocketError,
)
from datastreamcorelib.abstract import ZMQSocketUrisInputTypes

from .compat import asyncio_eventloop_check_policy

LOGGER = logging.getLogger(__name__)
asyncio_eventloop_check_policy()


@dataclass(frozen=True)
class Socket(ZMQSocket):
    """Wrapper for the raw AIO socket"""

    socket_type: ZMQSocketType
    _raw_socket: Any = field(default=None, init=False, repr=True)

    def __post_init__(self) -> None:
        """Create the RAW socket"""
        # Map our abstract types to the implementation type
        raw_socket_type: Optional[int] = None  # the ZMQ raw socket types are ints
        if self.socket_type == ZMQSocketType.PUB:
            raw_socket_type = zmq.PUB  # pylint: disable=E1101
        if self.socket_type == ZMQSocketType.SUB:
            raw_socket_type = zmq.SUB  # pylint: disable=E1101
        if self.socket_type == ZMQSocketType.REQ:
            raw_socket_type = zmq.REQ  # pylint: disable=E1101
        if self.socket_type == ZMQSocketType.REP:
            raw_socket_type = zmq.REP  # pylint: disable=E1101
        if raw_socket_type is None:
            raise ValueError("Invalid socket type {}".format(self.socket_type))
        object.__setattr__(self, "_raw_socket", zmq.asyncio.Context.instance().socket(raw_socket_type))

    def subscribe(self, topic: bytes) -> None:
        """Subscribe to a topic"""
        self._raw_socket.subscribe(topic)
        LOGGER.debug("{} subscribed to {!r}".format(self, topic))

    @property
    def closed(self) -> bool:
        """Tells if the socket is open or closed"""
        return bool(self._raw_socket.closed)

    def close(self) -> None:
        """Close the socket"""
        self._raw_socket.close()

    def __getattr__(self, key: str) -> Any:
        """Pass all but our abstractions to the raw socket"""
        return getattr(self._raw_socket, key)

    def __dir__(self) -> Iterable[str]:
        """Expose the raw socket dir too"""
        retval = set(self._raw_socket.__dir__())
        retval.add("__post_init__")
        retval.add("socket_type")
        retval.add("_raw_socket")
        return list(retval)

    def __hash__(self) -> int:
        """Make a hash based on the base sockets one"""
        return int(self._raw_socket.__hash__()) + self.socket_type.value


@dataclass
class SocketHandler(BaseSocketHandler):
    """Implement socket fetching"""

    def get_socket(self, desc: ZMQSocketDescription) -> ZMQSocket:
        """Get socket by address, or bind new one."""
        sock = self._get_cached_socket(desc)
        if sock:
            if not sock.closed:
                return sock
            # Clear the cache and create a new socket.
            del self._sockets_by_desc[desc]

        sock = Socket(desc.sockettype)
        # Bind/connect as needed
        if desc.sockettype not in (ZMQSocketType.SUB, ZMQSocketType.PUB, ZMQSocketType.REQ, ZMQSocketType.REP):
            raise RuntimeError("Don't know how to handle type {}".format(desc.sockettype))
        if desc.sockettype in (ZMQSocketType.SUB, ZMQSocketType.REQ):
            for addr in desc.socketuris:
                sock.connect(addr)
                LOGGER.debug("connected {} to {!r}".format(sock, addr))
        if desc.sockettype in (ZMQSocketType.PUB, ZMQSocketType.REP):
            for addr in desc.socketuris:
                sock.bind(addr)
                LOGGER.debug("bound {} to {!r}".format(sock, addr))

        self._set_cached_socket(desc, sock)
        return sock


@dataclass
class PubSubManager(BasePubSubManager):
    """
    Manage subscriptions, sockets and coroutines to read from the sockets
    """

    _socket_reader_tasks: Dict[Socket, "asyncio.Task[Callable[[Socket], Awaitable[None]]]"] = field(
        default_factory=dict, init=False
    )

    def __post_init__(self) -> None:
        """Instantiate the sockethandler"""
        # We do *not* want to use the singleton for sockethandler, it messes things up for running multiple
        # services in same asyncio loop
        self.sockethandler = self.handlerklass()

    def subscribe(self, sub: Subscription) -> None:
        """Add the subscription to our handlers and make sure socket reader is active"""
        super().subscribe(sub)
        sdesc = ZMQSocketDescription(sub.socketuris, ZMQSocketType.SUB)
        sock = cast(Socket, self.sockethandler.get_socket(sdesc))

        def reader_task_done(task: "asyncio.Task[Any]") -> None:
            """done callback for the reader task"""
            # raise exception if there was any
            task.result()

        if sock not in self._socket_reader_tasks or self._socket_reader_tasks[sock].done():
            # Add the reader task to the mainloop
            self._socket_reader_tasks[sock] = cast(
                "asyncio.Task[Callable[[Socket], Awaitable[None]]]",
                asyncio.get_event_loop().create_task(self._socket_reader(sock)),
            )
            self._socket_reader_tasks[sock].add_done_callback(reader_task_done)

    def subscribe_async(self, sub: Subscription) -> None:
        """Wrapper for subscribe that forces the subscription.isasync to be true"""
        if not sub.isasync:
            object.__setattr__(sub, "isasync", True)
        return self.subscribe(sub)

    async def _socket_reader(self, sock: Socket) -> None:
        """Waits and dispatches messages as long as the socket is open"""
        try:
            while not sock.closed:
                # LOGGER.debug("waiting message on {}".format(sock))
                msgparts = await sock.recv_multipart()
                # LOGGER.debug("got message on {}".format(sock))
                await self.raw_zmq_callback_async(sock, msgparts)
            LOGGER.debug("socket closed")
        except asyncio.CancelledError:
            # Handle cancellations gracefully
            LOGGER.debug("cancelled")

    async def publish_async(
        self, msg: PubSubMessage, sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes, None] = None
    ) -> None:
        """Publish a message, optionally take a socket definition of where to publish"""
        if isinstance(sockdef, ZMQSocket):
            ret = await cast(Socket, sockdef).send_multipart(msg.zmq_encode())
            return cast(None, ret)

        if sockdef is None:
            if not self.default_pub_socket:
                raise NoDefaultSocketError()
            ret = await cast(Socket, self.default_pub_socket).send_multipart(msg.zmq_encode())
            return cast(None, ret)

        sdesc = ZMQSocketDescription(sockdef, ZMQSocketType.PUB)
        sock = cast(Socket, self.sockethandler.get_socket(sdesc))
        ret = await sock.send_multipart(msg.zmq_encode())
        return cast(None, ret)

    def _publish_actual(self, msg: PubSubMessage, sock: ZMQSocket) -> None:
        """Implementation for actually handling the send, creates task to the eventloop"""
        # Fire-and-forget publish
        LOGGER.warning("You should use `await psmgr.publish_async` instead of just publish", stack_info=True)
        task = asyncio.get_event_loop().create_task(self.publish_async(msg, sock))

        def send_task_done(task: "asyncio.Task[Any]") -> None:
            """done callback for the send task"""
            # raise exception if there was any
            try:
                task.result()
            except asyncio.CancelledError:
                # Handle cancellations gracefully
                LOGGER.warning("task {} was cancelled for some reason, it should not have been".format(task))

        task.add_done_callback(send_task_done)


def pubsubmanager_factory() -> PubSubManager:
    """Get the default asyncio compatible PubSubManager with proper cast, requiring no arguments"""
    # We do *not* want to use the singleton for PubSubManager, it messes things up for running multiple
    # services in same asyncio loop
    return PubSubManager(SocketHandler)
