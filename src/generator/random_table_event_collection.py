from collections.abc import Iterator
from copy import deepcopy
from typing import Literal

from pydantic.v1 import BaseModel
from pydantic.v1 import NonNegativeInt
from pydantic.v1 import PositiveInt
from pydantic.v1 import conint
from pydantic.v1 import validator

from .exceptions import EventCountOutOfRangeError
from .exceptions import EventTypeError
from .positive_int_range import PositiveIntRange
from .random_table_event import RandomTableEvent


class EventCountConstraint(PositiveIntRange):
    minimum: NonNegativeInt | None = 0
    maximum: conint(ge=0, le=1000) = 1000


class RandomTableEventCollection(BaseModel):
    event_count_constraint: EventCountConstraint
    events: list[RandomTableEvent]

    @validator("events", allow_reuse=True)
    def get_sorted_unique_events(self, events: list) -> list:
        event_counts = {}
        for event in events:
            if event.name not in event_counts:
                event_counts[event.name] = 1
            else:
                event_counts[event.name] += 1

        duplicated_event_ids = {event.name: 0 for event in events if event_counts[event.name] > 1}
        new_events = []
        for event in events:
            new_event = deepcopy(event)
            if event.name in duplicated_event_ids:
                duplicated_event_ids[event.name] += 1
                new_event.name = f"{event.name} No.{duplicated_event_ids[event.name]}"
            new_events.append(new_event)

        return sorted(new_events, key=lambda x: x.name)

    def is_valid_event_collection(self, values: object) -> bool:
        return isinstance(values, type(self.events)) and all(
            type(v) in self.__annotations__["events"].__args__ for v in values
        )

    def __setattr__(self, key: Literal["events", "event_count_constraint"], value: object) -> None:
        _ = getattr(self, key)  # Raise AttributeError if not present

        is_events = key == "events"

        if is_events and not self.is_valid_event_collection(value):
            msg = f"'events' must be of type '{type(self.events)}', was '{type(value)}'"
            raise EventTypeError(msg)

        if is_events and len(value) not in self.event_count_constraint:
            msg = (
                f"Event count out of range. "
                f"'events' must have a number of elements within {self.event_count_constraint}, was {len(value)}."
            )
            raise EventCountOutOfRangeError(msg)

        if not is_events and len(self.events) not in value:
            msg = (
                f"Setting an event count constraint that would invalidate the current events. "
                f"Number of current events {len(self.events)}, 'event_count_constraint': {value}. "
                f"If this occurred during __init__, provide matching 'events'"
            )
            raise ValueError(msg)

        # Sort if not "event_count_constraint"
        if is_events:
            value = self.get_sorted_unique_events(value)
        object.__setattr__(self, key, value)

    def __len__(self) -> NonNegativeInt:
        return len(self.events)

    def __iter__(self) -> Iterator[RandomTableEvent]:
        yield from self.events

    def as_markdown(self, header: str | None = None, header_level: PositiveInt = 1) -> str:
        self_as_string = [f"{'#' * header_level} {header} (n={len(self)})\n"] if header else []

        if len(self) == 0:
            self_as_string.append("None\n")
        elif len(self) == 1:
            self_as_string.append(f"{self.events[0].name_with_description}\n")
        else:
            self_as_string.append(
                "".join([f"{i}. {event.name_with_description}\n" for i, event in enumerate(self.events)])
            )

        return "\n".join(self_as_string)
