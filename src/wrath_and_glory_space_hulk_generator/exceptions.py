class SpaceHulkGeneratorError(Exception):
    pass


class EventCountOutOfRangeError(SpaceHulkGeneratorError, ValueError):
    """Raise when an event count list is passed with too few or too many items."""


class EventTypeError(SpaceHulkGeneratorError, TypeError):
    """Raise when the wrong type of container or container element is passed to set events."""


class InvalidTableEventError(SpaceHulkGeneratorError, ValueError):
    """Raise when an event is attempted to be set but the event is not in the event info of the according table."""


class EventListLengthError(SpaceHulkGeneratorError, ValueError):
    """Raise when a list of events is out-of-bounds of the according table."""
