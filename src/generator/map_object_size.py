import logging
from enum import Enum
from random import randint
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import ConstrainedInt
from pydantic import PositiveInt
from pydantic import validator

from .positive_int_range import PositiveIntRange


class MapObjectSizeInt(ConstrainedInt):
    ge = 1
    le = 500


class MapObjectDimensionConstraint(PositiveIntRange):
    minimum: MapObjectSizeInt
    maximum: MapObjectSizeInt

    @validator("maximum", allow_reuse=True)
    def assert_min_not_equal_to_max(cls, maximum: PositiveInt, values: dict[str, PositiveInt]) -> PositiveInt:
        if (minimum := values.get("minimum", False)) and minimum == maximum:
            msg = f"Minimum & maximum must not be equal, was: minimum {minimum} == maximum {maximum}"
            raise ValueError(msg)
        return maximum

    def get_random_value(self) -> "MapObjectSizeInt":
        return MapObjectSizeInt(randint(self.minimum, self.maximum))


class UnitOfMeasurement(Enum):
    METER = "m"


class MapObjectSize(BaseModel):
    x: MapObjectSizeInt = MapObjectSizeInt.ge
    y: MapObjectSizeInt = MapObjectSizeInt.ge
    unit: UnitOfMeasurement = UnitOfMeasurement.METER

    @validator("y", allow_reuse=True, always=True)
    def copy_x_dimension_if_y_is_unassigned(
        cls, y: MapObjectSizeInt, values: dict[str, MapObjectSizeInt]
    ) -> MapObjectSizeInt:
        return values["x"] if y is None else y

    @property
    def area(self) -> PositiveInt:
        return self.x * self.y

    def __setitem__(self, key: str, value: Union[MapObjectSizeInt, UnitOfMeasurement]) -> None:
        if (
            key in ["x", "y"]
            and not isinstance(value, MapObjectSizeInt)
            or key == "unit"
            and not isinstance(value, UnitOfMeasurement)
        ):
            msg = f"Unsupported type '{type(value)}' for attribute '{key}'"
            raise TypeError(msg)

        setattr(self, key, value)

    def __getitem__(self, item: str) -> Union[MapObjectSizeInt, UnitOfMeasurement]:
        return getattr(self, item)

    def __lt__(self, other: "MapObjectSize") -> bool:
        if not isinstance(other, type(self)):
            msg = f"Unsupported type '{type(other)}'"
            raise TypeError(msg)
        if self.unit != other.unit:
            logging.warning("Unit conversion between size objects isn't supported yet!")
            return NotImplemented
        return self.area < other.area


class MapObjectSizeConstraint(BaseModel):
    x: MapObjectDimensionConstraint
    y: Optional[MapObjectDimensionConstraint]
    unit: UnitOfMeasurement = UnitOfMeasurement.METER

    def get_random_size(self) -> MapObjectSize:
        return MapObjectSize(x=self.x.get_random_value(), y=self.y.get_random_value())

    @validator("y", allow_reuse=True, always=True)
    def copy_x_limits_if_y_limits_are_unassigned(
        cls, y: MapObjectDimensionConstraint, values: dict[str, MapObjectDimensionConstraint]
    ) -> MapObjectDimensionConstraint:
        return values["x"] if y is None else y

    def __setitem__(self, key: str, value: Union[MapObjectDimensionConstraint, UnitOfMeasurement]) -> None:
        if (
            key in ["x", "y"]
            and not isinstance(value, MapObjectDimensionConstraint)
            or key == "unit"
            and not isinstance(value, UnitOfMeasurement)
        ):
            msg = f"Unsupported type '{type(value)}' for attribute '{key}'"
            raise TypeError(msg)

        setattr(self, key, value)

    def __getitem__(self, item: str) -> Union[MapObjectDimensionConstraint, UnitOfMeasurement]:
        return getattr(self, item)


GlobalMapObjectSizeConstraint = MapObjectSizeConstraint(
    x=MapObjectDimensionConstraint(
        minimum=MapObjectSizeInt(MapObjectSizeInt.ge), maximum=MapObjectSizeInt(MapObjectSizeInt.le)
    )
)
