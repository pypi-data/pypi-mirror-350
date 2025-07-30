import os
import sys
import streamlit.web.cli as stcli


def main():
    sys.argv = [
        "streamlit",
        "run",
        os.path.join(os.path.dirname(__file__), "app", "app.py"),
        "--browser.gatherUsageStats", "false",
        "--global.developmentMode", "false",
        "--global.suppressDeprecationWarnings", "true",
        "--logger.level", "warning",
        "--client.showErrorDetails", "false",
        "--client.toolbarMode", "minimal",
        "--server.headless", "true",
        "--ui.hideTopBar", "true",
    ]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
