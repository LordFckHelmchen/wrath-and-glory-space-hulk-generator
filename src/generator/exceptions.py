# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025 The Wrath & Glory Space Hulk Generator contributors



class SpaceHulkGeneratorError(Exception):
    pass


class EventCountOutOfRangeError(SpaceHulkGeneratorError, ValueError):
    """Raise when an event count list is passed with too few or too many items."""


class EventTypeError(SpaceHulkGeneratorError, TypeError):
    """Raise when the wrong type of container or container element is passed to set events."""
