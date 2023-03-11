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
