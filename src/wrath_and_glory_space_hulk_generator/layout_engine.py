from enum import Enum
from typing import Union

from pydantic import NonNegativeInt


class LayoutEngine(Enum):
    CIRCO = "circo"
    FDP = "fdp"
    OSAGE = "osage"

    @classmethod
    def index(cls, member: Union[str, "LayoutEngine"]) -> NonNegativeInt:
        if isinstance(member, str):
            try:
                member = LayoutEngine(member)
            except ValueError:
                member = getattr(LayoutEngine, member)
        return list(cls).index(LayoutEngine(member))
