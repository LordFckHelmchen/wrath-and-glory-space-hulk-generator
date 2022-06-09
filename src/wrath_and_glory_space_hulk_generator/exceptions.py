class SpaceHulkGeneratorError(Exception):
    pass


class EventCountOutOfRangeError(SpaceHulkGeneratorError, ValueError):
    """Raise when an event count list is passed with too few or too many items."""


class EventTypeError(SpaceHulkGeneratorError, TypeError):
    """Raise when the wrong type of container or container element is passed to set events."""


class InvalidLayoutEngineError(SpaceHulkGeneratorError, TypeError):
    """Raise when the given layout engine could not be interpreted as LayoutEngine."""
