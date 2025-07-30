import logging
import time

import streamlit as st
from pydantic import ValidationError

from common import StatQLAppConfig, get_runtime_ctx, IntegrationInfo
from statql.common import Model, IntegrationIdentifier
from statql.framework import PluginsManager

logger = logging.getLogger(__name__)


class IntegrationsState(Model):
    integrated_catalog_name: str | None = None


def main():
    if "integrations_state" not in st.session_state:
        st.session_state.integrations_state = IntegrationsState()

    integrations_state = st.session_state.integrations_state

    config = get_runtime_ctx().get_config()

    # New integrations button
    if st.button("New Integration", icon="➕", key="new_integration"):
        new_integration_dialog(config=config, integrations_state=integrations_state)

    for integration in sorted(config.integrations, key=lambda integration_info: integration_info.id.catalog_name):
        fe_controller = PluginsManager.get_plugin_by_catalog_name(catalog_name=integration.id.catalog_name).fe_controller_cls
        details = fe_controller.get_fe_details(integration_details=integration.details)

        with st.expander(f"{fe_controller.title} - {integration.id.integration_name}"):
            for key, value in details:
                st.write(f"{key}: {value}")

            if st.button("Delete", icon="🗑️", key=f"{integration.id}_delete"):
                delete_integration_dialog(config=config, integration_id=integration.id)


@st.dialog("Add Integration")
def new_integration_dialog(*, config: StatQLAppConfig, integrations_state: IntegrationsState) -> None:
    # Catalog selection
    st.write("What platform would you like to integrate?")

    cols = st.columns(2)

    for i, plugin in enumerate(PluginsManager.get_all()):
        with cols[i % 2]:
            if st.button(plugin.fe_controller_cls.title, use_container_width=True):
                integrations_state.integrated_catalog_name = plugin.catalog_name

    # Integration form of selected catalog
    if integrations_state.integrated_catalog_name:
        plugin = PluginsManager.get_plugin_by_catalog_name(catalog_name=integrations_state.integrated_catalog_name)
        fe_controller = plugin.fe_controller_cls

        with st.form("Integration Form"):
            user_input = {"integration_name": st.text_input("Integration name (alias to use in queries)"), **fe_controller.get_integration_form()}

            if st.form_submit_button("Add", icon="➕"):
                integration_name = user_input["integration_name"]
                integration_id = IntegrationIdentifier(catalog_name=plugin.catalog_name, integration_name=integration_name)

                if config.get_integration_details(integration_id=integration_id) is not None:
                    st.error(f"Integration name already exists: '{integration_name}'")
                    return

                try:
                    integration_details = fe_controller.build_integration_details(
                        integration_name=integration_name,
                        integration_form_input=user_input,
                        secrets_manager=get_runtime_ctx().secrets_manager,
                    )
                except ValidationError as e:
                    st.error(f"Invalid integration details: {e}")
                    return

                if collision_error := fe_controller.verify_new_integration(
                    new_integration=integration_details,
                    existing_integrations=[
                        integration.details for integration in config.integrations if integration.id.catalog_name == integrations_state.integrated_catalog_name
                    ],
                ):
                    st.error(collision_error)
                    return

                config.integrations.append(IntegrationInfo(id=integration_id, details=integration_details))

                get_runtime_ctx().save_config(config=config)

                get_runtime_ctx().completions_manager.request(integration_identifiers=[integration_id])

                st.info("Successfully added integration!")

                time.sleep(1)
                st.rerun()


@st.dialog("Delete Integration")
def delete_integration_dialog(*, config: StatQLAppConfig, integration_id: IntegrationIdentifier) -> None:
    st.markdown(f"Are you sure you want to delete this integration?")

    if st.button("Yes"):
        config.remove_integration(integration_id=integration_id)
        get_runtime_ctx().save_config(config=config)

        st.info(f"Integration deleted")

        time.sleep(1)
        st.rerun()


if __name__ == "__main__":
    main()
