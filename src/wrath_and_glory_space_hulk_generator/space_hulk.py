from typing import List, Union, Tuple

from pydantic import BaseModel
from pydantic import NonNegativeInt

from .exceptions import EventTypeError
from .random_table_event_list import RandomTableEventList, SizedRandomTableEventList

AnyRandomTableEventList = Union[RandomTableEventList, SizedRandomTableEventList]


class SpaceHulk(BaseModel):
    origins: RandomTableEventList
    occupations: RandomTableEventList
    purposes: RandomTableEventList
    rooms: SizedRandomTableEventList
    hazards: RandomTableEventList

    @property
    def number_of_origins(self) -> NonNegativeInt:
        return len(self.origins)

    @property
    def number_of_rooms(self) -> NonNegativeInt:
        return len(self.rooms)

    def __iter__(self) -> Tuple[str, AnyRandomTableEventList]:
        for field in self.__fields__:
            yield field, getattr(self, field)

    def __getitem__(self, table_name: str) -> AnyRandomTableEventList:
        return getattr(self, table_name)

    def __setitem__(self, table_name: str, value: AnyRandomTableEventList) -> None:
        setattr(self, table_name, value)

    def __setattr__(self, table_name: str, value: AnyRandomTableEventList) -> None:
        if self.is_valid_event_list_for_table(table_name, event_list=value):
            expected_type = self.__annotations__[table_name]
            observed_type = value.__annotations__ if hasattr(value, "__annotations__") else value.__class__.__name__
            raise EventTypeError(f"Invalid type for '{self.__class__.__name__}.{table_name}'. "
                                 f"Expected '{expected_type}', got '{observed_type}'")
        object.__setattr__(self, table_name, value)

    def is_valid_event_list_for_table(self, table_name: str, event_list: AnyRandomTableEventList) -> bool:
        # Check the container type (e.g. List for List[X]). Use getitem to throw AttributeError on invalid table_name.
        if not isinstance(event_list, type(self[table_name])):
            return False

        # Check the container content type
        allowed_event_types = self.__annotations__[table_name].__args__
        return all(type(e) in allowed_event_types for e in event_list)

    def get_event_names(self, table_name: str) -> List[str]:
        return [event.name for event in self[table_name]]
