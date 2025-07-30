"""Console scripts"""

from typing import Dict, List, Any, Union
import asyncio
import logging
import sys
import tempfile
import uuid
import random
import platform
import json
from pathlib import Path
from dataclasses import dataclass, field


import click
import toml
from libadvian.binpackers import ensure_str


from datastreamcorelib.logging import init_logging
from datastreamcorelib.binpackers import ensure_utf8
from datastreamcorelib.pubsub import PubSubMessage, Subscription
from datastreamcorelib.datamessage import PubSubDataMessage
from datastreamcorelib.imagemessage import PubSubImageMessage
from datastreamservicelib.service import SimpleService


LOGGER = logging.getLogger(__name__)


@dataclass
class Publisher(SimpleService):
    """Publisher service"""

    topic: bytes
    send_count: int = field(default=-1)
    images: bool = field(default=False)
    data: Dict[str, Any] = field(default_factory=dict)

    def reload(self) -> None:
        """Create task for sending messages"""
        super().reload()
        self.tm.create_task(self.message_sender(), name="sender")

    async def message_sender(self) -> None:
        """Send messages"""
        msgno = 0
        try:
            while self.psmgr.default_pub_socket and not self.psmgr.default_pub_socket.closed:
                msgno += 1
                msg: Union[None, PubSubImageMessage, PubSubDataMessage] = None
                if self.images:
                    msg = PubSubImageMessage(topic=self.topic)
                    msg.imginfo["format"] = "bgr8"
                    msg.imginfo["w"] = 1
                    msg.imginfo["h"] = 1
                    msg.imgdata = bytes((0, 0, 255))
                else:
                    msg = PubSubDataMessage(topic=self.topic)
                if not msg:
                    raise RuntimeError("We should not reach this ever")
                msg.data["msgno"] = msgno
                if self.data:
                    msg.data.update(self.data)
                LOGGER.debug("Publishing {}".format(msg))
                await self.psmgr.publish_async(msg)
                if self.send_count > 0 and msgno > self.send_count:
                    return self.quit()
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pass
        return None


@dataclass
class CollectingSubscriber(SimpleService):
    """Subscriber service that track received messages"""

    topic: bytes
    recv_count: int = field(default=-1)
    messages_by_sub: Dict[uuid.UUID, List[PubSubMessage]] = field(default_factory=dict)
    decoder_class: Any = field(default=PubSubDataMessage)

    def reload(self) -> None:
        """Create subscription"""
        super().reload()
        sub = Subscription(
            self.config["zmq"]["sub_socket"],
            self.topic,
            self.success_callback,
            decoder_class=self.decoder_class,
            isasync=True,
        )
        self.messages_by_sub[sub.trackingid] = []
        self.psmgr.subscribe_async(sub)

    async def success_callback(self, sub: Subscription, msg: PubSubMessage) -> None:
        """Append the message to the correct list"""
        if sub.trackingid not in self.messages_by_sub:
            self.messages_by_sub[sub.trackingid] = []
        self.messages_by_sub[sub.trackingid].append(msg)
        LOGGER.debug("Got msg {}".format(msg))
        if self.recv_count > 0 and len(self.messages_by_sub[sub.trackingid]) >= self.recv_count:
            self.quit()

    async def teardown(self) -> None:
        """Clean up the messages_by_sub"""
        self.messages_by_sub = {}
        return await super().teardown()


@click.command()
@click.option("-s", "--socket_uri", help="For example ipc:///tmp/publisher.sock", required=True)
@click.option("-t", "--topic", help="The topic to use for sending", required=True)
@click.option("-i", "--images", help="Send images (one red pixel)", is_flag=True)
@click.option("-c", "--count", help="Number of messages to send", type=int, default=-1)
@click.option("--data", help="Arbitary message.data content to publish", type=str)
def publisher_cli(socket_uri: str, topic: str, count: int, images: bool, data: str = "") -> None:
    """CLI entrypoint for publisher"""
    init_logging(logging.DEBUG)
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.debug("sys.argv={}".format(sys.argv))
    data_dec = {}
    if data:
        data_dec = json.loads(ensure_str(data))
    with tempfile.TemporaryDirectory() as tmpdir:
        configpath = Path(tmpdir) / "config.toml"
        LOGGER.debug("writing file {}".format(configpath))
        with open(configpath, "wt", encoding="utf-8") as fpntr:
            toml.dump({"zmq": {"pub_sockets": [socket_uri]}}, fpntr)
        pub_instance = Publisher(configpath, ensure_utf8(topic), count, images, data_dec)
        exitcode = asyncio.get_event_loop().run_until_complete(pub_instance.run())
    sys.exit(exitcode)


@click.command()
@click.option("-s", "--socket_uri", help="Must be same the publisher uses", required=True)
@click.option("-t", "--topic", help="The topic to use for receiving, must match topic used in publisher", required=True)
@click.option("-i", "--images", help="Use image decoder", is_flag=True)
@click.option("-c", "--count", help="Exit after this many messages received (-1 for inf)", type=int, default=-1)
def subscriber_cli(socket_uri: str, topic: str, count: int, images: bool) -> None:
    """CLI entrypoint for subscriber"""
    init_logging(logging.DEBUG)
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.debug("sys.argv={}".format(sys.argv))
    with tempfile.TemporaryDirectory() as tmpdir:
        serv_pub_sock_uri = "ipc://" + str(Path(tmpdir) / "testsubscriber_pub.sock")
        if platform.system() == "Windows":
            serv_pub_sock_uri = f"tcp://127.0.0.1:{random.randint(1337, 65000)}"  # nosec
        configpath = Path(tmpdir) / "config.toml"
        LOGGER.debug("writing file {}".format(configpath))
        with open(configpath, "wt", encoding="utf-8") as fpntr:
            toml.dump({"zmq": {"sub_socket": [socket_uri], "pub_sockets": [serv_pub_sock_uri]}}, fpntr)
        sub_instance = CollectingSubscriber(configpath, ensure_utf8(topic), count)
        if images:
            sub_instance.decoder_class = PubSubImageMessage
        exitcode = asyncio.get_event_loop().run_until_complete(sub_instance.run())
    sys.exit(exitcode)
