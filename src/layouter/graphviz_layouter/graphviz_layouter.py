import random
from copy import copy
from random import randint

from pydantic import PositiveInt
from pydantic.types import PositiveFloat

from src.generator.map_object_size import GlobalMapObjectSizeConstraint
from src.generator.random_table_event import RandomTableEvent
from src.generator.space_hulk import SpaceHulk
from src.layouter.i_create_layouts import ICreateLayouts

from .graphviz_edge_type import GraphvizEdgeType
from .graphviz_engine import GraphvizEngine
from .layout_graph import LayoutGraph
from .layout_graph import Node
from .layout_graph_creator import GraphProperties
from .layout_graph_creator import LayoutGraphCreator

DEFAULT_EDGE_TYPE = GraphvizEdgeType.ORTHO
DEFAULT_LAYOUT_ENGINE = GraphvizEngine.FDP
DEFAULT_GRAPH_PROPERTIES: GraphProperties = {
    "engine": DEFAULT_LAYOUT_ENGINE.value,
    "graph_attr": {
        "bgcolor": "black",
        "center": "true",
        "dpi": "1280",
        "margin": "0",
        "pad": "2",
        "rankdir": "TD",
        "size": "1,1",
        "splines": DEFAULT_EDGE_TYPE.value,
        "sep": "+20",
        "esep": "+40",
        "K": "8",
        "concentrate": "true",
    },
    "node_attr": {"color": "gray", "fillcolor": "white", "fontsize": "20", "penwidth": "13", "style": "filled"},
    "edge_attr": {"color": "gray", "penwidth": "25"},
}


class GraphvizLayouter(ICreateLayouts):
    MAX_FONT_SIZE = 700

    def __init__(
        self, max_number_of_connections_per_room: PositiveInt = 10, graph_properties: GraphProperties | None = None
    ) -> None:
        """
        Create a new GraphvizLayouter.

        Parameters
        ----------
        max_number_of_connections_per_room
            The max. number of edges per node (e.g. the max. degree). The lower the number, the more connected and
            regular the layout gets. Higher numbers will cause more clustered layouts.
        graph_properties
            graphviz properties for the layout. Default: DEFAULT_GRAPH_PROPERTIES
        """
        self.max_number_of_connections_per_room = max_number_of_connections_per_room
        self.graph_properties = (graph_properties if graph_properties else {}) | DEFAULT_GRAPH_PROPERTIES

    @staticmethod
    def _get_other_room(current_room: RandomTableEvent, space_hulk: SpaceHulk) -> RandomTableEvent:
        other_room = random.choice(space_hulk.rooms.events)
        while other_room.name == current_room.name:
            other_room = random.choice(space_hulk.rooms.events)
        return other_room

    def create_layout(self, space_hulk: SpaceHulk) -> LayoutGraph:
        def get_scaled_font_size(node: Node, base_font_size: PositiveFloat) -> PositiveFloat:
            slope = (self.MAX_FONT_SIZE - base_font_size) / (
                GlobalMapObjectSizeConstraint.x.maximum - GlobalMapObjectSizeConstraint.x.minimum
            )
            offset = base_font_size - slope * GlobalMapObjectSizeConstraint.x.minimum
            return round(slope * float(node.size.x) + offset)

        layout_creator = LayoutGraphCreator(get_scaled_font_size=get_scaled_font_size)
        for room in space_hulk.rooms:
            layout_creator.add_node(Node(name=room.name, size=room.size))

        # Populate each room with at least one connection to another room
        unconnected_rooms = copy(space_hulk.rooms.events)
        room = unconnected_rooms.pop(0)
        while any(unconnected_rooms):
            for _ in range(random.randrange(1, self.max_number_of_connections_per_room)):
                if any(unconnected_rooms):
                    other_room = unconnected_rooms.pop(randint(0, len(unconnected_rooms) - 1))
                else:
                    other_room = self._get_other_room(room, space_hulk)
                layout_creator.add_edge(room.name, other_room.name)
            # noinspection PyUnboundLocalVariable
            room = other_room  # Assure connected graph; will always be set

        return layout_creator.create(self.graph_properties | {"comment": space_hulk.json()})

    def set_layout_edge_type(self, edge_type: GraphvizEdgeType) -> None:
        self.graph_properties["graph_attr"]["splines"] = edge_type.value

    def get_layout_edge_type(self) -> GraphvizEdgeType:
        return GraphvizEdgeType(self.graph_properties["graph_attr"]["splines"])

    def set_layout_engine(self, engine: GraphvizEngine) -> None:
        self.graph_properties["engine"] = engine.value

    def get_layout_engine(self) -> GraphvizEngine:
        return GraphvizEngine(self.graph_properties["engine"])
