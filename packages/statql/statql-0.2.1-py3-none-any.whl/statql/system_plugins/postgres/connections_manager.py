import typing
from asyncio import Lock
from collections import defaultdict
from logging import getLogger

import psycopg

from .definitions import PostgresConnectorConfig

logger = getLogger(__name__)


class PostgresConnectionsManager:
    def __init__(self, *, config: PostgresConnectorConfig):
        self._config = config
        self._db_name_to_connection: typing.Dict[str, psycopg.AsyncConnection] = {}
        self._db_name_to_lock: typing.Dict[str, Lock] = defaultdict(Lock)

    async def get_connection(self, *, db_name: str) -> psycopg.AsyncConnection:
        try:
            return self._db_name_to_connection[db_name]
        except KeyError:
            async with self._db_name_to_lock[db_name]:
                if not (conn := self._db_name_to_connection.get(db_name)):  # Double check after lock acquired
                    logger.debug(f"Connecting to {self._config.host}/{db_name}")
                    conn = await psycopg.AsyncConnection.connect(
                        f"postgresql://{self._config.user}:{self._config.password}@{self._config.host}:{self._config.port}/{db_name}",
                        connect_timeout=5,
                    )
                    await conn.set_autocommit(True)
                    self._db_name_to_connection[db_name] = conn

                return conn

    async def close(self) -> None:
        for db_name, connection in self._db_name_to_connection.items():
            async with self._db_name_to_lock[db_name]:
                await connection.close()
