from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .map_object_size import MapObjectSize
from .map_object_size import MapObjectSizeConstraint
from .sequenced_die import SequencedSixSidedDieRange


class RandomTableEvent(BaseModel):
    name: str
    description: Optional[str] = None
    size: Optional[MapObjectSize] = None

    def is_sized(self) -> bool:
        return self.size is not None

    @property
    def name_with_description(self) -> str:
        return f"{self.name}{f' - {self.description}' if self.description else ''}"

    def __lt__(self, other: RandomTableEvent) -> bool:
        return self.name_with_description < other.name_with_description or (
            self.is_sized() and other.is_sized() and self.size < other.size
        )

    def __gt__(self, other: RandomTableEvent) -> bool:
        return self.name_with_description > other.name_with_description or (
            self.is_sized() and other.is_sized() and other.size < self.size
        )

    def __eq__(self, other: RandomTableEvent) -> bool:
        return not (self < other or self > other)

    def __hash__(self) -> int:
        return hash((self.name, self.description, self.size))


class RandomTableEventInfo(RandomTableEvent):
    range: SequencedSixSidedDieRange
    size_constraint: Optional[MapObjectSizeConstraint] = None

    def has_size_constraint(self) -> bool:
        return self.size_constraint is not None

    def as_event(self) -> RandomTableEvent:
        return RandomTableEvent(
            name=self.name,
            description=self.description,
            size=self.size_constraint.get_random_size() if self.has_size_constraint() else None,
        )


RandomTableEventInfoList = list[RandomTableEventInfo]
