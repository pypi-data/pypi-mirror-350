import typing

import streamlit as st

from statql.common import IFEController, ISecretsManager
from .definitions import FileSystemConnectorConfig, FileSystemIntegrationDetails


# TODO - handle non-case-sensitive file systems and case-sensitive file systems separately


class FileSystemFEController(IFEController[FileSystemIntegrationDetails, FileSystemConnectorConfig]):
    title = "📁 File System"

    @classmethod
    def get_integration_form(cls) -> typing.Dict[str, typing.Any]:
        return {"root_path": st.text_input("Root path")}

    @classmethod
    def build_integration_details(
        cls, *, integration_name: str, integration_form_input: typing.Mapping[str, typing.Any], secrets_manager: ISecretsManager
    ) -> FileSystemIntegrationDetails:
        return FileSystemIntegrationDetails(root_path=integration_form_input["root_path"])

    @classmethod
    def verify_new_integration(
        cls, *, new_integration: FileSystemIntegrationDetails, existing_integrations: typing.Iterable[FileSystemIntegrationDetails]
    ) -> str | None:
        if new_integration.root_path in {integration.root_path for integration in existing_integrations}:
            return "File system is already integrated"

    @classmethod
    def build_connector_config(cls, *, integration_details: FileSystemIntegrationDetails, secrets_manager: ISecretsManager) -> FileSystemConnectorConfig:
        return FileSystemConnectorConfig(root_path=integration_details.root_path)

    @classmethod
    def get_fe_details(cls, *, integration_details: FileSystemIntegrationDetails) -> typing.List[typing.Tuple[str, str]]:
        return [("Root path", integration_details.root_path)]
