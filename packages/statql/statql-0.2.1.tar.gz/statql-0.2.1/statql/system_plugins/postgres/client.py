import typing
from logging import getLogger

from pandas import DataFrame
from psycopg import sql

from statql.common import timer
from .definitions import PostgresTableIdentifier, PostgresTableInfo
from .connections_manager import PostgresConnectionsManager

logger = getLogger(__name__)


class PostgresClient:
    @classmethod
    async def scan_table(
        cls,
        *,
        table_identifier: PostgresTableIdentifier,
        columns: typing.AbstractSet[str],
        chunk_size: int,
        connections: PostgresConnectionsManager,
    ) -> typing.AsyncGenerator[DataFrame, None]:
        logger.debug(f"Starting scan on table: {table_identifier.table_name}")

        columns_sql = sql.SQL(", ").join([sql.Identifier(col) for col in columns])
        table_sql = sql.SQL(".").join([sql.Identifier(table_identifier.schema_name), sql.Identifier(table_identifier.table_name)])
        query = sql.SQL("SELECT {columns} FROM {table} OFFSET %s LIMIT %s").format(columns=columns_sql, table=table_sql)

        connection = await connections.get_connection(db_name=table_identifier.db_name)

        async with connection.cursor() as cursor:
            offset = 0

            while True:
                await cursor.execute(query, (offset, chunk_size))
                rows = await cursor.fetchall()

                df = DataFrame(rows, columns=[desc[0] for desc in cursor.description])

                yield df

                if len(rows) < chunk_size:
                    break

                offset += len(rows)

    @classmethod
    async def random_scan_table(
        cls,
        *,
        table_identifier: PostgresTableIdentifier,
        columns: typing.AbstractSet[str],
        sample_ratio: float,
        sample_size: int,
        sample_count: int,
        connections: PostgresConnectionsManager,
    ) -> typing.AsyncGenerator[DataFrame, None]:
        logger.debug(f"Starting random scan on table: {table_identifier}")

        columns_sql = sql.SQL(", ").join([sql.Identifier(col) for col in columns])
        table_sql = sql.SQL(".").join([sql.Identifier(table_identifier.schema_name), sql.Identifier(table_identifier.table_name)])
        query = sql.SQL("SELECT {columns} FROM {table} TABLESAMPLE SYSTEM (%s) LIMIT %s").format(columns=columns_sql, table=table_sql)

        connection = await connections.get_connection(db_name=table_identifier.db_name)

        async with connection.cursor() as cursor:
            for i in range(sample_count):
                with timer(name=f"Fetch random chunk: {table_identifier}"):
                    await cursor.execute(query, (100 * sample_ratio, sample_size))
                    rows = await cursor.fetchall()

                    df = DataFrame(rows, columns=[desc[0] for desc in cursor.description])

                yield df

    @classmethod
    async def fetch_table_row_count_estimation(cls, *, table_identifier: PostgresTableIdentifier, connections: PostgresConnectionsManager) -> int:
        logger.debug(f"Fetching row count estimation for table: {table_identifier}")

        conn = await connections.get_connection(db_name=table_identifier.db_name)

        async with conn.cursor() as cursor:
            query = sql.SQL(
                """
                SELECT pg_class.reltuples 
                FROM pg_class 
                INNER JOIN pg_namespace ON pg_namespace.oid = pg_class.relnamespace
                WHERE pg_class.relname = %s AND pg_namespace.nspname = %s
                """
            )
            await cursor.execute(query, (table_identifier.table_name, table_identifier.schema_name))
            rows = await cursor.fetchmany()

            if len(rows) > 1:
                raise RuntimeError(f"Found {len(rows)} tables for table identifier: {table_identifier}")

            if len(rows) == 0:
                return 0

            return rows[0][0]

    @classmethod
    async def fetch_dbs_in_cluster(cls, *, connections: PostgresConnectionsManager) -> typing.List[str]:
        logger.debug(f"Fetching DBs in cluster")

        conn = await connections.get_connection(db_name="postgres")

        async with conn.cursor() as cursor:
            await cursor.execute(sql.SQL("SELECT datname FROM pg_database WHERE datistemplate = false"))
            return [_row[0] for _row in await cursor.fetchall()]

    @classmethod
    async def fetch_tables_in_db(cls, *, db_name: str, connections: PostgresConnectionsManager) -> typing.List[PostgresTableInfo]:
        logger.debug(f"Fetching tables in DB: {db_name}")

        # Returns list of (schema name, db name) tuples
        conn = await connections.get_connection(db_name=db_name)

        async with conn.cursor() as cursor:
            await cursor.execute(
                sql.SQL(
                    """
                    SELECT
                        table_schema,
                        table_name,
                        array_to_json(array_agg(column_name ORDER BY ordinal_position)) AS cols
                    FROM information_schema.columns
                    GROUP BY table_schema, table_name
                    """
                )
            )
            rows = await cursor.fetchall()

        return [
            PostgresTableInfo(
                table_identifier=PostgresTableIdentifier(
                    db_name=db_name,
                    schema_name=schema_name,
                    table_name=table_name,
                ),
                column_names=set(column_names),
            )
            for schema_name, table_name, column_names in rows
        ]
