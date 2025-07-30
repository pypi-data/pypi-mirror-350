from __future__ import annotations

import json
import logging
import typing
from concurrent.futures import ThreadPoolExecutor

import streamlit as st
from pydantic import ConfigDict, SerializeAsAny

from statql.common import IntegrationIdentifier, IIntegrationDetails, ISecretsManager, Model, FrozenModel
from statql.framework import StatQLClient, PluginsManager

logger = logging.getLogger(__name__)


class IntegrationInfo(FrozenModel):
    id: IntegrationIdentifier
    details: SerializeAsAny[IIntegrationDetails]


class StatQLAppConfig(Model):
    integrations: typing.List[IntegrationInfo]

    @classmethod
    def transform(cls, obj: typing.MutableMapping) -> None:
        parsed_integrations = []

        for integration_info in obj["integrations"]:
            if isinstance(integration_info, IntegrationInfo):
                parsed_integrations.append(integration_info)
            elif isinstance(integration_info, typing.Mapping):
                catalog_name = integration_info["id"]["catalog_name"]
                plugin = PluginsManager.get_plugin_by_catalog_name(catalog_name=catalog_name)
                parsed_integrations.append(
                    IntegrationInfo(
                        id=IntegrationIdentifier(**integration_info["id"]),
                        details=plugin.integration_details_cls(**integration_info["details"]),
                    )
                )
            else:
                raise TypeError

        obj["integrations"] = parsed_integrations

    def get_integration_details(self, *, integration_id: IntegrationIdentifier) -> IIntegrationDetails | None:
        for integration in self.integrations:
            if integration.id == integration_id:
                return integration.details

    def remove_integration(self, *, integration_id: IntegrationIdentifier) -> None:
        self.integrations = [integration for integration in self.integrations if integration.id != integration_id]


class RuntimeContext(Model):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    config_path: str
    completions_manager: CompletionsManager
    secrets_manager: ISecretsManager

    def get_config(self) -> StatQLAppConfig:
        logger.info(f"Loading config from {self.config_path}...")

        try:
            with open(self.config_path, "r") as f:
                return StatQLAppConfig(**json.load(f))
        except FileNotFoundError:
            return StatQLAppConfig(integrations=[])

    def save_config(self, *, config: StatQLAppConfig) -> None:
        logger.info(f"Saving config to {self.config_path}")

        with open(self.config_path, "w") as f:
            json.dump(config.model_dump(mode="json"), f, indent=3)

    def get_client(self) -> StatQLClient:
        config = self.get_config()

        integration_id_to_connector_config = {}

        for integration_info in config.integrations:
            plugin = PluginsManager.get_plugin_by_catalog_name(catalog_name=integration_info.id.catalog_name)
            connector_config = plugin.fe_controller_cls.build_connector_config(
                integration_details=integration_info.details, secrets_manager=self.secrets_manager
            )
            integration_id_to_connector_config[integration_info.id] = connector_config

        return StatQLClient(connector_configurations=integration_id_to_connector_config)


def get_runtime_ctx() -> RuntimeContext:
    return st.session_state.runtime_context


class CompletionsManager:
    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="completions_manager")
        self._completions = {}

    def request(self, integration_identifiers: typing.Iterable[IntegrationIdentifier]):
        for integration_identifier in integration_identifiers:
            self._executor.submit(self._populate_completions_for_integration, ctx=get_runtime_ctx(), integration_identifier=integration_identifier)

    def _populate_completions_for_integration(self, *, ctx: RuntimeContext, integration_identifier: IntegrationIdentifier) -> None:
        try:
            logger.info(f"Fetching completions...")

            with ctx.get_client() as client:
                for table_info in client.fetch_all_tables(integration_identifier=integration_identifier):
                    full_table_path = ".".join(table_info.path)
                    full_table_path = f"{integration_identifier.catalog_name}.{integration_identifier.integration_name}.{full_table_path}"

                    # Table completion
                    self._completions[full_table_path] = {
                        "caption": full_table_path,
                        "value": full_table_path,
                        "meta": "table",
                        "name": full_table_path,
                        "sframework": 1,
                    }

                    for column_name in table_info.columns:
                        self._completions[f"{full_table_path}:{column_name}"] = {
                            "caption": f"{table_info.path[-1]}.{column_name}",
                            "value": column_name,
                            "meta": "column",
                            "name": f"{full_table_path}:{column_name}",
                            "sframework": 1,
                        }

        except Exception as e:
            # TODO: sometimes this doesnt print?
            logger.exception(f"Failed to populate completions for integration {integration_identifier}: {e}")

    def get_all_completions(self) -> typing.List[typing.Dict]:
        return list(self._completions.values())
