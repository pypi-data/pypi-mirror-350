import typing

import streamlit as st

from statql.common import IFEController, IntegrationIdentifier, ISecretsManager
from .definitions import RedisIntegrationDetails, RedisConnectorConfig


class RedisFEController(IFEController[RedisIntegrationDetails, RedisConnectorConfig]):
    title = "🟥 Redis"

    @classmethod
    def get_integration_form(cls) -> typing.Dict[str, typing.Any]:
        return {
            "host": st.text_input("Host"),
            "port": st.text_input("Port"),
            "username": st.text_input("Username"),
            "password": st.text_input("Password", type="password"),
        }

    @classmethod
    def build_integration_details(
        cls, *, integration_id: IntegrationIdentifier, integration_form_input: typing.Mapping[str, typing.Any], secrets_manager: ISecretsManager
    ) -> RedisIntegrationDetails:
        secret_name = secrets_manager.store_secret(
            secret_name_prefix=f"password-{integration_form_input['host']}",
            secret_value=integration_form_input["password"],
        )

        return RedisIntegrationDetails(
            host=integration_form_input["host"],
            port=int(integration_form_input["port"]),
            username=integration_form_input["username"],
            password_secret_name=secret_name,
        )

    @classmethod
    def verify_new_integration(cls, *, new_integration: RedisIntegrationDetails, existing_integrations: typing.Iterable[RedisIntegrationDetails]) -> str | None:
        if new_integration.host in {integration.host for integration in existing_integrations}:
            return "Host is already integrated"

    @classmethod
    def build_connector_config(cls, *, integration_details: RedisIntegrationDetails, secrets_manager: ISecretsManager) -> RedisConnectorConfig:
        return RedisConnectorConfig(
            host=integration_details.host,
            port=integration_details.port,
            username=integration_details.username,
            password=(
                secrets_manager.get_secret(secret_name=integration_details.password_secret_name)
                if integration_details.password_secret_name is not None
                else None
            ),
        )

    @classmethod
    def get_fe_details(cls, *, integration_details: RedisIntegrationDetails) -> typing.List[typing.Tuple[str, str]]:
        details = [
            ("Host", integration_details.host),
            ("Port", str(integration_details.port)),
        ]

        if integration_details.username is not None:
            details.append(("Username", integration_details.username))

        return details
