import enum

from statql.common import IIntegrationDetails, IConnectorConfig


class RedisKeysTableColumns(enum.StrEnum):
    KEY = "key"


class RedisConnectorConfig(IConnectorConfig):
    host: str
    port: int
    username: str | None = None
    password: str | None = None
    scan_chunk_size: int = 10_000


class RedisIntegrationDetails(IIntegrationDetails):
    host: str
    port: int
    username: str | None = None
    password_secret_name: str | None = None
