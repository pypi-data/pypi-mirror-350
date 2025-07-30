from __future__ import annotations

import abc
import enum
import os
import typing
from pathlib import Path

from pandas import DataFrame

from .cache import ICache
from .secrets import ISecretsManager
from .utils import FrozenModel, Model

STATQL_DIR_PATH = Path.home() / ".statql"
os.makedirs(STATQL_DIR_PATH, exist_ok=True)

TableIdentifier = typing.Hashable


class StatQLInternalColumns(enum.StrEnum):
    ROW_ID = "__statql_row_id__"


class StatQLMetaColumns(enum.StrEnum):
    INTEGRATION = "@integration"


class TableInfo(FrozenModel):
    path: typing.Sequence[str]
    columns: typing.AbstractSet[str]


class IConnectorConfig(abc.ABC, FrozenModel):
    pass


class IIntegrationDetails(abc.ABC, FrozenModel):
    pass


class IConnector[ConnectorConfigT: IConnectorConfig, TableIdentifierT: TableIdentifier](abc.ABC):
    def __init__(self, *, cache: ICache, config: ConnectorConfigT):
        self._config = config
        self._cache = cache

    @abc.abstractmethod
    def resolve_table_path(self, *, table_path: typing.Sequence[str]) -> typing.Generator[TableIdentifierT, None, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def scan_table(self, *, table: TableIdentifierT, columns: typing.AbstractSet[str]) -> typing.Generator[DataFrame, None, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def estimate_row_count(self, *, table: TableIdentifierT) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch_all_tables(self) -> typing.Generator[TableInfo, None, None]:
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class IAsyncConnector[ConnectorConfigT: Model, TableIdentifierT: typing.Hashable](abc.ABC):
    def __init__(self, *, cache: ICache, config: ConnectorConfigT):
        self._config = config
        self._cache = cache

    @abc.abstractmethod
    async def resolve_table_path(self, *, table_path: typing.Sequence[str]) -> typing.AsyncGenerator[TableIdentifierT, None]:
        raise NotImplementedError

    @abc.abstractmethod
    async def scan_table(self, *, table: TableIdentifierT, columns: typing.AbstractSet[str]) -> typing.AsyncGenerator[DataFrame, None]:
        raise NotImplementedError

    @abc.abstractmethod
    async def estimate_row_count(self, *, table: TableIdentifierT) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def fetch_all_tables(self) -> typing.AsyncGenerator[TableInfo, None]:
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self) -> None:
        raise NotImplementedError


class IFEController[IntegrationDetailsT: IIntegrationDetails, ConnectorConfigT: IConnectorConfig](abc.ABC):
    title: typing.ClassVar[str]

    def __init_subclass__(cls, **kwargs):
        # Making sure everything is set
        _ = cls.title

        super().__init_subclass__(**kwargs)

    @classmethod
    @abc.abstractmethod
    def get_integration_form(cls) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError  # Use streamlit inputs to get user inputs. Return user inputs (eg {"name": "liel"})

    @classmethod
    @abc.abstractmethod
    def build_integration_details(
        cls, *, integration_name: str, integration_form_input: typing.Mapping[str, typing.Any], secrets_manager: ISecretsManager
    ) -> IntegrationDetailsT:
        # Builds integration config from user input. Should not return sensitive info. If you need to store passwords, use SecretsManager.
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def verify_new_integration(cls, *, new_integration: IntegrationDetailsT, existing_integrations: typing.Iterable[IntegrationDetailsT]) -> str | None:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def build_connector_config(cls, *, integration_details: IntegrationDetailsT, secrets_manager: ISecretsManager) -> ConnectorConfigT:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get_fe_details(cls, *, integration_details: IntegrationDetailsT) -> typing.List[typing.Tuple[str, str]]:
        raise NotImplementedError


class PluginBlueprint(FrozenModel):
    catalog_name: str
    fe_controller_cls: typing.Type[IFEController]
    connector_cls: typing.Type[IConnector | IAsyncConnector]
    integration_details_cls: typing.Type[IIntegrationDetails]


class IntegrationIdentifier(FrozenModel):
    catalog_name: str
    integration_name: str

    def __str__(self):
        return f"{self.catalog_name}.{self.integration_name}"
