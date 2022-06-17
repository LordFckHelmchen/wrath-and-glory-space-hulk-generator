from pathlib import Path

import streamlit as st

from src.generator.indexable_enums import LayoutEdgeType
from src.generator.indexable_enums import LayoutEngine
from src.generator.indexable_enums import LayoutFormat
from src.generator.layout_graph import LayoutGraph


def make_file_name(layout_engine: LayoutEngine,
                   layout_edge_type: LayoutEdgeType,
                   layout_format: LayoutFormat,
                   base_path: Path = Path("space_hulks")) -> str:
    return str(base_path / f"{layout_engine.value}_{layout_edge_type.value}_layout.{layout_format.value}")


def create_layout_file(layout: LayoutGraph, layout_engine: LayoutEngine, layout_format: LayoutFormat) -> str:
    layout_edge_type = LayoutEdgeType(layout.graph_attr['splines'])
    return layout.render(engine=layout_engine.value,
                         format=layout_format.value,
                         outfile=make_file_name(layout_engine, layout_edge_type, layout_format),
                         cleanup=True,
                         view=False)


# noinspection PyUnusedLocal
@st.cache
def create_preview_file(layout: LayoutGraph,
                        layout_engine: LayoutEngine,
                        edge_type: LayoutEdgeType,  # Used for hashing
                        layout_format: LayoutFormat = LayoutFormat.PNG) -> str:
    """
    Short-cut function to cache the preview file as long as the layout and engine didn't change
    """

    return create_layout_file(layout, layout_engine=layout_engine, layout_format=layout_format)


# noinspection PyUnusedLocal
@st.cache
def create_download_file(layout: LayoutGraph,
                         layout_engine: LayoutEngine,
                         edge_type: LayoutEdgeType,  # Used for hashing
                         layout_format: LayoutFormat = LayoutFormat.PDF) -> str:
    """
    Short-cut function to cache the download file as long as the layout and engine didn't change
    """

    return create_layout_file(layout, layout_engine=layout_engine, layout_format=layout_format)
