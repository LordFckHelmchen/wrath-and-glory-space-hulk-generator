import logging
import mimetypes
from enum import Enum
from pathlib import Path
from random import randint

import streamlit as st
from pydantic import NonNegativeInt

from src.app.layout_file_creator import create_download_file
from src.app.layout_file_creator import create_preview_file
from src.generator.indexable_enums import LayoutEdgeType
from src.generator.indexable_enums import LayoutEngine
from src.generator.space_hulk_generator import RoomCount
from src.generator.space_hulk_generator import SpaceHulkGenerator
from src.generator.space_hulk_layouter import SpaceHulkLayouter

# st.set_page_config(layout="wide")

IS_DEBUG = False
LAYOUT_ENGINE_KEY = "layout_engine"


def is_space_hulk_created() -> bool:
    return "space_hulk" in st.session_state


def create_new_hulk_and_layout():
    st.session_state.space_hulk = st.session_state.generator.create_hulk(
        number_of_rooms_per_origin=st.session_state.number_of_rooms_per_origin)
    create_new_layout_if_hulk_is_created()


def create_new_layout_if_hulk_is_created() -> None:
    if is_space_hulk_created():
        st.session_state.layout = SpaceHulkLayouter().create_layout(st.session_state.space_hulk,
                                                                    engine=st.session_state[LAYOUT_ENGINE_KEY])
        update_metrics()


LAYOUT_KEY = "layout"


def assign_engine_to_layout_if_layout_is_created() -> None:
    if LAYOUT_KEY in st.session_state:
        st.session_state.layout.engine = st.session_state[LAYOUT_ENGINE_KEY].value


def assign_edge_type_to_layout_if_layout_is_created() -> None:
    if LAYOUT_KEY in st.session_state:
        st.session_state.layout.graph_attr["splines"] = st.session_state[LAYOUT_EDGE_TYPE_KEY].value


NUMBER_OF_ORIGINS_METRIC_KEY = "#Origins"
NUMBER_OF_ROOMS_IN_HULK_METRIC_KEY = "#Rooms"
NUMBER_OF_EDGES_METRIC_KEY = "#Connections"


def update_metrics() -> None:
    st.session_state[NUMBER_OF_ROOMS_IN_HULK_METRIC_KEY] = st.session_state.space_hulk.number_of_rooms
    st.session_state[NUMBER_OF_ORIGINS_METRIC_KEY] = st.session_state.space_hulk.number_of_origins
    st.session_state[NUMBER_OF_EDGES_METRIC_KEY] = st.session_state.layout.number_of_edges


def get_enum_index_and_update_state(state_key: str, indexable_enum_class, default: Enum) -> NonNegativeInt:
    member = st.session_state.get(state_key, indexable_enum_class(default))

    try:
        return indexable_enum_class.index(member)
    except TypeError as err:
        new_member = str(member).split(".")[-1].lower()
        logging.warning(f"Couldn't retrieve the index for '{member}' from '{indexable_enum_class}'. "
                        f"Retrying with stringified engine name '{new_member}'", exc_info=err)

    # This should never happen but it those. State is something like 'ENUM.MEMBER', so let's try to stringify
    # it and then use the name to retrieve the index.
    new_member = indexable_enum_class(new_member)
    st.session_state[state_key] = new_member
    return LayoutEngine.index(new_member)


def get_index_of_current_layout_engine() -> NonNegativeInt:
    return get_enum_index_and_update_state(LAYOUT_ENGINE_KEY,
                                           indexable_enum_class=LayoutEngine,
                                           default=LayoutEngine(SpaceHulkLayouter.DEFAULT_GRAPH_PROPERTIES["engine"]))


def get_index_of_current_edge_type() -> NonNegativeInt:
    return get_enum_index_and_update_state(LAYOUT_EDGE_TYPE_KEY,
                                           indexable_enum_class=LayoutEdgeType,
                                           default=LayoutEdgeType(
                                               SpaceHulkLayouter.DEFAULT_GRAPH_PROPERTIES["graph_attr"]["splines"]))


st.title("Wrath & Glory Space Hulk Generator")

if "generator" not in st.session_state:
    st.session_state.generator = SpaceHulkGenerator()

st.header("Generator Settings")


def recreate_hulk_and_layout_if_hulk_is_created() -> None:
    if is_space_hulk_created():
        create_new_hulk_and_layout()


generator_settings_columns = st.columns(3)

MIN_NUMBER_OF_ROOMS_KEY = "number_of_rooms_per_origin"
with generator_settings_columns[0]:
    st.slider("Minimum number of rooms (per origin)",
              min_value=RoomCount.ge,
              max_value=RoomCount.le,
              value=10,
              key=MIN_NUMBER_OF_ROOMS_KEY,
              on_change=recreate_hulk_and_layout_if_hulk_is_created)


    def randomize_min_number_of_rooms() -> None:
        st.session_state[MIN_NUMBER_OF_ROOMS_KEY] = randint(RoomCount.ge, RoomCount.le)
        recreate_hulk_and_layout_if_hulk_is_created()


    st.button("Randomize min. number of rooms", on_click=randomize_min_number_of_rooms)

with generator_settings_columns[1]:
    st.selectbox("Layout engine",
                 options=list(LayoutEngine),
                 format_func=lambda x: x.value,
                 index=get_index_of_current_layout_engine(),
                 key=LAYOUT_ENGINE_KEY,
                 on_change=assign_engine_to_layout_if_layout_is_created)

LAYOUT_EDGE_TYPE_KEY = "layout_edge_type"
with generator_settings_columns[2]:
    st.selectbox("Connection type",
                 options=list(LayoutEdgeType),
                 format_func=lambda x: x.value,
                 index=get_index_of_current_edge_type(),
                 key=LAYOUT_EDGE_TYPE_KEY,
                 on_change=assign_edge_type_to_layout_if_layout_is_created)

st.header("Space Hulk")

space_hulk_header_columns = st.columns(3)

with space_hulk_header_columns[0]:
    if st.button("Create new hulk?"):
        create_new_hulk_and_layout()

if not is_space_hulk_created():
    st.stop()

with space_hulk_header_columns[1]:
    if st.button("Create new layout?"):
        create_new_layout_if_hulk_is_created()

with st.spinner("Rendering layout..."):
    preview_file = create_preview_file(st.session_state.layout,
                                       layout_engine=st.session_state[LAYOUT_ENGINE_KEY],
                                       edge_type=st.session_state[LAYOUT_EDGE_TYPE_KEY])
    download_file = create_download_file(st.session_state.layout,
                                         layout_engine=st.session_state[LAYOUT_ENGINE_KEY],
                                         edge_type=st.session_state[LAYOUT_EDGE_TYPE_KEY])

# Show preview
st.caption("Map preview - Use the download button above to access the vectorized version")
st.image(image=preview_file, use_column_width=True, width=20)

# Prepare download
with space_hulk_header_columns[2], open(download_file, "rb") as file:
    file_name = Path(file.name)
    st.download_button(label=f"Download {file_name.suffix.replace('.', '').upper()}",
                       data=file,
                       file_name=file_name.name,
                       mime=mimetypes.guess_type(file_name)[0],
                       on_click=lambda: logging.info(f"Space Hulk exported\n"
                                                     f"number_of_rooms_per_origin: "
                                                     f"{st.session_state.number_of_rooms_per_origin}\n"
                                                     f"{st.session_state.layout}"))

metric_cols = st.columns(4)
metric_cols[0].metric(NUMBER_OF_ORIGINS_METRIC_KEY, value=st.session_state.space_hulk.number_of_origins)
metric_cols[1].metric(NUMBER_OF_ROOMS_IN_HULK_METRIC_KEY, value=st.session_state.space_hulk.number_of_rooms)
metric_cols[2].metric(NUMBER_OF_EDGES_METRIC_KEY, value=st.session_state.layout.number_of_edges)

if not IS_DEBUG:
    st.stop()

st.text("JSON Source")
st.json(st.session_state.space_hulk.json(exclude_none=True), expanded=False)
with st.expander("DOT Source"):
    st.text(st.session_state.layout)
with st.expander("Session state"):
    st.write(st.session_state)
