from collections.abc import Generator
from copy import deepcopy
from typing import Optional

from pydantic import BaseModel
from pydantic import NonNegativeInt
from pydantic import PositiveInt
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
    events: list[RandomTableEvent]

    @validator("events", allow_reuse=True)
    def assure_events_are_sorted_and_unique(cls, events: list) -> list:
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

    def __setattr__(self, key: str, value):
        _ = getattr(self, key)  # Raise AttributeError if not present

        if key == "events":
            if not isinstance(value, type(self.events)) or not all(
                type(e) in self.__annotations__["events"].__args__ for e in value
            ):
                raise EventTypeError(f"'events' must be of type '{type(self.events)}', was '{type(value)}'")
            elif len(value) not in self.event_count_constraint:
                raise EventCountOutOfRangeError(
                    f"Event count out of range. "
                    f"'events' must have a number of elements within "
                    f"{self.event_count_constraint}, was {len(value)}."
                )

            value = self.assure_events_are_sorted_and_unique(value)
        elif len(self.events) not in value:  # key == "event_count_constraint":
            raise ValueError(
                f"Setting an event count constraint that would invalidate the current events. "
                f"Number of current events {len(self.events)}, 'event_count_constraint': {value}. "
                f"If this occurred during __init__, provide matching 'events'"
            )

        object.__setattr__(self, key, value)

    def __len__(self) -> NonNegativeInt:
        return len(self.events)

    def __iter__(self) -> Generator[RandomTableEvent, None, None]:
        yield from self.events

    def as_markdown(self, header: Optional[str] = None, header_level: PositiveInt = 1) -> str:
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
