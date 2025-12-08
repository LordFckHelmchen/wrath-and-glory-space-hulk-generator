class SpaceHulkGeneratorError(Exception):
    pass


class EventCountOutOfRangeError(SpaceHulkGeneratorError, ValueError):
    """Raise when an event count list is passed with too few or too many items."""


class EventTypeError(SpaceHulkGeneratorError, TypeError):
    """Raise when the wrong type of container or container element is passed to set events."""


class DigitOutOfRangeOfDieError(SpaceHulkGeneratorError, ValueError):
    """Raise when a digit is out of the valid range for a die."""


class RangeNotSortedError(SpaceHulkGeneratorError, ValueError):
    """Raise when a range is not sorted in ascending order."""


class DimensionConstraintOfZeroSizeError(SpaceHulkGeneratorError, ValueError):
    """Raise when a dimension constraint has zero size (min == max)."""
