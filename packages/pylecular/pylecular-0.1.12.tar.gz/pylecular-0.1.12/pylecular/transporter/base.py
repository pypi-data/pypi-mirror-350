import importlib
from abc import ABC, abstractmethod
from typing import Optional

from pylecular.packet import Packet


class Transporter(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def publish(self, packet: Packet):
        pass

    @abstractmethod
    async def subscribe(self, command, topic: Optional[str] = None):
        pass

    @classmethod
    def get_by_name(
        cls: type["Transporter"], name: str, config: dict, transit, handler=None, node_id=None
    ) -> "Transporter":
        importlib.import_module("pylecular.transporter.nats")

        for subclass in cls.__subclasses__():
            if subclass.__name__.lower().startswith(name.lower()):
                return subclass.from_config(config, transit, handler, node_id)
        raise ValueError(f"No transporter found for: {name}")

    @classmethod
    @abstractmethod
    def from_config(
        cls: type["Transporter"], config: dict, transit, handler=None, node_id=None
    ) -> "Transporter":
        pass
