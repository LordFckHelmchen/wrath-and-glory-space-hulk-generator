import logging
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple

from pydantic import NonNegativeInt
from pydantic import PositiveFloat

from .layout_graph import GraphStats
from .layout_graph import LayoutGraph
from .layout_graph import Node


class LayoutGraphCreator(GraphStats):
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

    def add_node(self, node: Node) -> None:
        if node.name in self._nodes:
            logging.warning(f"Node '{node.name}' has already been added, ignoring duplicate!")
        self._nodes[node.name] = node

    def add_edge(self, from_node: str, to_node: str, avoid_duplicates: bool = True) -> None:
        if from_node not in self._nodes or to_node not in self._nodes:
            raise ValueError(f"unknown nodes {from_node} or {to_node}")

        edge = sorted((from_node, to_node))
        if not avoid_duplicates or edge not in self._edges:
            # noinspection PyTypeChecker
            self._edges.append(edge)

    def create(self, graph_attrs: Dict, add_node_size_to_node_label: bool = True) -> LayoutGraph:
        layout = LayoutGraph(**graph_attrs)
        largest_node_name = max(self._nodes.values(), key=lambda x: x.size.area).name
        for node in sorted(self._nodes.values(), key=lambda x: x.name):
            label = node.name.replace(' ', '\n')  # Make labels multi-line to avoid overfull boxes.
            if add_node_size_to_node_label:
                label = f"{label}\n{node.size.x}x{node.size.y} {node.size.unit.value}"
            layout.node(**node.to_dot(), label=label, root=str(node.name == largest_node_name).lower(),
                        fontsize=str(self._get_scaled_font_size(node, layout.global_node_font_size)))
        for edge in sorted(self._edges):
            layout.edge(*edge)
        return layout

    @property
    def number_of_nodes(self) -> NonNegativeInt:
        return len(self._nodes)

    @property
    def number_of_edges(self) -> NonNegativeInt:
        return len(self._edges)
