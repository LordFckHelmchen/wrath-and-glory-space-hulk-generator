from typing import Dict
from typing import SupportsInt

from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import validator


class PositiveIntRange(BaseModel):
    minimum: PositiveInt
    maximum: PositiveInt

    @validator("maximum", allow_reuse=True)
    def assert_min_not_larger_than_max(cls, maximum: PositiveInt, values: Dict[str, PositiveInt]) -> PositiveInt:
        if (minimum := values.get("minimum", False)) and minimum > maximum:
            raise ValueError(f"Maximum must be larger than minimum, was: minimum {minimum}, maximum {maximum}")
        return maximum

    def __contains__(self, other: SupportsInt) -> bool:
        return self.minimum <= int(other) <= self.maximum

    def __iter__(self) -> PositiveInt:
        yield self.minimum
        yield self.maximum
