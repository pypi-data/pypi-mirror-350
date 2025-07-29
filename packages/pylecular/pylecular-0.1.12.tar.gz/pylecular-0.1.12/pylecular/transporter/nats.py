import json
from typing import Any

import nats

from pylecular.packet import Packet

from .base import Transporter


class NatsTransporter(Transporter):
    name = "nats"

    def __init__(self, connection_string, transit, handler=None, node_id=None):
        super().__init__(self.name)
        self.connection_string = connection_string
        self.transit = transit
        self.handler = handler
        self.node_id = node_id
        self.nc: Any = None

    # TODO: maybe move it to base class
    # TODO: user real world serializer
    def _serialize(self, payload):
        payload["ver"] = "4"
        payload["sender"] = self.node_id
        return json.dumps(payload).encode("utf-8")

    def get_topic_name(self, command: str, node_id: str | None = None):
        topic = f"MOL.{command}"
        if node_id:
            topic += f".{node_id}"
        return topic

    async def message_handler(self, msg):
        data = json.loads(msg.data.decode("utf-8"))
        type = Packet.from_topic(msg.subject)
        sender = data.get("sender")
        packet = Packet(type, sender, data)
        if self.handler:
            await self.handler(packet)
        else:
            raise ValueError("Message received but no handler is defined")

    async def publish(self, packet: Packet):
        topic = self.get_topic_name(packet.type.value, packet.target)
        await self.nc.publish(topic, self._serialize(packet.payload))

    async def connect(self):
        self.nc = await nats.connect(self.connection_string)

    async def disconnect(self):
        if self.nc:
            await self.nc.close()
            self.nc = None

    async def subscribe(self, command, node_id=None):
        topic = self.get_topic_name(command, node_id)
        if self.handler is None:
            raise ValueError("Handler must be provided for subscription.")
        if (
            not callable(self.message_handler)
            or not callable(self.message_handler)
            or not hasattr(self.message_handler, "__code__")
            or not self.message_handler.__code__.co_flags & 0x80
        ):
            raise ValueError("Handler must be an async function.")
        await self.nc.subscribe(topic, cb=self.message_handler)

    @classmethod
    def from_config(
        cls: type["NatsTransporter"], config, transit, handler=None, node_id=None
    ) -> "Transporter":
        return cls(
            connection_string=config["connection"],
            transit=transit,
            handler=handler,
            node_id=node_id,
        )
