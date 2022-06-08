import logging
from enum import Enum
from typing import Union

from pydantic import NonNegativeInt


class LayoutEngine(Enum):
    CIRCO = "circo"
    FDP = "fdp"
    OSAGE = "osage"

    @classmethod
    def index(cls, member: Union[str, "LayoutEngine"]) -> NonNegativeInt:
        # TODO: Remove debug code after proving that this function works properly and its a streamlit issue
        input_arg = member
        if isinstance(member, str):  # member.name or member.value
            try:
                member = LayoutEngine(member)
            except ValueError:
                member = getattr(LayoutEngine, member)

        try:
            index = list(cls).index(LayoutEngine(member))
        except ValueError as err:
            logging.error(f"{err}: 'member' was '{input_arg}' (type '{type(input_arg)}', "
                          f"index input was '{member}' (type {type(member)}'")
            raise err

        return index
