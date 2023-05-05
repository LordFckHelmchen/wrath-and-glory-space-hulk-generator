import tempfile
from pathlib import Path

import streamlit as st
from PyPDF2 import PdfMerger

from src.generator.space_hulk import SpaceHulk
from src.layouter.graphviz_layouter.graphviz_edge_type import GraphvizEdgeType
from src.layouter.graphviz_layouter.graphviz_engine import GraphvizEngine
from src.layouter.graphviz_layouter.graphviz_format import GraphvizFormat
from src.layouter.graphviz_layouter.layout_graph import LayoutGraph

DEFAULT_BASE_PATH = Path("space_hulks")


def make_file_name(
    layout_engine: GraphvizEngine,
    layout_edge_type: GraphvizEdgeType,
    layout_format: GraphvizFormat,
    base_path: Path = DEFAULT_BASE_PATH,
) -> Path:
    return base_path / f"{layout_engine.value}_{layout_edge_type.value}_layout.{layout_format.value}"


@st.cache
def create_layout_preview_file(
    layout: LayoutGraph,
    layout_engine: GraphvizEngine,  # Used for hashing
    edge_type: GraphvizEdgeType,  # Used for hashing
    layout_format: GraphvizFormat = GraphvizFormat.PNG,  # Used for hashing
) -> str:
    """
    Caches the preview file as long as the layout and engine didn't change
    """
    return layout.render(
        engine=layout_engine.value,
        format=layout_format.value,
        outfile=str(make_file_name(layout_engine, edge_type, layout_format)),
        cleanup=True,
        view=False,
    )


@st.cache
def create_combined_file(space_hulk: SpaceHulk, layout: LayoutGraph) -> str:
    """Create a full file with space hulk description & rendered layout"""
    file_format = GraphvizFormat.PDF
    file_name = make_file_name(layout.layout_engine, layout.layout_edge_type, file_format)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_directory = Path(temp_dir)
        merger = PdfMerger()
        for obj in [space_hulk, layout]:
            obj_file_name = temp_directory / f"{type(obj).__name__}.{file_format}"
            obj.render_pdf(obj_file_name)
            merger.append(str(obj_file_name))

        merger.write(str(file_name))
        merger.close()

    return str(file_name)
