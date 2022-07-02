from pathlib import Path

import streamlit as st

from src.generator.indexable_enums import LayoutEdgeType
from src.generator.indexable_enums import LayoutEngine
from src.generator.indexable_enums import LayoutFormat
from src.generator.layout_graph import LayoutGraph
from src.generator.space_hulk import SpaceHulk


def make_file_name(layout_engine: LayoutEngine,
                   layout_edge_type: LayoutEdgeType,
                   layout_format: LayoutFormat,
                   base_path: Path = Path("space_hulks")) -> Path:
    return base_path / f"{layout_engine.value}_{layout_edge_type.value}_layout.{layout_format.value}"


@st.cache
def create_preview_file(layout: LayoutGraph,
                        layout_engine: LayoutEngine,  # Used for hashing
                        edge_type: LayoutEdgeType,  # Used for hashing
                        layout_format: LayoutFormat = LayoutFormat.PNG  # Used for hashing
                        ) -> str:
    """
    Caches the preview file as long as the layout and engine didn't change
    """
    return layout.render(engine=layout_engine.value,
                         format=layout_format.value,
                         outfile=str(make_file_name(layout_engine, edge_type, layout_format)),
                         cleanup=True,
                         view=False)


@st.cache
def create_download_file(space_hulk: SpaceHulk, layout: LayoutGraph) -> str:
    file_name = make_file_name(layout.layout_engine, layout.layout_edge_type, LayoutFormat.PDF)
    layout.render_pdf(file_name=file_name, space_hulk=space_hulk)
    return str(file_name)
