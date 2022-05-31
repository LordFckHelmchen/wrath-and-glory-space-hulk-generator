import logging
from random import randint
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveInt
from pydantic import PrivateAttr
from pydantic import validator

from .map_object_size import MapObjectDimensionConstraint
from .map_object_size import MapObjectSize
from .map_object_size import MapObjectSizeConstraint
from .random_table_event_collection import EventCountConstraint
from .random_table_event_collection import RandomTableEvent
from .sequenced_die import SequencedDie
from .sequenced_die import SequencedSixSidedDieRange
from .space_hulk import RandomTableEventCollection


class RandomTableEventInfo(RandomTableEvent):
    range: SequencedSixSidedDieRange
    size_constraint: Optional[MapObjectSizeConstraint] = None

    def random_size(self) -> Optional[MapObjectSize]:
        if not self.has_size_constraint():
            return None

        size = MapObjectSize()
        for dim in ["x", "y"]:
            dim_size_constraint: MapObjectDimensionConstraint = getattr(self.size_constraint, dim)
            setattr(size, dim, randint(dim_size_constraint.minimum, dim_size_constraint.maximum))
        return size

    def has_size_constraint(self) -> bool:
        return self.size_constraint is not None

    def as_event(self) -> RandomTableEvent:
        return RandomTableEvent(name=self.name, description=self.description, size=self.random_size())


RandomTableEventInfoList = List[RandomTableEventInfo]


class RandomTable(BaseModel):
    table_name: str = Field(min_length=1)
    event_count_constraint: EventCountConstraint
    events: RandomTableEventInfoList

    _die: SequencedDie = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._die = SequencedDie.from_events(self.events)

        # check if events are consecutive
        for event_i, event_j in zip(self.events[0:-2], self.events[1:-1]):
            if not self._die.are_consecutive_rolls(event_i.range.maximum, event_j.range.minimum):
                logging.debug(f"Events should be consecutive for the die determination to work properly: "
                              f"'{event_i.name} {event_i.range}' is non-consecutive to "
                              f"'{event_j.name} {event_j.range}' -> determined die: {self._die}")

    @validator("events", allow_reuse=True)
    def assure_event_ranges_are_sorted_and_non_overlapping(cls,
                                                           events: RandomTableEventInfoList) -> RandomTableEventInfoList:
        events.sort(key=lambda x: x.range.minimum)
        for event_i, event_j in zip(events[0:-2], events[1:-1]):
            if event_i.range.maximum >= event_j.range.minimum:
                raise ValueError(f"Event ranges must be non-overlapping: "
                                 f"'{event_i.name} {event_i.range}' overlaps with '{event_j.name} {event_j.range}'")
        return events

    def generate_single_event(self) -> RandomTableEvent:
        while not (event_info := next((info for info in self.events if self._die.roll() in info.range), None)):
            logging.debug("Re-rolling due to result being in an non-consecutive area")

        return event_info.as_event()

    def generate_events(self, number_of_events: PositiveInt = 1) -> RandomTableEventCollection:
        if number_of_events > self.event_count_constraint.maximum:
            logging.warning(f"Number of events may not be larger than {self.event_count_constraint.maximum}: "
                            f"Was {number_of_events}")
            number_of_events = self.event_count_constraint.maximum

        return RandomTableEventCollection(events=[self.generate_single_event() for _ in range(number_of_events)],
                                          event_count_constraint=self.event_count_constraint)
