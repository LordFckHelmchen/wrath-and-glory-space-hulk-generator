# SPDX-FileCopyrightText: Copyright (c) 2025 LordFckHelmchen
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

from .random_table import RandomTable


@dataclass
class SpaceHulkTables:
    origins: RandomTable
    occupations: RandomTable
    purposes: RandomTable
    rooms: RandomTable
    hazards: RandomTable

    def __getitem__(self, item: str) -> RandomTable:
        return getattr(self, item)
