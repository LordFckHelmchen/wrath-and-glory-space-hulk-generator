import random
from copy import copy
from enum import Enum
from random import randint
from typing import Dict
from typing import Optional
from typing import Union

from pydantic import NonNegativeInt
from pydantic import PositiveInt

from .layout_graph import LayoutGraph
from .layout_graph import LayoutGraphCreator
from .layout_graph import Node
from .map_object_size import GlobalMapObjectSizeConstraint
from .random_table_event_collection import RandomTableEvent
from .space_hulk import SpaceHulk


class LayoutEngine(Enum):
    CIRCO = "circo"
    FDP = "fdp"
    OSAGE = "osage"

    @classmethod
    def index(cls, value_or_member: Union[str, "LayoutEngine"]) -> NonNegativeInt:
        return list(cls).index(LayoutEngine(value_or_member))


GraphProperties = Dict[str, Union[str, Dict[str, str]]]


class SpaceHulkLayouter:
    DEFAULT_GRAPH_PROPERTIES: GraphProperties = {"engine": LayoutEngine.FDP.value,
                                                 "graph_attr": {"bgcolor": "black", "center": "true", "margin": "0",
                                                                "pad": "2", "splines": "ortho"},
                                                 "node_attr": {"color": "white", "fontsize": "20", "style": "filled"},
                                                 "edge_attr": {"color": "white", "penwidth": "25"}}
    MAX_FONT_SIZE = 700

    def __init__(self):
        pass

    def create_layout(self,
                      space_hulk: SpaceHulk,
                      engine: Optional[LayoutEngine] = None,
                      max_number_of_connections_per_room: PositiveInt = 10) -> LayoutGraph:
        """

        :param space_hulk:
        :param engine:
        :param max_number_of_connections_per_room: The lower the number, the more connected and regular the layout gets.
        Higher numbers will cause more clustered layouts.
        :return:
        """

        def get_scaled_font_size(node: Node, base_font_size: float):
            slope = (self.MAX_FONT_SIZE - base_font_size) / (
                    GlobalMapObjectSizeConstraint.x.maximum - GlobalMapObjectSizeConstraint.x.minimum)
            offset = base_font_size - slope * GlobalMapObjectSizeConstraint.x.minimum
            return round(slope * float(node.size.x) + offset)

        layout_creator = LayoutGraphCreator(get_scaled_font_size=get_scaled_font_size)
        for room in space_hulk.rooms:
            layout_creator.add_node(Node(name=room.name, size=room.size))

        # Populate each room with at least one connection to another room
        unconnected_rooms = copy(space_hulk.rooms.events)
        room = unconnected_rooms.pop(0)
        while any(unconnected_rooms):
            for connection_id in range(random.randrange(1, max_number_of_connections_per_room)):
                if any(unconnected_rooms):
                    other_room = unconnected_rooms.pop(randint(0, len(unconnected_rooms) - 1))
                else:
                    other_room = self._get_other_room(room, space_hulk)
                layout_creator.add_edge(room.name, other_room.name)
            # noinspection PyUnboundLocalVariable
            room = other_room  # Assure connected graph; will always be set

        engine_attr = {"engine": engine.value} if engine else {}  # Use default if None
        return layout_creator.create(self.DEFAULT_GRAPH_PROPERTIES | engine_attr)

    @staticmethod
    def _get_other_room(current_room: RandomTableEvent, space_hulk: SpaceHulk,
                        avoid_self_connection: bool = True) -> RandomTableEvent:
        other_room = random.choice(space_hulk.rooms.events)
        while avoid_self_connection and other_room.name == current_room.name:
            other_room = random.choice(space_hulk.rooms.events)
        return other_room
