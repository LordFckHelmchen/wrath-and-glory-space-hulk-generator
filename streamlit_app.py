import logging
from pathlib import Path

import streamlit as st

from src.wrath_and_glory_space_hulk_generator.exceptions import EventCountOutOfRangeError
from src.wrath_and_glory_space_hulk_generator.layout_engine import LayoutEngine
from src.wrath_and_glory_space_hulk_generator.layout_graph import LayoutGraph
from src.wrath_and_glory_space_hulk_generator.space_hulk_generator import RoomCount
from src.wrath_and_glory_space_hulk_generator.space_hulk_generator import SpaceHulkGenerator
from src.wrath_and_glory_space_hulk_generator.space_hulk_layouter import LayoutFormat
from src.wrath_and_glory_space_hulk_generator.space_hulk_layouter import SpaceHulkLayouter

# st.set_page_config(layout="wide")

IS_DEBUG = True
PREVIEW_FILE_ID = "preview_file"
DOWNLOAD_FILE_ID = "download_file"
LAYOUT_FILE_PROPERTIES = {PREVIEW_FILE_ID: {"format": LayoutFormat.PNG.value},
                          DOWNLOAD_FILE_ID: {"format": LayoutFormat.PDF.value, "mime": "application/pdf"}}
for sink_id, sink_props in LAYOUT_FILE_PROPERTIES.items():
    LAYOUT_FILE_PROPERTIES[sink_id]["file"] = Path(f"space_hulks/layout.{sink_props['format']}")


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
        st.session_state.layout.LAYOUT_ENGINE_KEY = st.session_state.layout_engine.value
        create_new_layout_if_hulk_is_created()


NUMBER_OF_ORIGINS_METRIC_KEY = "#Origins"
NUMBER_OF_ROOMS_IN_HULK_METRIC_KEY = "#Rooms"
NUMBER_OF_EDGES_METRIC_KEY = "#Connections"


def update_metrics() -> None:
    st.session_state[NUMBER_OF_ROOMS_IN_HULK_METRIC_KEY] = st.session_state.space_hulk.number_of_rooms
    st.session_state[NUMBER_OF_ORIGINS_METRIC_KEY] = st.session_state.space_hulk.number_of_origins
    st.session_state[NUMBER_OF_EDGES_METRIC_KEY] = st.session_state.layout.number_of_edges


def on_hulk_property_change_callback(table_name: str) -> None:
    widget_name = f"{table_name}_selection"

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
        st.session_state[NUMBER_OF_ORIGINS_METRIC_KEY] = st.session_state.space_hulk.number_of_origins


@st.cache
def create_layout_files(layout: LayoutGraph) -> None:
    for sink_id, sink_props in LAYOUT_FILE_PROPERTIES.items():
        layout.format = sink_props['format']
        layout.render(outfile=str(sink_props["file"]), cleanup=True, view=False)


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

LAYOUT_ENGINE_KEY = "layout_engine"
st.selectbox("Layout engine",
             options=list(LayoutEngine),
             format_func=lambda x: x.value,
             index=LayoutEngine.index(st.session_state.get(LAYOUT_ENGINE_KEY,
                                                           SpaceHulkLayouter.DEFAULT_GRAPH_PROPERTIES["engine"])),
             key=LAYOUT_ENGINE_KEY,
             on_change=recreate_layout_with_new_engine_if_layout_is_created)

if st.button("Create new hulk?"):
    create_new_hulk_and_layout()

if is_space_hulk_created():
    st.header("Space Hulk")

    # TODO: Add name & description field

    metric_cols = st.columns(4)
    metric_cols[0].metric(NUMBER_OF_ORIGINS_METRIC_KEY, value=st.session_state.space_hulk.number_of_origins)
    metric_cols[1].metric(NUMBER_OF_ROOMS_IN_HULK_METRIC_KEY, value=st.session_state.space_hulk.number_of_rooms)
    metric_cols[2].metric(NUMBER_OF_EDGES_METRIC_KEY, value=st.session_state.layout.number_of_edges)

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

    with st.spinner("Rendering layout..."):
        create_layout_files(st.session_state.layout)

    # Show preview
    st.image(image=str(LAYOUT_FILE_PROPERTIES[PREVIEW_FILE_ID]["file"]), use_column_width=True, width=20)

    # Prepare download
    with LAYOUT_FILE_PROPERTIES[DOWNLOAD_FILE_ID]["file"].open("rb") as file:
        st.download_button(label=f"Download {LAYOUT_FILE_PROPERTIES[DOWNLOAD_FILE_ID]['format'].upper()}",
                           data=file,
                           file_name=LAYOUT_FILE_PROPERTIES[DOWNLOAD_FILE_ID]["file"].name,
                           mime=LAYOUT_FILE_PROPERTIES[DOWNLOAD_FILE_ID]['mime'],
                           on_click=lambda: logging.info(f"Space Hulk exported\n"
                                                         f"number_of_rooms_per_origin: "
                                                         f"{st.session_state.number_of_rooms_per_origin}\n"
                                                         f"{st.session_state.layout}"))

    if IS_DEBUG:
        st.text("JSON Source")
        st.json(st.session_state.space_hulk.json(exclude_none=True), expanded=False)
        with st.expander("DOT Source"):
            st.text(st.session_state.layout)
