import tempfile
import uuid
from pathlib import Path

import streamlit as st
from PyPDF2 import PdfMerger

from src.generator.space_hulk import SpaceHulk
from src.layouter.i_layout import ILayout
from src.layouter.layout_file_type import LayoutFileType


def make_file_name(file_type: LayoutFileType, postfix: str = "") -> Path:
    return Path("space_hulks") / f"space_hulk_{uuid.uuid4()}{postfix}.{file_type.value}"


@st.cache
def create_layout_preview_file(layout: ILayout, file_type: LayoutFileType = LayoutFileType.PNG) -> str:
    """
    Caches the preview file as long as the layout and engine didn't change
    """
    file_name = make_file_name(file_type, postfix="_preview")
    layout.render_to_file(file_name=file_name)
    return str(file_name)


@st.cache
def create_combined_file(space_hulk: SpaceHulk, layout: ILayout) -> str:
    """Create a full file with space hulk description & rendered layout"""
    file_type = LayoutFileType.PDF
    file_name = make_file_name(file_type)

    # Merge description & layout into single PDF
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_directory = Path(temp_dir)
        merger = PdfMerger()
        for obj in [space_hulk, layout]:
            obj_file_name = temp_directory / f"{type(obj).__name__}{file_name.suffix}"  # Use '.ext'-behavior of Path
            obj.render_to_file(file_name=obj_file_name)
            merger.append(str(obj_file_name))

        merger.write(str(file_name))
        merger.close()

    return str(file_name)
