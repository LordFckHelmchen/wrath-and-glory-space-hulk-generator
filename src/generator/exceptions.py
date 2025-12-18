# SPDX-FileCopyrightText: Copyright (c) 2025 LordFckHelmchen
# SPDX-License-Identifier: GPL-3.0-or-later


class SpaceHulkGeneratorError(Exception):
    pass


class EventCountOutOfRangeError(SpaceHulkGeneratorError, ValueError):
    """Raise when an event count list is passed with too few or too many items."""


class EventTypeError(SpaceHulkGeneratorError, TypeError):
    """Raise when the wrong type of container or container element is passed to set events."""
