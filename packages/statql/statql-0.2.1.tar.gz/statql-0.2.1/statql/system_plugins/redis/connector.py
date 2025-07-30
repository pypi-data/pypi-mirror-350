import typing

from pandas import DataFrame
from redis.asyncio import Redis

from statql.common import ICache, IAsyncConnector, StatQLInternalColumns
from .definitions import RedisConnectorConfig, RedisKeysTableColumns


class RedisConnector(IAsyncConnector[RedisConnectorConfig, str]):
    def __init__(self, *, cache: ICache, config: RedisConnectorConfig):
        super().__init__(cache=cache, config=config)
        self._redis = Redis(host=config.host, port=config.port, username=config.username, password=config.password, decode_responses=True)

    async def resolve_table_path(self, *, table_path: typing.Sequence[str]) -> typing.AsyncGenerator[str, None]:
        if len(table_path) != 1:
            raise SyntaxError(f"Invalid table path")

        table_name = table_path[0]

        if table_name not in ("keys", "?"):
            raise SyntaxError(f"Unknown table name: {table_name}")

        yield "keys"

    async def scan_table(self, *, table: str, columns: typing.AbstractSet[str]) -> typing.AsyncGenerator[DataFrame, None]:
        if table != "keys":
            raise RuntimeError(f"Unsupported table: {table}")

        cursor = 0

        while True:
            cursor, keys = await self._redis.scan(cursor=cursor, match="*", count=self._config.scan_chunk_size)

            if keys:
                records = []

                for key in keys:
                    # TODO - add more columns
                    record = {StatQLInternalColumns.ROW_ID: key}

                    if RedisKeysTableColumns.KEY in columns:
                        record[RedisKeysTableColumns.KEY] = key

                    records.append(record)

                yield DataFrame(records)

            if cursor == 0:
                break

    async def estimate_row_count(self, *, table: str) -> int:
        if table != "keys":
            raise RuntimeError(f"Unsupported table: {table}")

        num_keys = await self._redis.dbsize()
        return num_keys

    async def fetch_all_tables(self) -> typing.AsyncGenerator[str, None]:
        yield "keys"

    async def close(self) -> None:
        await self._redis.close()
