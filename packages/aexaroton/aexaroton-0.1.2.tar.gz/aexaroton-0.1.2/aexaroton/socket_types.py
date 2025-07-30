from enum import IntEnum, auto, Enum

from pydantic import BaseModel

from aexaroton.types import ServerData


class MessageType(Enum):
    ready = "ready"
    connected = "connected"
    disconnected = "disconnected"
    keep_alive = "keep-alive"
    status = "status"


class ConsoleStreamType(IntEnum):
    start = auto()
    stop = auto()
    command = auto()
    started = auto()
    line = auto()


class TickStreamType(IntEnum):
    start = auto()
    stop = auto()
    started = auto()
    tick = auto()


class HeapStreamType(IntEnum):
    start = auto()
    stop = auto()
    started = auto()
    heap = auto()


class SocketMessage(BaseModel): ...


class ReadyMessage(SocketMessage):
    type: MessageType
    data: str


class ConnectedMessage(SocketMessage):
    type: MessageType


class DisconnectedMessage(SocketMessage):
    type: MessageType
    data: str


class KeepAliveMessage(SocketMessage):
    type: MessageType


class ServerStatusMessage(SocketMessage):
    type: MessageType
    stream: str
    data: ServerData
