import logging
import mimetypes
from pathlib import Path
from random import randint

import streamlit as st
import toml

from src.app.layout_file_creator import create_combined_file
from src.app.layout_file_creator import create_layout_preview_file
from src.generator.space_hulk_generator import RoomCount
from src.generator.space_hulk_generator import SpaceHulkGenerator
from src.layouter.graphviz_layouter.graphviz_edge_type import GraphvizEdgeType
from src.layouter.graphviz_layouter.graphviz_engine import GraphvizEngine
from src.layouter.graphviz_layouter.graphviz_layouter import GraphvizLayouter
from src.layouter.layouter_type import LayouterType

# Session state keys
GENERATOR_KEY = "generator"
LAYOUTER_KEY = "layouter"
LAYOUTER_TYPE = "layouter_type"
LAYOUT_EDGE_TYPE_KEY = "layout_edge_type"
LAYOUT_ENGINE_KEY = "layout_engine"
LAYOUT_KEY = "layout"
MIN_NUMBER_OF_ROOMS_KEY = "number_of_rooms_per_origin"
NUMBER_OF_EDGES_METRIC_KEY = "#Connections"
NUMBER_OF_ORIGINS_METRIC_KEY = "#Origins"
NUMBER_OF_ROOMS_IN_HULK_METRIC_KEY = "#Rooms"
SPACE_HULK_KEY = "space_hulk"

# Misc. Constants
DEFAULT_LAYOUTER = LayouterType.GRAPHVIZ
HELP_DATA: dict[str, Path] = {"About": Path("docs/APP_ABOUT.md"), "Usage": Path("docs/APP_USAGE.md")}
METRIC_STATE_ATTRIBUTE_MAP = {
    NUMBER_OF_ORIGINS_METRIC_KEY: (SPACE_HULK_KEY, "number_of_origins"),
    NUMBER_OF_ROOMS_IN_HULK_METRIC_KEY: (SPACE_HULK_KEY, "number_of_rooms"),
    NUMBER_OF_EDGES_METRIC_KEY: (LAYOUT_KEY, "number_of_edges"),
}


def is_space_hulk_created() -> bool:
    return SPACE_HULK_KEY in st.session_state


def create_new_hulk_and_layout() -> None:
    st.session_state[SPACE_HULK_KEY] = st.session_state[GENERATOR_KEY].create_hulk(
        number_of_rooms_per_origin=st.session_state[MIN_NUMBER_OF_ROOMS_KEY]
    )
    create_new_layout_if_hulk_is_created()


def create_new_layout_if_hulk_is_created() -> None:
    if is_space_hulk_created():
        st.session_state[LAYOUT_KEY] = st.session_state[LAYOUTER_KEY].create_layout(st.session_state[SPACE_HULK_KEY])
        update_metrics()


def store_layout_engine() -> None:
    st.session_state[LAYOUTER_KEY].set_layout_engine(st.session_state[LAYOUT_ENGINE_KEY])
    if LAYOUT_KEY in st.session_state:
        st.session_state[LAYOUT_KEY].layout_engine = st.session_state[LAYOUT_ENGINE_KEY]


def store_layout_edge_type() -> None:
    st.session_state[LAYOUTER_KEY].set_layout_edge_type(st.session_state[LAYOUT_EDGE_TYPE_KEY])
    if LAYOUT_KEY in st.session_state:
        st.session_state[LAYOUT_KEY].layout_edge_type = st.session_state[LAYOUT_EDGE_TYPE_KEY]


def update_metrics() -> None:
    st.session_state[NUMBER_OF_ROOMS_IN_HULK_METRIC_KEY] = st.session_state[SPACE_HULK_KEY].number_of_rooms
    st.session_state[NUMBER_OF_ORIGINS_METRIC_KEY] = st.session_state[SPACE_HULK_KEY].number_of_origins
    st.session_state[NUMBER_OF_EDGES_METRIC_KEY] = st.session_state[LAYOUT_KEY].number_of_edges


@st.experimental_memo
def get_app_version() -> str:
    with Path("pyproject.toml").open() as pyproject_toml_file:
        pyproject_toml = toml.load(pyproject_toml_file)
    try:
        return pyproject_toml["tool"]["poetry"]["version"]
    except KeyError:
        return ""


def recreate_hulk_and_layout_if_hulk_is_created() -> None:
    if is_space_hulk_created():
        create_new_hulk_and_layout()


def randomize_min_number_of_rooms() -> None:
    st.session_state[MIN_NUMBER_OF_ROOMS_KEY] = randint(RoomCount.ge, RoomCount.le)
    recreate_hulk_and_layout_if_hulk_is_created()


st.title("Wrath & Glory Space Hulk Generator")
metadata_cols = st.columns(2)
metadata_cols[0].write(
    "[![Star](https://img.shields.io/github/stars/LordFckHelmchen/wrath-and-glory-space-hulk-generator.svg?"
    "logo=github&style=social)](https://gitHub.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator)"
)
metadata_cols[1].write(f"![Version](https://img.shields.io/badge/version-{get_app_version()}-blue)")

for title, file in HELP_DATA.items():
    with st.expander(title):
        if title not in st.session_state:
            st.session_state[title] = file.read_text()
        st.markdown(st.session_state[title])

st.header("Generator Settings")

# Init state
if GENERATOR_KEY not in st.session_state:
    st.session_state[GENERATOR_KEY] = SpaceHulkGenerator()
if LAYOUTER_KEY not in st.session_state:
    st.session_state[LAYOUTER_KEY] = GraphvizLayouter()

generator_settings_columns = st.columns(2)

with generator_settings_columns[0]:
    st.slider(
        "Minimum number of rooms (per origin)",
        min_value=RoomCount.ge,
        max_value=RoomCount.le,
        value=10,
        key=MIN_NUMBER_OF_ROOMS_KEY,
        on_change=recreate_hulk_and_layout_if_hulk_is_created,
    )

    st.button("Randomize min. number of rooms", on_click=randomize_min_number_of_rooms)

with generator_settings_columns[1]:
    st.selectbox(
        "Layouter type",
        options=list(LayouterType),
        format_func=lambda x: x.value,
        index=st.session_state.get(LAYOUTER_TYPE, DEFAULT_LAYOUTER).index,
        key=LAYOUTER_TYPE,
    )

if st.session_state.get(LAYOUTER_TYPE, DEFAULT_LAYOUTER) == LayouterType.GRAPHVIZ:
    st.subheader("Layouter Settings")

    layouter_settings_columns = st.columns(2)

    with layouter_settings_columns[0]:
        st.selectbox(
            "Layout engine",
            options=list(GraphvizEngine),
            format_func=lambda x: x.value,
            index=st.session_state.get(LAYOUT_ENGINE_KEY, st.session_state[LAYOUTER_KEY].get_layout_engine()).index,
            key=LAYOUT_ENGINE_KEY,
            on_change=store_layout_engine,
        )

    with layouter_settings_columns[1]:
        st.selectbox(
            "Connection type",
            options=list(GraphvizEdgeType),
            format_func=lambda x: x.value,
            index=st.session_state.get(
                LAYOUT_EDGE_TYPE_KEY, st.session_state[LAYOUTER_KEY].get_layout_edge_type()
            ).index,
            key=LAYOUT_EDGE_TYPE_KEY,
            on_change=store_layout_edge_type,
        )

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
    preview_file_name = create_layout_preview_file(
        layout=st.session_state[LAYOUT_KEY],
        layout_engine=st.session_state[LAYOUT_ENGINE_KEY],
        edge_type=st.session_state[LAYOUT_EDGE_TYPE_KEY],
    )
    download_file_name = create_combined_file(
        space_hulk=st.session_state[SPACE_HULK_KEY], layout=st.session_state[LAYOUT_KEY]
    )

# Prepare download
with space_hulk_header_columns[2], Path(download_file_name).open("rb") as file:
    file_name = Path(file.name)
    st.download_button(
        label=f"Download {file_name.suffix.replace('.', '').upper()}",
        data=file,
        file_name=file_name.name,
        mime=mimetypes.guess_type(file_name)[0],
        on_click=lambda: logging.info(
            f"Space Hulk exported\n"
            f"number_of_rooms_per_origin: "
            f"{st.session_state[MIN_NUMBER_OF_ROOMS_KEY]}\n"
            f"{st.session_state[LAYOUT_KEY]}"
        ),
    )

# Show details
with st.expander("Details"):
    st.markdown(st.session_state[SPACE_HULK_KEY].as_markdown(header_level=3))

# Show metrics
metric_cols = st.columns(len(METRIC_STATE_ATTRIBUTE_MAP))
for index, (metric_key, (state_key, attribute_name)) in enumerate(METRIC_STATE_ATTRIBUTE_MAP.items()):
    metric_cols[index].metric(metric_key, value=getattr(st.session_state[state_key], attribute_name))

# Show preview
st.caption("Map preview - Use the download button above to access the vectorized version")
st.image(image=preview_file_name, use_column_width=True, width=20)
