from pathlib import Path
from typing import Generator
from typing import List
from typing import Tuple

from pydantic import BaseModel
from pydantic import NonNegativeInt
from pydantic import PositiveInt

from .random_table_event_collection import RandomTableEventCollection
from ..md2pdf.md2pdf import Markdown2PdfParser


class SpaceHulk(BaseModel):
    origins: RandomTableEventCollection
    occupations: RandomTableEventCollection
    purposes: RandomTableEventCollection
    hazards: RandomTableEventCollection
    rooms: RandomTableEventCollection
    name: str = ""
    description: str = ""

    @property
    def number_of_origins(self) -> NonNegativeInt:
        return len(self.origins)

    @property
    def number_of_rooms(self) -> NonNegativeInt:
        return len(self.rooms)

    def __iter__(self) -> Generator[Tuple[str, RandomTableEventCollection], None, None]:
        for field in self.__fields__:
            field_value = getattr(self, field)
            if isinstance(field_value, RandomTableEventCollection):
                yield field, getattr(self, field)

    def __getitem__(self, table_name: str) -> RandomTableEventCollection:
        return getattr(self, table_name)

    def __setitem__(self, table_name: str, value: RandomTableEventCollection) -> None:
        setattr(self, table_name, value)

    def get_event_names(self, table_name: str) -> List[str]:
        return [event.name for event in self[table_name]]

    def as_markdown(self, header_level: PositiveInt = 1) -> str:
        self_as_string = [
            f"{'#' * header_level} Space Hulk{f' _{self.name}_' if self.name else ''}\n",
            f"{'#' * (header_level + 1)} Description\n",
        ]

        if self.description:
            self_as_string.append(f"{self.description}\n")

        header_level += 2
        for event_table_name, event_collection in self:
            self_as_string.append(
                event_collection.as_markdown(header=event_table_name.capitalize(), header_level=header_level)
            )

        return "\n".join(self_as_string)

    def render_pdf(self, file_name: Path) -> None:
        Markdown2PdfParser().parse(self.as_markdown()).output(name=str(file_name))
