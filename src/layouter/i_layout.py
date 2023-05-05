from abc import abstractmethod
from pathlib import Path

from .layout_file_type import LayoutFileType


class ILayout:
    @abstractmethod
    def render_to_file(self, file_name: Path, file_type: LayoutFileType) -> None:
        """
        Create a file of the layout

        Parameters
        ----------

        file_name
            Full name of the file to render to. Extensions will be overwritten by the given file type
        file_type
            Type of the output file
        """
