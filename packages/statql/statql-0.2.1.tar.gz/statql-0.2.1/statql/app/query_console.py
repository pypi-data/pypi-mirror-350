import time
from logging import getLogger
from threading import Thread

import streamlit as st
from code_editor import code_editor
from pandas import DataFrame
from pydantic import ConfigDict

from common import get_runtime_ctx
from statql.common import Model

logger = getLogger(__name__)


class QueryConsoleState(Model):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    is_stop_requested: bool = False
    executor: Thread | None = None
    output: DataFrame | None = None
    error: Exception | None = None

    @property
    def is_running(self) -> bool:
        return bool(self.executor and self.executor.is_alive())


def main():
    if "query_console" not in st.session_state:
        st.session_state.query_console = QueryConsoleState()

    qc_state = st.session_state.query_console

    # --- Query Input ---
    editor_dict = code_editor(
        "",
        lang="sql",
        theme="material",
        height=[5, 5],
        shortcuts="vscode",
        response_mode=["blur"],  # push edits on focus‑out so Run sees latest text
        key="sql_editor",
        focus=True,
        completions=get_runtime_ctx().completions_manager.get_all_completions(),
    )

    # --- Control Buttons ---
    col1, col2, _ = st.columns([1, 1, 5])

    with col1:
        if st.button("Go!", icon="🚀", disabled=qc_state.is_running):
            qc_state.output = None
            qc_state.is_stop_requested = False
            execute_sql(sql=editor_dict["text"], state=qc_state)
            st.rerun()

    with col2:
        if st.button("Stop!", icon="🛑", disabled=qc_state.is_stop_requested or not qc_state.is_running):
            qc_state.is_stop_requested = True
            st.rerun()

    # --- Results Output ---
    output_placeholder = st.empty()

    if qc_state.is_running:
        while qc_state.is_running:
            output_placeholder.dataframe(qc_state.output)
            time.sleep(0.5)

        st.rerun()

    else:
        if qc_state.output is not None:
            output_placeholder.dataframe(qc_state.output)

        if qc_state.error is not None:
            st.error(str(qc_state.error))


def execute_sql(sql: str, state: QueryConsoleState) -> None:
    ctx = get_runtime_ctx()

    def inner():
        try:
            with ctx.get_client() as client:
                for batch in client.query(sql=sql):
                    state.output = batch.data

                    if state.is_stop_requested:
                        break

                    time.sleep(0.5)

        except Exception as e:
            logger.exception(f"Error while executing SQL: {e}")
            state.error = e

    state.executor = Thread(target=inner, daemon=True)
    state.executor.start()


if __name__ == "__main__":
    main()
