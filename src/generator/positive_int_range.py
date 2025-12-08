from collections.abc import Iterator
from typing import SupportsInt

from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import validator

from .exceptions import RangeNotSortedError


class PositiveIntRange(BaseModel):
    minimum: PositiveInt
    maximum: PositiveInt

    @validator("maximum", allow_reuse=True)
    def assert_min_not_larger_than_max(self, maximum: PositiveInt, values: dict[str, PositiveInt]) -> PositiveInt:
        if (minimum := values.get("minimum", False)) and minimum > maximum:
            msg = f"Maximum must be larger than minimum, was: minimum {minimum}, maximum {maximum}"
            raise RangeNotSortedError(msg)
        return maximum

    def __contains__(self, other: SupportsInt) -> bool:
        return self.minimum <= int(other) <= self.maximum

    def __iter__(self) -> Iterator[PositiveInt]:
        yield self.minimum
        yield self.maximum
