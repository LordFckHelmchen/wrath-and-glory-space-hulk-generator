from __future__ import annotations

import logging
from enum import Enum
from random import randint
from typing import Annotated

from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveInt
from pydantic import ValidationInfo
from pydantic import field_validator

from .positive_int_range import PositiveIntRange

MAP_OBJECT_SIZE_INT_MIN = 1
MAP_OBJECT_SIZE_INT_MAX = 500

MapObjectSizeInt = Annotated[int, Field(ge=MAP_OBJECT_SIZE_INT_MIN, le=MAP_OBJECT_SIZE_INT_MAX)]


class MapObjectDimensionConstraint(PositiveIntRange):
    minimum: MapObjectSizeInt
    maximum: MapObjectSizeInt

    @field_validator("maximum")
    @classmethod
    def assert_min_not_equal_to_max(cls, maximum: PositiveInt, info: ValidationInfo) -> PositiveInt:
        if (minimum := info.data.get("minimum", False)) and minimum == maximum:
            msg = f"Minimum & maximum must not be equal, was: minimum {minimum} == maximum {maximum}"
            raise ValueError(msg)
        return maximum

    def get_random_value(self) -> MapObjectSizeInt:
        return MapObjectSizeInt(randint(self.minimum, self.maximum))


class UnitOfMeasurement(Enum):
    METER = "m"


class MapObjectSize(BaseModel):
    # Default to min. sized map object
    x: MapObjectSizeInt = MAP_OBJECT_SIZE_INT_MIN
    y: MapObjectSizeInt = MAP_OBJECT_SIZE_INT_MIN
    unit: UnitOfMeasurement = UnitOfMeasurement.METER

    @field_validator("y")
    @classmethod
    def copy_x_dimension_if_y_is_unassigned(cls, y: MapObjectSizeInt, info: ValidationInfo) -> MapObjectSizeInt:
        return y or info.data["x"]

    @property
    def area(self) -> PositiveInt:
        return self.x * self.y

    def __setitem__(self, key: str, value: MapObjectSizeInt | UnitOfMeasurement) -> None:
        if (key in {"x", "y"} and not isinstance(value, MapObjectSizeInt)) or (
            key == "unit" and not isinstance(value, UnitOfMeasurement)
        ):
            msg = f"Unsupported type '{type(value)}' for attribute '{key}'"
            raise TypeError(msg)

        setattr(self, key, value)

    def __getitem__(self, item: str) -> MapObjectSizeInt | UnitOfMeasurement:
        return getattr(self, item)

    def __lt__(self, other: MapObjectSize) -> bool:
        if not isinstance(other, type(self)):
            msg = f"Unsupported type '{type(other)}'"
            raise TypeError(msg)
        if self.unit != other.unit:
            logging.getLogger(__name__).warning("Unit conversion between size objects isn't supported yet!")
            return NotImplemented
        return self.area < other.area


class MapObjectSizeConstraint(BaseModel):
    x: MapObjectDimensionConstraint
    y: MapObjectDimensionConstraint | None = None
    unit: UnitOfMeasurement = UnitOfMeasurement.METER

    def get_random_size(self) -> MapObjectSize:
        return MapObjectSize(x=self.x.get_random_value(), y=self.y.get_random_value())

    @field_validator("y")
    @classmethod
    def copy_x_limits_if_y_limits_are_unassigned(
        cls, y: MapObjectDimensionConstraint | None, info: ValidationInfo
    ) -> MapObjectDimensionConstraint:
        return y or info.data["x"]

    def __setitem__(self, key: str, value: MapObjectDimensionConstraint | UnitOfMeasurement) -> None:
        if (key in {"x", "y"} and not isinstance(value, MapObjectDimensionConstraint)) or (
            key == "unit" and not isinstance(value, UnitOfMeasurement)
        ):
            msg = f"Unsupported type '{type(value)}' for attribute '{key}'"
            raise TypeError(msg)

        setattr(self, key, value)

    def __getitem__(self, item: str) -> MapObjectDimensionConstraint | UnitOfMeasurement:
        return getattr(self, item)


GlobalMapObjectSizeConstraint = MapObjectSizeConstraint(
    x=MapObjectDimensionConstraint(minimum=MAP_OBJECT_SIZE_INT_MIN, maximum=MAP_OBJECT_SIZE_INT_MAX)
)
