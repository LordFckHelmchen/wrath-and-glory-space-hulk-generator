import logging

import streamlit as st

from src.wrath_and_glory_space_hulk_generator.exceptions import EventCountOutOfRangeError
from src.wrath_and_glory_space_hulk_generator.space_hulk_generator import RoomCount
from src.wrath_and_glory_space_hulk_generator.space_hulk_generator import SpaceHulkGenerator
from src.wrath_and_glory_space_hulk_generator.space_hulk_layouter import LayoutEngine
from src.wrath_and_glory_space_hulk_generator.space_hulk_layouter import SpaceHulkLayouter

# st.set_page_config(layout="wide")

IS_DEBUG = True


def is_space_hulk_created() -> bool:
    return "space_hulk" in st.session_state


def create_new_hulk_and_layout():
    st.session_state.space_hulk = st.session_state.generator.create_hulk(
        number_of_rooms_per_origin=st.session_state.number_of_rooms_per_origin)
    create_new_layout_if_hulk_is_created()


def create_new_layout_if_hulk_is_created() -> None:
    if is_space_hulk_created():
        st.session_state.layout = SpaceHulkLayouter().create_layout(st.session_state.space_hulk,
                                                                    engine=st.session_state.layout_engine)
        update_metrics()


def recreate_hulk_and_layout_if_hulk_is_created() -> None:
    if is_space_hulk_created():
        create_new_hulk_and_layout()


def recreate_layout_with_new_engine_if_layout_is_created() -> None:
    if "layout" in st.session_state:
        st.session_state.layout.engine = st.session_state.layout_engine.value
        create_new_layout_if_hulk_is_created()


def get_layout_engine() -> LayoutEngine:
    return st.session_state.layout_engine if "layout_engine" in st.session_state else \
        LayoutEngine(SpaceHulkLayouter.DEFAULT_GRAPH_PROPERTIES["engine"])


def update_metrics() -> None:
    st.session_state["#Rooms in Hulk"] = st.session_state.space_hulk.number_of_rooms
    st.session_state["#Rooms in Layout"] = st.session_state.layout.number_of_nodes
    st.session_state["#Origins"] = st.session_state.space_hulk.number_of_origins
    st.session_state["#Connections"] = st.session_state.layout.number_of_edges


def on_hulk_property_change_callback(table_name: str) -> None:
    widget_name = f"{table_name}_selection"
    valid_event_counts = getattr(st.session_state.generator._tables, table_name).event_count_constraint
    st.write(f"{len(st.session_state[widget_name])} {valid_event_counts}")

    try:
        new_event_infos = st.session_state[widget_name]
        st.session_state.space_hulk[table_name].events = [event_info.as_event() for event_info in new_event_infos]
    except EventCountOutOfRangeError as err:
        st.warning(f"{err} Your changes have been reverted.")
        # TODO: Reassignment of values
        st.session_state[widget_name] = st.session_state.space_hulk[table_name]

    if table_name == "rooms":
        create_new_layout_if_hulk_is_created()
    elif table_name == "origins":
        st.session_state["#Origins"] = st.session_state.space_hulk.number_of_origins


st.title("Wrath & Glory Space Hulk Generator")

if "generator" not in st.session_state:
    st.session_state.generator = SpaceHulkGenerator()

st.header("Generator Settings")

st.number_input("Minimum number of rooms (per origin)",
                min_value=RoomCount.ge,
                max_value=RoomCount.le,
                value=10,
                key="number_of_rooms_per_origin",
                on_change=recreate_hulk_and_layout_if_hulk_is_created)

st.selectbox("Layout engine",
             options=list(LayoutEngine),
             format_func=lambda x: x.value,
             index=LayoutEngine.index(get_layout_engine()),
             key="layout_engine",
             on_change=recreate_layout_with_new_engine_if_layout_is_created)

if st.button("Create new hulk?"):
    create_new_hulk_and_layout()

if is_space_hulk_created():
    st.header("Space Hulk")

    # TODO: Add name & description field

    metric_cols = st.columns(4)
    metric_cols[0].metric("#Origins", value=st.session_state.space_hulk.number_of_origins)
    metric_cols[1].metric("#Rooms", value=st.session_state.space_hulk.number_of_rooms)
    metric_cols[2].metric("#Rooms in Layout", value=st.session_state.layout.number_of_nodes)
    metric_cols[3].metric("#Connections", value=st.session_state.layout.number_of_edges)

    if st.button("Create new layout?"):
        create_new_layout_if_hulk_is_created()

    with st.expander("Show or modify space hulk properties", expanded=True):
        table_name: str = ""

        for table_name, _ in st.session_state.space_hulk:

            options = st.session_state.generator.get_table_events(table_name)
            defaults = []
            for selected_name in st.session_state.space_hulk.get_event_names(table_name):
                defaults.append(next(option for option in options if option.name == selected_name))
            # TODO: Consider linking occupations & purposes
            st.multiselect(label=table_name.capitalize(),
                           options=options,
                           default=defaults,
                           format_func=lambda x: x.name_with_description,
                           on_change=on_hulk_property_change_callback,
                           args=(table_name,),
                           key=f"{table_name}_selection")

    # TODO: Fix wrong scaling for graph (no engine arg. in proto -> Consider showing image instead)
    # TODO: Fix chart not using layout engine
    st.graphviz_chart(str(st.session_state.layout), use_container_width=False)  # str to avoid graphviz from crashing on derived Graph class.


    # TODO: Add download/export buttons
    # TODO: Add user action logging
    # TODO: Add storing of exported hulks
    if IS_DEBUG:
        st.text("JSON Source")
        st.json(st.session_state.space_hulk.json(exclude_none=True), expanded=False)
        with st.expander("DOT Source"):
            st.text(st.session_state.layout)
