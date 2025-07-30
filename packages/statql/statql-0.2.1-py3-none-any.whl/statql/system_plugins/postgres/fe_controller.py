import typing

import streamlit as st

from statql.common import IFEController, ISecretsManager
from .definitions import PostgresConnectorConfig, PostgresIntegrationDetails


class PostgresFEController(IFEController[PostgresIntegrationDetails, PostgresConnectorConfig]):
    title = "🐘 PostgresSQL"

    @classmethod
    def get_integration_form(cls) -> typing.Dict:
        return {
            "host": st.text_input("Host"),
            "port": st.text_input("Port"),
            "username": st.text_input("Username"),
            "password": st.text_input("Password", type="password"),
        }

    @classmethod
    def build_integration_details(
        cls, *, integration_name: str, integration_form_input: typing.Mapping[str, typing.Any], secrets_manager: ISecretsManager
    ) -> PostgresIntegrationDetails:
        secret_name = secrets_manager.store_secret(
            secret_name_prefix=f"pg-password-{integration_name}",
            secret_value=integration_form_input["password"],
        )

        return PostgresIntegrationDetails(
            host=integration_form_input["host"].lower(),
            port=integration_form_input["port"],
            user=integration_form_input["username"],
            password_secret_name=secret_name,
        )

    @classmethod
    def verify_new_integration(
        cls, *, new_integration: PostgresIntegrationDetails, existing_integrations: typing.Iterable[PostgresIntegrationDetails]
    ) -> str | None:
        if new_integration.host in {integration.host for integration in existing_integrations}:
            return "Host is already integrated"

    @classmethod
    def build_connector_config(cls, *, integration_details: PostgresIntegrationDetails, secrets_manager: ISecretsManager) -> PostgresConnectorConfig:
        return PostgresConnectorConfig(
            host=integration_details.host,
            port=integration_details.port,
            user=integration_details.user,
            password=secrets_manager.get_secret(secret_name=integration_details.password_secret_name),
        )

    @classmethod
    def get_fe_details(cls, *, integration_details: PostgresIntegrationDetails) -> typing.List[typing.Tuple[str, str]]:
        return [
            ("Host", integration_details.host),
            ("Port", str(integration_details.port)),
            ("Username", integration_details.user),
        ]
