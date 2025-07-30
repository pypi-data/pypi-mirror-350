import asyncio
import logging
import typing
from datetime import timedelta

from statql.common import FrozenModel, ICache, safe_wait
from .client import PostgresClient
from .definitions import PostgresTableInfo
from .connections_manager import PostgresConnectionsManager

logger = logging.getLogger(__name__)

BLACKLISTED_SCHEMAS = {"pg_catalog", "information_schema"}


class TableFilter(FrozenModel):
    db: str | None
    schema: str | None
    table: str | None

    def matches_db(self, *, db_name: str) -> bool:
        return self.db is None or self.db == db_name

    def matches_schema(self, *, schema_name: str) -> bool:
        return self.schema is None or self.schema == schema_name

    def matches_table(self, *, table_name: str) -> bool:
        return self.table is None or self.table == table_name


class Introspector:
    @classmethod
    async def introspect(
        cls,
        *,
        connections: PostgresConnectionsManager,
        cache: ICache,
        table_filter: TableFilter | None = None,
    ) -> typing.AsyncGenerator[PostgresTableInfo, None]:
        discovered_tables_q: asyncio.Queue[PostgresTableInfo] = asyncio.Queue()
        introspection_task = asyncio.create_task(
            cls._introspect_all(connections=connections, cache=cache, table_filter=table_filter, discovered_tables_q=discovered_tables_q)
        )

        try:
            while not (discovered_tables_q.empty() and introspection_task.done()):
                q_get_task = asyncio.create_task(discovered_tables_q.get())
                done, pending = await safe_wait([q_get_task, introspection_task], return_when=asyncio.FIRST_COMPLETED)

                if q_get_task in done:
                    yield q_get_task.result()

        finally:
            await introspection_task  # To raise errors

    @classmethod
    async def _introspect_all(
        cls,
        *,
        cache: ICache,
        connections: PostgresConnectionsManager,
        table_filter: TableFilter | None,
        discovered_tables_q: asyncio.Queue[PostgresTableInfo],
    ) -> None:
        try:
            db_names = await asyncio.to_thread(cache.fetch, key="db_names")
        except LookupError:
            db_names = await PostgresClient.fetch_dbs_in_cluster(connections=connections)
            await asyncio.to_thread(cache.store, key="db_names", value=db_names, ttl=timedelta(hours=24))

        await safe_wait(
            [
                asyncio.create_task(
                    cls._introspect_database(
                        db_name=db_name,
                        cache=cache,
                        connections=connections,
                        table_filter=table_filter,
                        discovered_tables_q=discovered_tables_q,
                    )
                )
                for db_name in db_names
                if table_filter is None or table_filter.matches_db(db_name=db_name)
            ],
            return_when=asyncio.ALL_COMPLETED,
        )

    @classmethod
    async def _introspect_database(
        cls,
        *,
        db_name: str,
        cache: ICache,
        connections: PostgresConnectionsManager,
        table_filter: TableFilter | None,
        discovered_tables_q: asyncio.Queue[PostgresTableInfo],
    ) -> None:
        try:
            cached_table_infos = await asyncio.to_thread(cache.fetch, key=f"dbs.{db_name}.tables")
            table_infos = [PostgresTableInfo(**cached_table_info) for cached_table_info in cached_table_infos]

        except LookupError:
            table_infos = await PostgresClient.fetch_tables_in_db(db_name=db_name, connections=connections)
            table_infos = [table_info for table_info in table_infos if table_info.table_identifier.schema_name not in BLACKLISTED_SCHEMAS]
            await asyncio.to_thread(
                cache.store,
                key=f"dbs.{db_name}.tables",
                value=[table_info.model_dump(mode="json") for table_info in table_infos],
                ttl=timedelta(hours=24),
            )

        for table_info in table_infos:
            if table_filter is None or (
                table_filter.matches_schema(schema_name=table_info.table_identifier.schema_name)
                and table_filter.matches_table(table_name=table_info.table_identifier.table_name)
            ):
                await discovered_tables_q.put(table_info)
