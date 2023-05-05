from abc import ABC
from abc import abstractmethod
from pathlib import Path

from src.generator.space_hulk import SpaceHulk


class ILayout:
    @abstractmethod
    def render_pdf(self, file_name: Path) -> None:
        """Create a PDF of the layout"""


class ICreateLayouts(ABC):
    @abstractmethod
    def create_layout(self, space_hulk: SpaceHulk) -> ILayout:
        pass
