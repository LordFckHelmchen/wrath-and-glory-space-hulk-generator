import logging
from dataclasses import fields
from pathlib import Path
from typing import ClassVar

from pydantic import ConstrainedInt
from pydantic import PositiveInt
from pydantic import conint

from .random_table import RandomTable
from .random_table_event import RandomTableEventInfoList
from .random_table_event_collection import RandomTableEventCollection
from .space_hulk import SpaceHulk
from .space_hulk_tables import SpaceHulkTables


class RoomCount(ConstrainedInt):
    ge = 3
    le = 100
    strict = False

    @classmethod
    def from_int(cls, i: int) -> "RoomCount":
        if i < cls.ge:
            i = cls.ge
        elif i > cls.le:
            i = cls.le
        return cls(i)


class SpaceHulkGenerator:
    _default_table_folder: ClassVar[Path] = Path(__file__).parent / "assets"
    _mixed_origin_event_string: ClassVar[str] = "Mixed Origin"
    _minimum_number_of_origins_for_mixed_origin_event: ClassVar[conint(gt=1, lt=5)] = 2

    def __init__(
        self, table_folder: Path = _default_table_folder, table_name_glob_pattern: str = "table_*.json"
    ) -> None:
        tables = {}
        for table in fields(SpaceHulkTables):
            table_file = table_folder / table_name_glob_pattern.replace("*", table.name)
            tables[table.name] = RandomTable.parse_file(table_file)

        self._tables = SpaceHulkTables(**tables)

    def create_hulk(self, number_of_rooms_per_origin: PositiveInt = 10) -> SpaceHulk:
        if number_of_rooms_per_origin not in self._tables.rooms.event_count_constraint:
            logging.warning(
                f"Number of room out of range {self._tables.rooms.event_count_constraint}: "
                f"Was {number_of_rooms_per_origin}"
            )
        origins = self._create_origin()
        number_of_origins = len(origins)

        # Account for mixed origins
        number_of_rooms = RoomCount.from_int(number_of_origins * number_of_rooms_per_origin)

        return SpaceHulk(
            origins=origins,
            occupations=self._tables.occupations.generate_events(number_of_events=number_of_origins),
            purposes=self._tables.purposes.generate_events(number_of_events=number_of_origins),
            rooms=self._tables.rooms.generate_events(number_of_events=number_of_rooms),
            hazards=self._tables.hazards.generate_events(number_of_events=number_of_origins),
        )

    def _is_mixed_origin(self, origin: str) -> bool:
        return origin.casefold() == self._mixed_origin_event_string.casefold()

    def _create_origin(self) -> RandomTableEventCollection:
        origin = self._tables.origins.generate_single_event()
        origins = {origin.name: origin}
        while self._mixed_origin_event_string in origins:
            origins.pop(self._mixed_origin_event_string)
            origins |= {
                origin.name: origin
                for origin in self._tables.origins.generate_events(
                    number_of_events=self._minimum_number_of_origins_for_mixed_origin_event
                ).events
            }
        return RandomTableEventCollection(
            events=list(origins.values()), event_count_constraint=self._tables.origins.event_count_constraint
        )

    def get_table_events(self, table_name: str) -> RandomTableEventInfoList:
        events = getattr(self._tables, table_name).events

        if table_name == "origins":
            events = [event for event in events if event.name != self._mixed_origin_event_string]

        return events  # noqa: RET504 - not an unnecessary assignment ^^
