# SPDX-FileCopyrightText: Copyright (c) 2025 LordFckHelmchen
# SPDX-License-Identifier: GPL-3.0-or-later

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
