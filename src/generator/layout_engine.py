from enum import Enum
from typing import Union

from pydantic import NonNegativeInt

from src.generator.exceptions import InvalidLayoutEngineError


class LayoutEngine(Enum):
    CIRCO = "circo"
    FDP = "fdp"
    OSAGE = "osage"

    @classmethod
    def is_parsable_to_member(cls, value: Union[str, "LayoutEngine"]) -> bool:
        return isinstance(value, cls) \
               or isinstance(value, str) and any(value in [member.name, member.value] for member in cls)

    @classmethod
    def index(cls, member: Union[str, "LayoutEngine"]) -> NonNegativeInt:
        if not cls.is_parsable_to_member(member):
            raise InvalidLayoutEngineError(
                f"'{member}' of type {type(member)} cannot be interpreted as {cls.__name__}.")

        if isinstance(member, str):  # member.name or member.value
            try:
                member = cls(member)
            except ValueError:
                member = getattr(cls, member)

        return list(cls).index(member)
