from typing import List
from typing import Tuple

from pydantic import BaseModel
from pydantic import NonNegativeInt

from .random_table_event_collection import RandomTableEventCollection


class SpaceHulk(BaseModel):
    origins: RandomTableEventCollection
    occupations: RandomTableEventCollection
    purposes: RandomTableEventCollection
    rooms: RandomTableEventCollection
    hazards: RandomTableEventCollection

    @property
    def number_of_origins(self) -> NonNegativeInt:
        return len(self.origins)

    @property
    def number_of_rooms(self) -> NonNegativeInt:
        return len(self.rooms)

    def __iter__(self) -> Tuple[str, RandomTableEventCollection]:
        for field in self.__fields__:
            yield field, getattr(self, field)

    def __getitem__(self, table_name: str) -> RandomTableEventCollection:
        return getattr(self, table_name)

    def __setitem__(self, table_name: str, value: RandomTableEventCollection) -> None:
        setattr(self, table_name, value)

    def get_event_names(self, table_name: str) -> List[str]:
        return [event.name for event in self[table_name]]
