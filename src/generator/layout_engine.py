from enum import Enum
from typing import Union

from pydantic import NonNegativeInt

from src.generator.exceptions import InvalidLayoutEngineError


class LayoutEngine(Enum):
    CIRCO = "circo"
    FDP = "fdp"
    OSAGE = "osage"

    @classmethod
    def is_parsable_to_layout_engine(cls, value: Union[str, "LayoutEngine"]) -> bool:
        return isinstance(value, LayoutEngine) \
               or isinstance(value, str) and any(value in [member.name, member.value] for member in LayoutEngine)

    @classmethod
    def index(cls, member: Union[str, "LayoutEngine"]) -> NonNegativeInt:
        if not cls.is_parsable_to_layout_engine(member):
            raise InvalidLayoutEngineError(
                f"'{member}' of type {type(member)} cannot be interpreted as {cls.__name__}.")

        if isinstance(member, str):  # member.name or member.value
            try:
                member = LayoutEngine(member)
            except ValueError:
                member = getattr(LayoutEngine, member)

        return list(cls).index(member)
