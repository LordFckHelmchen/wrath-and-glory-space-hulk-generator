import re
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from pathlib import Path

from graphviz import Graph
from pydantic import NonNegativeInt
from pydantic import PositiveFloat

from src.generator.map_object_size import MapObjectSize
from src.layouter.i_create_layouts import ILayout

from .graphviz_edge_type import GraphvizEdgeType
from .graphviz_engine import GraphvizEngine
from .graphviz_format import GraphvizFormat


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


class LayoutGraph(Graph, GraphStats, ILayout):
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
    def layout_edge_type(self) -> GraphvizEdgeType:
        return GraphvizEdgeType(self.graph_attr["splines"])

    @layout_edge_type.setter
    def layout_edge_type(self, edge_type: GraphvizEdgeType) -> None:
        self.graph_attr["splines"] = edge_type.value

    @property
    def layout_engine(self) -> GraphvizEngine:
        return GraphvizEngine(self.engine)

    @layout_engine.setter
    def layout_engine(self, engine: GraphvizEngine) -> None:
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

    def render_pdf(self, file_name: Path) -> None:
        self.render(engine=self.engine, format=GraphvizFormat.PDF.value, outfile=file_name, cleanup=True, view=False)
