from enum import auto, Enum, IntEnum
from typing import TypedDict

from pydantic import BaseModel


class ExarotonResponse(TypedDict):
    success: bool
    error: str
    data: dict | None


class ServerStatus(IntEnum):
    offline = 0
    online = 1
    starting = 2
    stopping = 3
    restarting = 4
    saving = 5
    loading = 6
    crashed = 7
    pending = 8
    transferring = 9
    preparing = 10


class AccountData(BaseModel):
    name: str
    email: str
    verified: bool
    credits: float


class ServerPlayerData(BaseModel):
    max: int
    count: int
    list: list[str]


class ServerSoftwareData(BaseModel):
    id: str
    name: str
    version: str


class ServerData(BaseModel):
    id: str
    name: str
    address: str
    motd: str
    status: ServerStatus
    host: str | None
    port: int | None
    players: ServerPlayerData
    software: ServerSoftwareData | None
    shared: bool


class LogsData(BaseModel):
    content: str | None


class LogsShareData(BaseModel):
    id: str
    url: str
    raw: str


class RamData(BaseModel):
    ram: int


class MotdData(BaseModel):
    motd: str


class CommandData(BaseModel):
    command: str


class FileInfoData(BaseModel):
    path: str
    name: str
    isTextFile: bool
    isConfigFile: bool
    isDirectory: bool
    isLog: bool
    isReadable: bool
    isWritable: bool
    size: int
    children: list[str] | None


class ConfigFileType(Enum):
    string = auto()
    integer = auto()
    float = auto()
    boolean = auto()
    multiselect = auto()
    select = auto()


class ConfigFileData(BaseModel):
    key: str
    value: str
    label: str
    type: ConfigFileType
    options: list[str] | None = None


class CreditPoolData(BaseModel):
    id: str
    name: str
    credits: float
    servers: int
    owner: str
    isOwner: bool
    members: int
    ownShare: float
    ownCredits: float


class CreditPoolMemberData(BaseModel):
    account: str
    name: str
    share: int
    credits: float
    isOwner: bool


