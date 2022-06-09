from streamlit import cache

from src.generator.layout_engine import LayoutEngine
from src.generator.layout_graph import LayoutGraph
from src.generator.space_hulk_layouter import LayoutFormat


def create_layout_file(layout: LayoutGraph, layout_engine: LayoutEngine, layout_format: LayoutFormat) -> str:
    return layout.render(engine=layout_engine.value,
                         format=layout_format.value,
                         outfile=f"space_hulks/{layout_engine.value}_layout.{layout_format.value}",
                         cleanup=True,
                         view=False)


@cache
def create_preview_file(layout: LayoutGraph,
                        layout_engine: LayoutEngine,
                        layout_format: LayoutFormat = LayoutFormat.PNG) -> str:
    """
    Short-cut function to cache the preview file as long as the layout and engine didn't change
    """

    return create_layout_file(layout, layout_engine=layout_engine, layout_format=layout_format)


@cache
def create_download_file(layout: LayoutGraph,
                         layout_engine: LayoutEngine,
                         layout_format: LayoutFormat = LayoutFormat.PDF) -> str:
    """
    Short-cut function to cache the download file as long as the layout and engine didn't change
    """

    return create_layout_file(layout, layout_engine=layout_engine, layout_format=layout_format)
