import streamlit as st

from src.generator.exceptions import EventCountOutOfRangeError
from streamlit_app import NUMBER_OF_ORIGINS_METRIC_KEY
from streamlit_app import create_new_layout_if_hulk_is_created


def on_hulk_property_change_callback(table_name: str) -> None:
    widget_name = f"{table_name}_selection"

    try:
        new_event_infos = st.session_state[widget_name]
        st.session_state.space_hulk[table_name].events = [event_info.as_event() for event_info in new_event_infos]
    except EventCountOutOfRangeError as err:
        st.warning(f"{err} Your changes have been reverted.")
        st.session_state[widget_name] = st.session_state.space_hulk[table_name]

    if table_name == "rooms":
        create_new_layout_if_hulk_is_created()
    elif table_name == "origins":
        st.session_state[NUMBER_OF_ORIGINS_METRIC_KEY] = st.session_state.space_hulk.number_of_origins


def modify_space_hulk_properties() -> None:
    with st.expander("Show or modify space hulk properties", expanded=True):
        table_name: str = ""

        for table_name, _ in st.session_state.space_hulk:
            options = st.session_state.generator.get_table_events(table_name)
            defaults = []
            for selected_name in st.session_state.space_hulk.get_event_names(table_name):
                defaults.append(next(option for option in options if option.name == selected_name))
            st.multiselect(
                label=table_name.capitalize(),
                options=options,
                default=defaults,
                format_func=lambda x: x.name_with_description,
                on_change=on_hulk_property_change_callback,
                args=(table_name,),
                key=f"{table_name}_selection",
            )
