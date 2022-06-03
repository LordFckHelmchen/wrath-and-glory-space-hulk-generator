from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import NonNegativeInt
from pydantic import conint
from pydantic import validator

from .exceptions import EventCountOutOfRangeError
from .exceptions import EventTypeError
from .positive_int_range import PositiveIntRange
from .random_table_event import RandomTableEvent


class EventCountConstraint(PositiveIntRange):
    minimum: Optional[NonNegativeInt] = 0
    maximum: conint(ge=0, le=1000) = 1000


class RandomTableEventCollection(BaseModel):
    event_count_constraint: EventCountConstraint
    events: List[RandomTableEvent]

    @validator("events", allow_reuse=True)
    def assure_events_are_sorted(cls, events: List) -> List:
        return sorted(events)

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

            value.sort()
        elif len(self.events) not in value:  # key == "event_count_constraint":
            raise ValueError(f"Setting an event count constraint that would invalidate the current events. "
                             f"Number of current events {len(self.events)}, 'event_count_constraint': {value}. "
                             f"If this occurred during __init__, provide matching 'events'")

        object.__setattr__(self, key, value)

    def __len__(self) -> NonNegativeInt:
        return len(self.events)

    def __iter__(self) -> RandomTableEvent:
        for event in self.events:
            yield event