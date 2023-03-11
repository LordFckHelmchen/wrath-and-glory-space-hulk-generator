from enum import Enum

from pydantic import NonNegativeInt


class IndexableEnum(Enum):
    @property
    def index(self) -> NonNegativeInt:
        """
        Retrieve the index aka position of the enum member in the Enum.

        This is implements the same functionality as list.index.
        :return: The index within the enum at which the member occurs
        """
        return list(type(self)).index(self)


class LayoutEngine(IndexableEnum):
    CIRCO = "circo"
    FDP = "fdp"
    OSAGE = "osage"


class LayoutEdgeType(IndexableEnum):
    LINE = "line"
    ORTHO = "ortho"
    SPLINES = "spline"


class LayoutFormat(IndexableEnum):
    DOT = "dot"
    PDF = "pdf"
    PNG = "png"
    SVG = "svg"
