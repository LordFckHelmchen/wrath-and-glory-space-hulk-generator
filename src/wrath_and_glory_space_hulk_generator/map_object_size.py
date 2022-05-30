from enum import Enum
from typing import Optional, Dict

from pydantic import BaseModel, validator, PositiveInt, ConstrainedInt

from .positive_int_range import PositiveIntRange


class MapObjectSizeInt(ConstrainedInt):
    ge = 1
    le = 500


class MapObjectDimensionConstraint(PositiveIntRange):
    minimum: MapObjectSizeInt
    maximum: MapObjectSizeInt

    @validator("maximum", allow_reuse=True)
    def assert_min_not_equal_to_max(cls, maximum: PositiveInt, values: Dict[str, PositiveInt]) -> PositiveInt:
        if (minimum := values.get("minimum", False)) and minimum == maximum:
            raise ValueError(f"Minimum & maximum must not be equal, was: minimum {minimum} == maximum {maximum}")
        return maximum


class UnitOfMeasurement(Enum):
    METER = "m"


class MapObjectSizeConstraint(BaseModel):
    x: MapObjectDimensionConstraint
    y: Optional[MapObjectDimensionConstraint]
    unit: UnitOfMeasurement = UnitOfMeasurement.METER

    @validator("y", allow_reuse=True, always=True)
    def copy_x_limits_if_y_limits_are_unassigned(cls, y: MapObjectDimensionConstraint,
                                                 values) -> MapObjectDimensionConstraint:
        return values["x"] if y is None else y


GlobalMapObjectSizeConstraint = MapObjectSizeConstraint(
    x=MapObjectDimensionConstraint(minimum=MapObjectSizeInt(MapObjectSizeInt.ge),
                                   maximum=MapObjectSizeInt(MapObjectSizeInt.le)))


class MapObjectSize(BaseModel):
    x: MapObjectSizeInt = MapObjectSizeInt.ge
    y: MapObjectSizeInt = MapObjectSizeInt.ge
    unit: UnitOfMeasurement = UnitOfMeasurement.METER

    @validator("y", allow_reuse=True, always=True)
    def copy_x_dimension_if_y_is_unassigned(cls, y: MapObjectSizeInt, values) -> MapObjectSizeInt:
        return values["x"] if y is None else y

    @property
    def area(self) -> PositiveInt:
        return self.x * self.y