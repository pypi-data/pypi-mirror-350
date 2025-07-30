import asyncio
import os
import sys
import typing
from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
from threading import Thread

from statql.common import (
    IConnector,
    IAsyncConnector,
    IntegrationIdentifier,
    async_gen_to_sync_gen,
    TableInfo,
    STATQL_DIR_PATH,
    ICache,
    JSONCache,
    IConnectorConfig,
)
from .plugins_manager import PluginsManager
from .query_executor import QueryExecutor
from .query_planner import Planner
from .quey_parser import QueryParser
from ..common import AggregationPipelineBatch, StatQLContext

logger = getLogger(__name__)


class StatQLClient:
    def __init__(
        self,
        *,
        connector_configurations: typing.Mapping[IntegrationIdentifier, IConnectorConfig],
        cache: ICache | None = None,
    ):
        self._connector_configurations = connector_configurations

        if cache is not None:
            self._cache = cache
        else:
            self._cache = JSONCache(dir_path=os.path.join(STATQL_DIR_PATH, "cache"))

        # Populated after __enter__
        self._ctx: StatQLContext | None = None
        self._event_loop: AbstractEventLoop | None = None
        self._event_loop_runner: Thread | None = None

    def __enter__(self):
        connectors = {}

        for integration_identifier, connector_config in self._connector_configurations.items():
            plugin = PluginsManager.get_plugin_by_catalog_name(catalog_name=integration_identifier.catalog_name)
            connectors[integration_identifier] = plugin.connector_cls(
                config=connector_config,
                cache=self._cache.get_segment(segment="integrations").get_segment(segment=str(integration_identifier)),
            )

        # Some catalogs are implemented in asyncio, so we build an event loop. In windows, we have to build WindowsSelectorEventLoopPolicy
        # because it is required by psycopg
        if sys.platform == "win32":
            from asyncio import WindowsSelectorEventLoopPolicy

            self._event_loop = WindowsSelectorEventLoopPolicy().new_event_loop()
        else:
            self._event_loop = asyncio.new_event_loop()

        self._event_loop.set_default_executor(ThreadPoolExecutor(max_workers=10))

        self._event_loop_runner = Thread(target=self._event_loop.run_forever, name="statql_event_loop")
        self._event_loop_runner.start()

        self._ctx = StatQLContext(event_loop=self._event_loop, connectors=connectors)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for connector in self._ctx.connectors.values():
            try:
                if isinstance(connector, IConnector):
                    connector.close()
                elif isinstance(connector, IAsyncConnector):
                    future = asyncio.run_coroutine_threadsafe(connector.close(), loop=self._event_loop)
                    future.result(timeout=5)
                else:
                    raise TypeError(f"Unexpected connector type: {type(connector).__name__}")

            except Exception as e:
                logger.exception(f"Failed to close connector: {e}")

        self._event_loop.call_soon_threadsafe(self._event_loop.stop)
        self._event_loop_runner.join()

    def query(self, *, sql: str) -> typing.Generator[AggregationPipelineBatch, None, None]:
        parsed_query = QueryParser.parse(sql=sql)
        execution_plan = Planner.plan(parsed_query=parsed_query, ctx=self._ctx)
        yield from QueryExecutor.execute(plan=execution_plan, ctx=self._ctx)

    def fetch_all_tables(self, *, integration_identifier: IntegrationIdentifier) -> typing.Generator[TableInfo, None, None]:
        connector = self._ctx.connectors[integration_identifier]

        if isinstance(connector, IConnector):
            gen = connector.fetch_all_tables()

        elif isinstance(connector, IAsyncConnector):
            gen = async_gen_to_sync_gen(async_gen=connector.fetch_all_tables(), loop=self._ctx.event_loop)

        else:
            raise TypeError(f"Unexpected connector type: {type(connector).__name__}")

        yield from gen
