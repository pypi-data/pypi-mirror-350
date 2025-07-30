import asyncio
import enum
import typing
from datetime import timedelta
from logging import getLogger

import numpy as np
from pandas import DataFrame

from statql.common import ICache, IAsyncConnector, StatQLInternalColumns, TableInfo
from .client import PostgresClient
from .definitions import PostgresTableIdentifier, PostgresConnectorConfig
from .connections_manager import PostgresConnectionsManager
from .introspector import Introspector, TableFilter

logger = getLogger(__name__)


class TableMetaColumnNames(enum.StrEnum):
    DB_NAME = "@db"
    SCHEMA_NAME = "@schema"
    TABLE_NAME = "@table"


class PostgresConnector(IAsyncConnector[PostgresConnectorConfig, PostgresTableIdentifier]):
    def __init__(self, *, cache: ICache, config: PostgresConnectorConfig):
        super().__init__(cache=cache, config=config)
        self._db_name_to_connection = {}
        self._connections = PostgresConnectionsManager(config=config)

    async def resolve_table_path(self, *, table_path: typing.Sequence[str]) -> typing.AsyncGenerator[PostgresTableIdentifier, None]:
        async for table_info in Introspector.introspect(
            connections=self._connections,
            cache=self._cache,
            table_filter=self._parse_table_path(table_path=table_path),
        ):
            yield table_info.table_identifier

    async def scan_table(self, *, table: PostgresTableIdentifier, columns: typing.AbstractSet[str]) -> typing.AsyncGenerator[DataFrame, None]:
        row_count = await self.estimate_row_count(table=table)

        if not self._config.sampling_config.is_worth_sampling(population_size=row_count, sample_size=self._config.scan_chunk_size):
            row_number = 0

            async for df in PostgresClient.scan_table(
                table_identifier=table,
                columns=columns - set(TableMetaColumnNames),
                connections=self._connections,
                chunk_size=self._config.scan_chunk_size,
            ):
                # Adding internal columns (required by infra)
                df[StatQLInternalColumns.ROW_ID] = np.arange(row_number, row_number + len(df))
                row_number += len(df)

                # Adding postgres meta columns
                if TableMetaColumnNames.DB_NAME in columns:
                    df[TableMetaColumnNames.DB_NAME] = table.db_name

                if TableMetaColumnNames.SCHEMA_NAME in columns:
                    df[TableMetaColumnNames.SCHEMA_NAME] = table.schema_name

                if TableMetaColumnNames.TABLE_NAME in columns:
                    df[TableMetaColumnNames.TABLE_NAME] = table.table_name

                yield df

        else:
            async for df in PostgresClient.random_scan_table(
                table_identifier=table,
                columns=columns - set(TableMetaColumnNames) | {"ctid"},
                sample_ratio=self._config.sampling_config.sample_ratio,
                sample_size=self._config.scan_chunk_size,
                sample_count=self._config.sampling_config.get_amount_of_samples(),
                connections=self._connections,
            ):
                # Adding internal columns (required by infra)
                df.rename(columns={"ctid": StatQLInternalColumns.ROW_ID}, inplace=True)

                # Adding postgres meta columns
                if TableMetaColumnNames.DB_NAME in columns:
                    df[TableMetaColumnNames.DB_NAME] = table.db_name

                if TableMetaColumnNames.SCHEMA_NAME in columns:
                    df[TableMetaColumnNames.SCHEMA_NAME] = table.schema_name

                if TableMetaColumnNames.TABLE_NAME in columns:
                    df[TableMetaColumnNames.TABLE_NAME] = table.table_name

                yield df

    async def estimate_row_count(self, *, table: PostgresTableIdentifier) -> int:
        try:
            return await asyncio.to_thread(self._cache.fetch, key=f"pg.table_row_count.{table}")
        except LookupError:
            row_count = await PostgresClient.fetch_table_row_count_estimation(table_identifier=table, connections=self._connections)
            await asyncio.to_thread(self._cache.store, key=f"pg.table_row_count.{table}", value=row_count, ttl=timedelta(hours=24))
            return row_count

    @classmethod
    def _parse_table_path(cls, *, table_path: typing.Sequence[str]) -> TableFilter:
        db, schema, table = table_path
        return TableFilter(
            db=None if db == "?" else db,
            schema=None if schema == "?" else schema,
            table=None if table == "?" else table,
        )

    async def fetch_all_tables(self) -> typing.AsyncGenerator[TableInfo, None]:
        async for table_info in Introspector.introspect(connections=self._connections, cache=self._cache):
            table_identifier = table_info.table_identifier

            yield TableInfo(
                path=(table_identifier.db_name, table_identifier.schema_name, table_identifier.table_name),
                columns=table_info.column_names | set(TableMetaColumnNames),
            )

    async def close(self) -> None:
        await self._connections.close()
