from abc import abstractmethod
from pathlib import Path


class ILayout:
    @abstractmethod
    def render_to_file(self, file_name: Path) -> None:
        """
        Create a file of the layout

        Parameters
        ----------

        file_name
            Full name of the file to render to. Extensions will be overwritten by the given file type
        """
