class SpaceHulkGeneratorError(Exception):
    pass


class EventCountOutOfRangeError(SpaceHulkGeneratorError, ValueError):
    """Raise when an event count list is passed with too few or too many items."""


class EventTypeError(SpaceHulkGeneratorError, TypeError):
    """Raise when the wrong type of container or container element is passed to set events."""


class ValueNotParsableToEnumMember(SpaceHulkGeneratorError, TypeError):
    """Raise when a given value cannot be parsed into an IndexableEnum member."""
