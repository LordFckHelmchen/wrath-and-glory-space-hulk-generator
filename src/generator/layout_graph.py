import re
import tempfile
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from pathlib import Path
from typing import Optional

from graphviz import Graph
from pydantic import NonNegativeInt
from pydantic import PositiveFloat

from .indexable_enums import LayoutEdgeType
from .indexable_enums import LayoutEngine
from .indexable_enums import LayoutFormat
from .map_object_size import MapObjectSize
from .space_hulk import SpaceHulk


class NodeShape(Enum):
    RECTANGLE = "rectangle"
    OVAL = "oval"
    CIRCLE = "circle"
    OCTAGON = "octagon"


@dataclass
class Node:
    name: str
    size: MapObjectSize
    shape: NodeShape = NodeShape.RECTANGLE
    connected_nodes: list[str] = field(default_factory=list)

    def to_dot(self) -> dict[str, str]:
        return {
            "name": self.name,
            "width": str(self.size.x),
            "height": str(self.size.y),
            "shape": self.shape.value,
            "fixedsize": "true",
        }

    @property
    def number_of_connections(self) -> NonNegativeInt:
        return len(self.connected_nodes)


class GraphStats(ABC):
    @property
    @abstractmethod
    def number_of_nodes(self) -> NonNegativeInt:
        pass

    @property
    @abstractmethod
    def number_of_edges(self) -> NonNegativeInt:
        pass


class LayoutGraph(Graph, GraphStats):
    GRAPH_VIZ_EDGE_STRING_PATTERN = r"\t(\".+\"|.+) -- (\".+\"|.+)\n"

    @property
    def number_of_nodes(self) -> NonNegativeInt:
        return len(self.body) - self.number_of_edges

    @property
    def number_of_edges(self) -> NonNegativeInt:
        return sum(1 for element in self.body if re.match(pattern=self.GRAPH_VIZ_EDGE_STRING_PATTERN, string=element))

    @property
    def global_node_font_size(self) -> PositiveFloat:
        return float(self.node_attr.get("fontsize", "16"))

    @property
    def layout_edge_type(self) -> LayoutEdgeType:
        return LayoutEdgeType(self.graph_attr["splines"])

    @layout_edge_type.setter
    def layout_edge_type(self, edge_type: LayoutEdgeType) -> None:
        self.graph_attr["splines"] = edge_type.value

    @property
    def layout_engine(self) -> LayoutEngine:
        return LayoutEngine(self.engine)

    @layout_engine.setter
    def layout_engine(self, engine: LayoutEngine) -> None:
        self.engine = engine.value

    def __str__(self) -> str:
        original_comment = self.comment

        # Add layout engine as comment
        engine_comment = self._comment(f"Layout engine: {self.engine}")
        if not original_comment:
            self.comment = engine_comment
        elif engine_comment not in self.comment:
            self.comment = f"{self.comment}\n{engine_comment}"
        self_as_string = super().__str__()

        self.comment = original_comment

        return self_as_string

    def render_pdf(self, file_name: Path, space_hulk: Optional[SpaceHulk] = None) -> None:
        file_format = LayoutFormat.PDF.value

        def render_layout_pdf(name: Path) -> None:
            self.render(engine=self.engine, format=file_format, outfile=name, cleanup=True, view=False)

        if not space_hulk:
            render_layout_pdf(file_name)
            return

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_directory = Path(temp_dir)
            hulk_file = temp_directory / f"hulk.{file_format}"
            space_hulk.render_pdf(hulk_file)

            layout_file = temp_directory / f"layout.{file_format}"
            render_layout_pdf(layout_file)

            from PyPDF2 import PdfMerger

            merger = PdfMerger()
            for pdf in [hulk_file, layout_file]:
                merger.append(str(pdf))

            merger.write(str(file_name))
            merger.close()
