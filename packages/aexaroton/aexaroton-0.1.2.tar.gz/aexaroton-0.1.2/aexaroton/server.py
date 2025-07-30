from __future__ import annotations
from typing import TYPE_CHECKING

from aexaroton import BASE_URL

from .types import ConfigFileData, FileInfoData, LogsData, LogsShareData, MotdData, RamData, ServerData, ExarotonResponse
from .websocket import WebSocket
from .errors import ExarotonError


if TYPE_CHECKING:
    from aiohttp import ClientSession


class Server:
    def __init__(self, data: ServerData, connection: "ClientSession"):
        self.data = data
        self._session = connection

    def __repr__(self) -> str:
        return f"<Server id={self.data.id}, name={self.data.name}>"

    async def create_socket(self) -> WebSocket:
        socket = WebSocket(self)
        await socket.connect()

        return socket

    async def get_logs(self) -> LogsData:
        async with self._session.get(BASE_URL / "servers" / self.data.id / "logs") as response:
            data: ExarotonResponse = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return LogsData(**data["data"])

    async def share_logs(self) -> LogsShareData:
        async with self._session.get(BASE_URL / "servers" / self.data.id / "logs" / "share") as response:
            data: ExarotonResponse = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return LogsShareData(**data["data"])

    async def get_ram(self) -> RamData:
        async with self._session.get(BASE_URL / "servers" / self.data.id / "options" / "ram") as response:
            data: ExarotonResponse = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return RamData(**data["data"])

    async def set_ram(self, ram: int) -> RamData:
        async with self._session.post(BASE_URL / "servers" / self.data.id / "options" / "ram", json={"ram": ram}) as response:
            data: ExarotonResponse = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return RamData(**data["data"])

    async def set_motd(self, motd: int) -> MotdData:
        async with self._session.post(BASE_URL / "servers" / self.data.id / "options" / "motd", json={"motd": motd}) as response:
            data: ExarotonResponse = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return MotdData(**data["data"])

    async def start(self, use_own_credits: bool | None = None) -> str:
        if self.data.shared is False and use_own_credits is not None:
            raise ValueError("user_own_credits is only for shared servers")
        elif self.data.shared is True and use_own_credits is None:
            raise ValueError("use_own_credits must be set for shared servers")

        if self.data.shared is False:
            async with self._session.get(BASE_URL / "servers" / self.data.id / "start") as response:
                data: dict = await response.json()

                if data["success"] != True:
                    raise ExarotonError(data["error"])

                assert data["data"] is not None
                return data["data"]

        else:
            async with self._session.post(BASE_URL / "servers" / self.data.id / "start", json={"useOwnCredits": use_own_credits}) as response:
                data: dict = await response.json()

                if data["success"] != True:
                    raise ExarotonError(data["error"])

                assert data["data"] is not None
                return data["data"]

    async def stop(self) -> str:
        async with self._session.get(BASE_URL / "servers" / self.data.id / "stop") as response:
            data: dict = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return data["data"]

    async def restart(self) -> str:
        async with self._session.get(BASE_URL / "servers" / self.data.id / "restart") as response:
            data: dict = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return data["data"]

    async def command(self, command: str) -> str:
        async with self._session.post(BASE_URL / "servers" / self.data.id / "command", json={"command": command}) as response:
            data: dict = await response.json()

            return data["data"]

    async def get_player_lists(self) -> list[str]:
        async with self._session.get(BASE_URL / "servers" / self.data.id / "playerlists") as response:
            data: dict = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return data["data"]

    # maybe there could be a PlayerList type?
    async def get_player_list(self, list_name: str) -> list[str]:
        async with self._session.get(BASE_URL / "servers" / self.data.id / "playerlists" / list_name) as response:
            data: dict = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return data["data"]

    async def add_to_player_list(self, list_name: str, entries: list[str]) -> list[str]:
        async with self._session.put(BASE_URL / "servers" / self.data.id / "playerlists" / list_name, json={"entries": entries}) as response:
            data: dict = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return data["data"]

    async def remove_from_player_list(self, list_name: str, entries: list[str]) -> list[str]:
        async with self._session.delete(BASE_URL / "servers" / self.data.id / "playerlists" / list_name, json={"entries": entries}) as response:
            data: dict = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return data["data"]

    async def get_file_info(self, file_path: str) -> FileInfoData:
        async with self._session.get(BASE_URL / "servers" / self.data.id / "files" / "info" / file_path) as response:
            data: dict = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return FileInfoData(**data["data"])

    async def get_file_data(self, file_path: str) -> bytes:
        async with self._session.get(BASE_URL / "servers" / self.data.id / "files" / "data" / file_path) as reponse:
            return await reponse.read()

    async def set_file_data(self, file_path: str, file_data: bytes) -> str:
        async with self._session.put(BASE_URL / "servers" / self.data.id / "files" / "data" / file_path, json=file_data) as response:
            data: dict = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return data["data"]

    async def delete_file(self, file_path: str) -> str:
        async with self._session.delete(BASE_URL / "servers" / self.data.id / "files" / "data" / file_path) as response:
            data: dict = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return data["data"]

    async def get_config_file(self, file_path: str) -> list[ConfigFileData]:
        async with self._session.get(BASE_URL / "servers" / self.data.id / "files" / "config" / file_path) as response:
            data: dict = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return [ConfigFileData(**config_data) for config_data in data["data"]]

    async def set_config_file(self, file_path: str, options: dict[str, str]) -> list[ConfigFileData]:
        async with self._session.post(BASE_URL / "servers" / self.data.id / "files" / "config" / file_path, json=options) as response:
            data: dict = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return [ConfigFileData(**config_data) for config_data in data["data"]]
