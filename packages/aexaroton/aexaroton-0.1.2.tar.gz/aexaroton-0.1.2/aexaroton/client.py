from typing import Self

import aiohttp

from aexaroton import BASE_URL
from .types import AccountData, CreditPoolData, CreditPoolMemberData, ServerData, ExarotonResponse
from .server import Server
from .errors import ExarotonError


class Client:
    def __init__(self, token: str):
        self._closed: bool = False

        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

    async def __aenter__(self) -> Self:
        return self 

    async def __aexit__(self, *_) -> None:
        await self.close()
        return

    async def close(self):
        self._closed = True
        await self.session.close()

    async def get_account(self) -> AccountData:
        async with self.session.get(BASE_URL / "account") as response:
            data: dict = await response.json()

            return AccountData(**data["data"])

    async def get_servers(self) -> list[Server]:
        async with self.session.get(BASE_URL / "servers") as response:
            data: dict = await response.json()

            return [Server(ServerData(**server_data), self.session) for server_data in data["data"]]

    async def get_server(self, server_id: str) -> Server:
        async with self.session.get(BASE_URL / "servers" / server_id) as response:
            data: ExarotonResponse = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return Server(ServerData(**data["data"]), self.session)

    async def get_credit_pools(self) -> list[CreditPoolData]:
        async with self.session.get(BASE_URL / "billing" / "pools") as response:
            data: ExarotonResponse = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return [CreditPoolData(**pool_data) for pool_data in data["data"]]

    async def get_credit_pool(self, pool_id: str) -> CreditPoolData:
        async with self.session.get(BASE_URL / "billing" / "pools" / pool_id) as response:
            data: ExarotonResponse = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return CreditPoolData(**data["data"])

    async def get_credit_pool_members(self, pool_id: str) -> list[CreditPoolMemberData]:
        async with self.session.get(BASE_URL / "billing" / "pools" / pool_id / "members") as response:
            data: ExarotonResponse = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return [CreditPoolMemberData(**pool_member) for pool_member in data["data"]]

    async def get_credit_pool_servers(self, pool_id: str) -> list[Server]:
        async with self.session.get(BASE_URL / "billing" / "pools" / pool_id / "servers") as response:
            data: ExarotonResponse = await response.json()

            if data["success"] != True:
                raise ExarotonError(data["error"])

            assert data["data"] is not None
            return [Server(ServerData(**server_data), self.session) for server_data in data["data"]]


