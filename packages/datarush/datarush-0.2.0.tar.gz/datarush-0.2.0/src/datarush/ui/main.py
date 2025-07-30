"""Main streamlit entrypoint."""

import streamlit as st

from datarush.config import AppConfig
from datarush.ui import operations, parameters, raw_template, sidebar


def main() -> None:
    """Run DataRush UI."""
    st.set_page_config(layout="wide")

    pages = [
        st.Page(parameters.parameters_page, title="Parameters"),
        st.Page(operations.operations_page, title="Operations"),
        st.Page(raw_template.raw_template_page, title="Raw"),
    ]

    main_page = st.navigation(pages, position="hidden")
    sidebar.sidebar_section(pages)
    main_page.run()


if __name__ == "__main__":
    AppConfig.validate()
    main()
