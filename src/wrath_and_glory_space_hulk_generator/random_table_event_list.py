from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import NonNegativeInt
from pydantic import conint

from .exceptions import EventCountOutOfRangeError
from .exceptions import EventTypeError
from .map_object_size import MapObjectSize
from .positive_int_range import PositiveIntRange


class RandomTableEvent(BaseModel):
    name: str
    description: Optional[str] = None

    @property
    def name_with_description(self) -> str:
        return f"{self.name}{f' - {self.description}' if self.description else ''}"


class SizedRandomTableEvent(RandomTableEvent):
    size: MapObjectSize


class EventCountConstraint(PositiveIntRange):
    minimum: Optional[NonNegativeInt] = 0
    maximum: conint(ge=0, le=1000) = 1000


AnyRandomTableEvent = Union[RandomTableEvent, SizedRandomTableEvent]


class RandomTableEventList(BaseModel):
    event_count_constraint: EventCountConstraint
    events: List[RandomTableEvent]

    def __setattr__(self, key: str, value):
        _ = getattr(self, key)  # Raise AttributeError if not present

        if key == "events":
            if not isinstance(value, type(self.events)) or not all(
                    type(e) in self.__annotations__["events"].__args__ for e in value):
                raise EventTypeError(f"'events' must be of type '{type(self.events)}', was '{type(value)}'")
            elif len(value) not in self.event_count_constraint:
                raise EventCountOutOfRangeError(f"Event count out of range. "
                                                f"'events' must have a number of elements within "
                                                f"{self.event_count_constraint}, was {len(value)}.")
        else:  # key == "event_count_constraint":
            if len(self.events) not in value:
                raise ValueError(f"Setting an event count constraint that would invalidate the current events. "
                                 f"Number of current events {len(self.events)}, "
                                 f"'event_count_constraint': {value}. "
                                 f"If this occurred during __init__, provide matching 'events'")

        object.__setattr__(self, key, value)

    def __len__(self) -> NonNegativeInt:
        return len(self.events)

    def __iter__(self) -> RandomTableEvent:
        for event in self.events:
            yield event
        # yield "events", self.events
        # yield "event_count_constraint", self.event_count_constraint


class SizedRandomTableEventList(RandomTableEventList):
    events: List[SizedRandomTableEvent]

    def __iter__(self):
        return super().__iter__()
