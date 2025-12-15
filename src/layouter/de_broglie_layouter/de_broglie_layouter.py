import json
import shutil
import subprocess  # noqa: S404  # Required for calling De Broglie executable
import uuid
from pathlib import Path

import img2pdf

from src.generator.space_hulk import SpaceHulk
from src.layouter.i_create_layouts import ICreateLayouts
from src.layouter.i_layout import ILayout
from src.layouter.layout_file_type import LayoutFileType

DE_BROGLIE_EXECUTABLE = Path(__file__).parent / "DeBroglie_v2.0.0" / "bin" / "DeBroglie.Console"

DEFAULT_CONFIG_FILE = Path(__file__).parent / "tile_sets" / "space_hulk_game" / "tile_config.json"


class DeBroglieLayouter(ICreateLayouts):
    def __init__(self) -> None:
        self.config_file = DEFAULT_CONFIG_FILE
        with self.config_file.open("r") as f:
            self._config = json.load(f)

    @property
    def output_file(self) -> Path:
        base_dir = (self.config_file.parent / self._config.get("baseDirectory", ".")).expanduser().resolve()
        return (base_dir / self._config["dest"]).expanduser().resolve()

    def create_layout(self, space_hulk: SpaceHulk) -> ILayout:  # noqa: ARG002
        """
        Creates a new output file based on the wave-function collapse algorithm

        Notes
        -----
        For now, the space_hulk is completely ignored.

        Returns
        -------
        ILayout
            The created layout.
        """
        subprocess.run([DE_BROGLIE_EXECUTABLE, self.config_file], check=False)  # noqa: S603  # TODO(djm): https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/issues/28
        return DeBroglieLayoutWrapper(self.output_file)  # This has potential issues with parallelism


class DeBroglieLayoutWrapper(ILayout):
    def __init__(self, output_file: Path) -> None:
        self._output_file = output_file
        self.creation_id = uuid.uuid4()

    def render_to_file(self, file_name: Path) -> None:
        file_type = LayoutFileType(file_name.suffix[1:].casefold())  # Clip dot from suffix
        file_name.parent.mkdir(parents=True, exist_ok=True)  # Assert that the target directory exists
        if file_type == LayoutFileType.PNG:
            shutil.copyfile(self._output_file, file_name)
        elif file_type == LayoutFileType.PDF:
            with file_name.open("wb") as f:
                f.write(img2pdf.convert(str(self._output_file)))
