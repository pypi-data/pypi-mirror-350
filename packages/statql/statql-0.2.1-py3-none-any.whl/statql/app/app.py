import logging
import os

import streamlit as st

from common import RuntimeContext, CompletionsManager
from statql.common import FileSecretsManager, STATQL_DIR_PATH


def main():
    logging.basicConfig(
        level=logging.DEBUG if int(os.environ.get("DEBUG", 0)) else logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if "runtime_context" not in st.session_state:
        runtime_context = RuntimeContext(
            config_path=os.path.join(STATQL_DIR_PATH, "app_config.json"),
            completions_manager=CompletionsManager(),
            secrets_manager=FileSecretsManager(secrets_file_path=os.path.join(STATQL_DIR_PATH, "secrets")),
        )
        st.session_state.runtime_context = runtime_context
        runtime_context.completions_manager.request(integration_identifiers=[integration.id for integration in runtime_context.get_config().integrations])

    st.set_page_config(page_title="StatQL", page_icon="📊", layout="wide")
    st.title("📊 StatQL")
    st.divider()

    pg = st.navigation([st.Page("query_console.py", title="📟 Query Console"), st.Page("integrations.py", title="🔌 Integrations")])
    pg.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
