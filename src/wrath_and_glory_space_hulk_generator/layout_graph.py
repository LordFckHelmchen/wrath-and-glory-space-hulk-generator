import re
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple

from graphviz import Graph
from pydantic import NonNegativeInt
from pydantic import PositiveFloat

from .map_object_size import MapObjectSize


class NodeShape(Enum):
    RECTANGLE = "rectangle"
    OVAL = "oval"
    EGG = "egg"
    OCTAGON = "octagon"


@dataclass
class Node:
    name: str
    size: MapObjectSize
    shape: NodeShape = NodeShape.RECTANGLE
    connected_nodes: List[str] = field(default_factory=list)

    def to_dot(self) -> Dict[str, str]:
        return {"name": self.name, "width": str(self.size.x), "height": str(self.size.y), "shape": self.shape.value,
                "fixedsize": "true"}

    @property
    def number_of_connections(self) -> NonNegativeInt:
        return len(self.connected_nodes)


class LayoutGraph(Graph):
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


class LayoutGraphCreator:
    def __init__(self, get_scaled_font_size: Callable[[Node, PositiveFloat], PositiveFloat] = lambda n, s: s):
        """
        Constructor

        :param get_scaled_font_size: A lambda that takes the base font size (either from the layout or a default value
        of 16) and a Node and returns a scaled font size. This can be used to adjust the font size to a nodes attributes
        (e.g. its size).
        """
        self._nodes: Dict[str, Node] = {}
        self._edges: List[Tuple[str, str]] = []
        self._get_scaled_font_size = get_scaled_font_size

    def add_node(self, node: Node):
        # TODO: Allow duplicated rooms!
        self._nodes[node.name] = node

    def add_edge(self, from_node: str, to_node: str, avoid_duplicates: bool = True):
        if from_node not in self._nodes or to_node not in self._nodes:
            raise IOError(f"unknown nodes {from_node} or {to_node}")

        edge = sorted((from_node, to_node))
        if not avoid_duplicates or edge not in self._edges:
            # noinspection PyTypeChecker
            self._edges.append(edge)

    def create(self, graph_attrs: Dict) -> LayoutGraph:
        layout = LayoutGraph(**graph_attrs)
        largest_node_name = max(self._nodes.values(), key=lambda x: x.size.area).name
        for node in sorted(self._nodes.values(), key=lambda x: x.name):
            label = node.name.replace(' ', '\n')
            label = f"{label}\n{node.size.x}x{node.size.y} {node.size.unit.value}"
            layout.node(**node.to_dot(), label=label,  # Nake multi-line labels.
                        root=str(node.name == largest_node_name).lower(),
                        fontsize=str(self._get_scaled_font_size(node, layout.global_node_font_size)))
        for edge in sorted(self._edges):
            layout.edge(*edge)
        return layout
