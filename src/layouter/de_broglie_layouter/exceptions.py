# SPDX-FileCopyrightText: Copyright (c) 2025 LordFckHelmchen
# SPDX-License-Identifier: GPL-3.0-or-later


class DeBroglieLayouterError(Exception):
    pass


class ContradictionError(DeBroglieLayouterError, RuntimeError):
    """Raise when the layouter cannot resolve the given tile-configuration."""

    def __init__(self) -> None:
        super().__init__("Contradiction encountered - couldn't resolve constraints")


class UnknownSubprocessCallError(DeBroglieLayouterError, RuntimeError):
    """Raise when the call to the De Broglie subprocess fails."""

    def __init__(self) -> None:
        super().__init__("Unknown error occurred during De Broglie subprocess call")
