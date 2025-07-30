import asyncio

from typing import TYPE_CHECKING, Callable, Awaitable, assert_never, overload, Literal
from collections import defaultdict

import aiohttp

from aexaroton import BASE_URL
from aexaroton.socket_types import KeepAliveMessage, MessageType, ServerStatusMessage, SocketMessage, ReadyMessage, ConnectedMessage, DisconnectedMessage


if TYPE_CHECKING:
    from .server import Server


class ConsoleListener:
    def __init__(self, socket: "WebSocket") -> None:
        self.socket = socket

    async def send_command(self, command: str):
        await self.socket._send_console_command(command)

    async def process_line(self, line: str):
        raise NotImplementedError()


# TODO: add wait_for using futures
class WebSocket:
    def __init__(self, server: "Server"):
        self.server = server

        self.socket: aiohttp.ClientWebSocketResponse | None = None

        self._socket_task: asyncio.Task | None = None
        self._dispatch_tasks: list[asyncio.Task] = []

        self._event_listeners: defaultdict[MessageType, list[Callable[[SocketMessage], Awaitable[None]]]] = defaultdict(list)
        self._console_listener: ConsoleListener | None = None

        self._connecting_event = asyncio.Event()

    async def _is_connected(self) -> bool:
        return self.socket is not None

    async def connect(self):
        if self.socket is not None:
            raise ValueError("Called connect on an already connected websocket")
        
        if self._connecting_event.is_set():
            raise RuntimeError("Connecting event somehow set before connecting")

        self._socket_task = asyncio.create_task(self._socket_dispatch_task())
        await self._connecting_event.wait()

    async def close(self):
        if not await self._is_connected():
            raise ValueError("Cannot close an unopened socket")

        self.socket = None
        assert self._socket_task is not None
        self._socket_task.cancel()
        self._console_listener = None
        self._connecting_event.clear()

        await asyncio.gather(*self._dispatch_tasks)

    # TODO: how the heck do I type hint this
    async def register_listener(self, message_type: MessageType, callback: Callable[[SocketMessage], Awaitable[None]]):
        self._event_listeners[message_type].append(callback)

    async def register_console_listener(self, console_listener: type[ConsoleListener], *, tail_lines: int = 0):
        if not 0 <= tail_lines <= 500:
            raise ValueError(f"tail_lines must be between 0 and 500 (inclusive) not {tail_lines}")

        if self._console_listener is not None:
            raise ValueError("Must unregister previous console listener before registering a new one")

        if not await self._is_connected():
            raise ValueError("Socket must be open to register a console listener")

        await self._send(
            {
                "stream": "console",
                "type": "start",
                "data": {
                    "tail": tail_lines
                }
            }
        )

        self._console_listener = console_listener(self)

    async def unregister_console_listener(self):
        if not await self._is_connected():
            raise ValueError("Socket must be open to unregister a console listener")

        if self._console_listener is None:
            raise ValueError("There is no console listener to unregister")

        await self._send(
            {
                "stream": "console",
                "type": "stop"
            }
        )

        self._console_listener = None

    async def _send_console_command(self, command: str):
        if not await self._is_connected():
            raise ValueError("Socket must be open to send a console command")

        await self._send(
            {
                "stream": "console",
                "type": "command",
                "data": command
            }
        )

    async def _send(self, data: dict):
        if not await self._is_connected():
            raise RuntimeError("Somehow attempting to send in an unopened socket")

        assert self.socket is not None
        await self.socket.send_json(data)

    async def _socket_dispatch_task(self):
        async with self.server._session.ws_connect(BASE_URL / "servers" / self.server.data.id / "websocket") as ws:
            self.socket = ws
            self._connecting_event.set()

            async for message in ws:
                match message.type:
                    case aiohttp.WSMsgType.TEXT:
                        data: dict = message.json()
                        self._dispatch_tasks.append(asyncio.create_task(self._dispatch_event(data)))
                    case aiohttp.WSMsgType.ERROR | aiohttp.WSMsgType.closed:
                        break

    async def _dispatch_event(self, message: dict):
        if (stream_type := message.get("stream")) is not None:
            if stream_type == "status":
                pass
            else:
                # TODO: add other streams
                match stream_type:
                    case "console":
                        if self._console_listener is None:
                            raise RuntimeError("Somehow getting console stream without a console listener registered")

                        match message["type"]:
                            case "started":
                                pass
                            case "line":
                                await self._console_listener.process_line(message["data"])
                            case _:
                                raise RuntimeError(f"Unexpected message type in console stream {message['type']}")
                    case _:
                        raise NotImplementedError(f"Stream type {stream_type} not implemented")

                return

        message_type_name = message["type"].replace("-", "_")

        try:
            message_type = MessageType[message_type_name]
        except KeyError:
            raise RuntimeError(f"Unexpected message type {message_type_name}")

        match message_type:
            case MessageType.ready:
                event = ReadyMessage(**message)
            case MessageType.connected:
                event = ConnectedMessage(**message)
            case MessageType.disconnected:
                event = DisconnectedMessage(**message)
            case MessageType.keep_alive:
                event = KeepAliveMessage(**message)
            case MessageType.status:
                event = ServerStatusMessage(**message)
            case _:
                assert_never(message_type)

        await asyncio.gather(*[callback(event) for callback in self._event_listeners[message_type]])
