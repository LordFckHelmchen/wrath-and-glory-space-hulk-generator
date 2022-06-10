from enum import Enum
from typing import Union, Any

from pydantic import NonNegativeInt

from src.generator.exceptions import ValueNotParsableToEnumMember


class IndexableEnum(Enum):
    @classmethod
    def is_parsable_to_member(cls, value: Any) -> bool:
        return isinstance(value, str) and any(value in [member.name, member.value] for member in cls) \
               or isinstance(value, cls)

    @classmethod
    def index(cls, member: Union[str, "IndexableEnum"]) -> NonNegativeInt:
        if not cls.is_parsable_to_member(member):
            raise ValueNotParsableToEnumMember(f"'{member}' of type {type(member)} "
                                               f"cannot be interpreted as {cls.__name__}.")

        if isinstance(member, str):  # member.name or member.value
            try:
                member = cls(member)
            except ValueError:
                member = getattr(cls, member)

        return list(cls).index(member)


class LayoutEngine(IndexableEnum):
    CIRCO = "circo"
    FDP = "fdp"
    OSAGE = "osage"


class LayoutEdgeType(IndexableEnum):
    LINE = "line"
    ORTHO = "ortho"
    SPLINES = "spline"

