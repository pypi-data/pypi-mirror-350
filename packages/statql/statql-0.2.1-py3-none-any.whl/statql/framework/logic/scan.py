import asyncio
import typing
from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
from queue import Queue, Empty

from statql.common import IAsyncConnector, IConnector, safe_wait, IntegrationIdentifier, TableIdentifier, StatQLMetaColumns
from ..common import (
    IPlanNode,
    StatQLContext,
    TableColumn,
    Term,
    PopulationPipelineBatch,
)

logger = getLogger(__name__)


class Scan(IPlanNode[PopulationPipelineBatch]):
    def __init__(
        self,
        *,
        integration_id_to_connector: typing.Mapping[IntegrationIdentifier, IConnector | IAsyncConnector],
        table_path: typing.Sequence[str],
        columns: typing.AbstractSet[TableColumn],
    ):
        super().__init__()

        if len(integration_id_to_connector) == 0:
            raise ValueError(f"Expected at least one connector")

        if all(isinstance(connector, IAsyncConnector) for connector in integration_id_to_connector.values()):
            self._async_mode = True
        elif all(isinstance(connector, IConnector) for connector in integration_id_to_connector.values()):
            self._async_mode = False
        else:
            raise ValueError(f"All connectors must be sync / async")

        self._integration_id_to_connector = integration_id_to_connector
        self._table_path = table_path
        self._columns = columns

    def get_output_terms(self) -> typing.Set[Term]:
        return set(self._columns)

    def execute(self, *, ctx: StatQLContext) -> typing.Generator[PopulationPipelineBatch, None, None]:
        if self._async_mode:
            scanner = AsyncScanner(
                integration_id_to_connector=self._integration_id_to_connector, event_loop=ctx.event_loop, table_path=self._table_path, columns=self._columns
            )
            yield from scanner.scan()

        else:
            scanner = SyncScanner(integration_id_to_connector=self._integration_id_to_connector, table_path=self._table_path, columns=self._columns)
            yield from scanner.scan()


class SyncScanner:
    def __init__(
        self,
        *,
        integration_id_to_connector: typing.Mapping[IntegrationIdentifier, IConnector],
        table_path: typing.Sequence[str],
        columns: typing.AbstractSet[TableColumn],
    ):
        self._integration_id_to_connector = integration_id_to_connector
        self._table_path = table_path
        self._columns = columns

        self._output_q = Queue()
        self._tables_being_scanned = set()
        self._executor = ThreadPoolExecutor(max_workers=10)
        self._is_terminated = False

    def scan(self) -> typing.Generator[PopulationPipelineBatch, None, None]:
        with self._executor:
            dispatch_futures = [
                self._executor.submit(self._dispatch_tables, integration_id=integration_id) for integration_id in self._integration_id_to_connector
            ]

            try:
                while True:
                    try:
                        yield self._output_q.get(timeout=1)
                    except Empty:
                        if all(dispatch_future.done() for dispatch_future in dispatch_futures) and not self._tables_being_scanned:
                            break
            finally:
                self._is_terminated = True
                self._executor.shutdown(wait=True, cancel_futures=True)

    def _dispatch_tables(self, *, integration_id: IntegrationIdentifier) -> None:
        try:
            connector = self._integration_id_to_connector[integration_id]

            for table_identifier in connector.resolve_table_path(table_path=self._table_path):
                generator = self._scan_table(integration_id=integration_id, table=table_identifier)
                self._tables_being_scanned.add(table_identifier)
                self._executor.submit(self._get_item_from_gen, scan_table_gen=generator)

        except Exception as e:
            logger.exception(f"Dispatch failed: {e}")

    def _get_item_from_gen(self, *, scan_table_gen: typing.Generator[PopulationPipelineBatch, None, None]) -> None:
        try:
            batch = next(scan_table_gen)

        except StopIteration:
            pass

        except Exception as e:
            logger.exception(f"Error while scanning table: {e}")

        else:
            self._output_q.put(batch)
            self._executor.submit(self._get_item_from_gen, scan_table_gen=scan_table_gen)

    def _scan_table(self, *, integration_id: IntegrationIdentifier, table: TableIdentifier) -> typing.Generator[PopulationPipelineBatch, None, None]:
        try:
            connector = self._integration_id_to_connector[integration_id]

            estimated_row_count = connector.estimate_row_count(table=table)
            column_rename_map = {col.column_name: str(hash(col)) for col in self._columns}

            # Making sure not to request StatQL meta columns from the connector
            connector_columns = column_rename_map.keys() - set(StatQLMetaColumns)

            for data in connector.scan_table(table=table, columns=connector_columns):
                if self._is_terminated:
                    break

                # Fill in missing columns (StatQL is not strict in that sense since when querying multiple tables, you don't know if they differ in schema)
                for term in self._columns:
                    if term.column_name not in data.columns:
                        data[term.column_name] = None

                if StatQLMetaColumns.INTEGRATION in column_rename_map:
                    data[StatQLMetaColumns.INTEGRATION] = integration_id.integration_name

                data.rename(columns=column_rename_map, inplace=True)

                yield PopulationPipelineBatch(
                    data=data,
                    integration_id=integration_id,
                    table_id=table,
                    table_size=estimated_row_count,
                    original_batch_size=len(data),
                )

        finally:
            logger.debug(f"Table scan generator has exited: {table}")
            self._tables_being_scanned.remove(table)


class AsyncScanner:
    def __init__(
        self,
        *,
        integration_id_to_connector: typing.Mapping[IntegrationIdentifier, IAsyncConnector],
        event_loop: AbstractEventLoop,
        table_path: typing.Sequence[str],
        columns: typing.AbstractSet[TableColumn],
    ):
        self._integration_id_to_connector = integration_id_to_connector
        self._event_loop = event_loop
        self._table_path = table_path
        self._columns = columns

        self._output_q = Queue()
        self._is_terminated = False

    def scan(self) -> typing.Generator[PopulationPipelineBatch, None, None]:
        scan_all_tables_futures = asyncio.run_coroutine_threadsafe(self._scan_all_tables(), loop=self._event_loop)

        try:
            while True:
                try:
                    yield self._output_q.get(timeout=1)
                except Empty:
                    if scan_all_tables_futures.done():
                        break

        finally:
            self._is_terminated = True
            _ = scan_all_tables_futures.result()

    async def _scan_all_tables(self) -> None:
        await safe_wait(
            [
                asyncio.create_task(self._scan_table(integration_id=integration_id, table=table))
                for integration_id, connector in self._integration_id_to_connector.items()
                async for table in connector.resolve_table_path(table_path=self._table_path)
            ],
            return_when=asyncio.ALL_COMPLETED,
        )

    async def _scan_table(
        self,
        *,
        integration_id: IntegrationIdentifier,
        table: typing.Hashable,
    ) -> None:
        connector = self._integration_id_to_connector[integration_id]
        estimated_row_count = await connector.estimate_row_count(table=table)
        column_rename_map = {col.column_name: str(hash(col)) for col in self._columns}

        # Making sure not to request StatQL meta columns from the connector
        connector_columns = column_rename_map.keys() - set(StatQLMetaColumns)

        async for data in connector.scan_table(table=table, columns=connector_columns):
            if self._is_terminated:
                break

            # Fill in missing columns (StatQL is not strict in that sense since when querying multiple tables, you don't know if they differ in schema)
            for term in self._columns:
                if term.column_name not in data.columns:
                    data[term.column_name] = None

            if StatQLMetaColumns.INTEGRATION in column_rename_map:
                data[StatQLMetaColumns.INTEGRATION] = integration_id.integration_name

            data.rename(columns=column_rename_map, inplace=True)

            self._output_q.put(
                PopulationPipelineBatch(
                    data=data,
                    integration_id=integration_id,
                    table_id=table,
                    table_size=estimated_row_count,
                    original_batch_size=len(data),
                )
            )
