"""State management for the Dataflow object in Streamlit session."""

from typing import cast

import streamlit as st

from datarush.core.dataflow import Dataflow


def get_dataflow() -> Dataflow:
    """Get the dataflow object from the session state."""
    if "dataflow" not in st.session_state:
        set_dataflow(Dataflow())
    return cast(Dataflow, st.session_state["dataflow"])


def set_dataflow(dataflow: Dataflow) -> None:
    """Set the dataflow object in the session state."""
    st.session_state["dataflow"] = dataflow
