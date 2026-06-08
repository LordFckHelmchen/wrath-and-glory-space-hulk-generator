# SPDX-FileCopyrightText: Copyright (c) 2025 LordFckHelmchen
# SPDX-License-Identifier: GPL-3.0-or-later
import json
import logging
import random
import shutil
import subprocess  # noqa: S404  # Required for calling De Broglie executable
import uuid
from collections import Counter
from pathlib import Path

import img2pdf
from pydantic import NonNegativeInt

from src.generator.space_hulk import SpaceHulk
from src.layouter.i_create_layouts import ICreateLayouts
from src.layouter.i_layout import ILayout
from src.layouter.layout_file_type import LayoutFileType

from .exceptions import ContradictionError
from .exceptions import UnknownSubprocessCallError

DE_BROGLIE_EXECUTABLE = Path(__file__).parent / "DeBroglie_v2.0.0" / "bin" / "DeBroglie.Console"

DEFAULT_CONFIG_FILE = Path(__file__).parent / "tile_sets" / "space_hulk_game" / "default_tile_config.json"
DEFAULT_CONFIG = json.loads(DEFAULT_CONFIG_FILE.read_text(encoding="utf-8"))
TILE_PROBABILITIES = {
    tile["value"]: freq for tile in DEFAULT_CONFIG["tiles"] if (freq := tile.get("multiplyFrequency"))
}
TILES_DIR = Path(__file__).parent / "tile_sets" / "space_hulk_game" / "svg"
ROOMS_DIR = TILES_DIR / "rooms"
TILE_SUFFIX = ".svg"
ROOM_TILES = sorted(file_or_dir.stem for file_or_dir in ROOMS_DIR.glob(f"*{TILE_SUFFIX}"))
assert set(ROOM_TILES) <= set(TILE_PROBABILITIES), (
    f"Some room tiles are missing probabilities!{set(ROOM_TILES) - set(TILE_PROBABILITIES)}"
)
ROOM_TILE_PROBABILITIES = {tile: TILE_PROBABILITIES[tile] for tile in ROOM_TILES if tile in TILE_PROBABILITIES}


class DeBroglieLayouter(ICreateLayouts):
    def __init__(self, number_of_retries: NonNegativeInt = 3) -> None:
        self.number_of_retries = number_of_retries

    @property
    def output_file(self) -> Path:
        base_dir = (DEFAULT_CONFIG_FILE.parent / DEFAULT_CONFIG.get("baseDirectory", ".")).expanduser().resolve()
        return (base_dir / DEFAULT_CONFIG["dest"]).expanduser().resolve()

    @property
    def contradiction_file(self) -> Path:
        return self.output_file.with_suffix(f".contradiction{self.output_file.suffix}")

    def _make_config(self, space_hulk: SpaceHulk) -> Path:
        """
        Creates a modified config from the default config.

        Parameters
        ----------
        space_hulk : SpaceHulk
            The space hulk with room data.

        Returns
        -------
        Path
            Path to the config file.
        """
        modified_config = DEFAULT_CONFIG.copy()

        # Get rooms to be added & group them by their counts to reduce number of constraints
        rooms_to_counts = Counter(
            random.choices(
                list(ROOM_TILE_PROBABILITIES),
                k=space_hulk.number_of_rooms,
                weights=list(ROOM_TILE_PROBABILITIES.values()),
            )
        )
        counts_to_rooms = {}
        for room, count in rooms_to_counts.items():
            counts_to_rooms.setdefault(count, []).append(room)

        # Set count constraint for each group of rooms with the same count and assure that there are no other room
        # tiles, by constraining omitted rooms to 0
        room_count_constraints = []
        room_count_constraints.extend([
            {"type": "count", "comparison": "Exactly", "count": count, "tiles": sorted(counts_to_rooms[count])}
            for count in sorted(counts_to_rooms)
        ])

        if any(omitted_rooms := sorted(set(ROOM_TILES) - set(rooms_to_counts))):
            modified_config["tiles"] = [tile for tile in modified_config["tiles"] if tile["value"] not in omitted_rooms]

        modified_config.setdefault("constraints", []).extend(room_count_constraints)

        # Write to temporary file
        with self.output_file.with_stem("tile_config").open("w", encoding="utf-8") as fp:
            json.dump(modified_config, fp, indent=2)
            return Path(fp.name)

    def create_layout(self, space_hulk: SpaceHulk) -> ILayout:
        """
        Creates a new output file based on the wave-function collapse algorithm.

        The layout now respects the number of rooms in the space hulk by adding
        count constraints for room tiles.

        Parameters
        ----------
        space_hulk : SpaceHulk
            The space hulk with room data.

        Returns
        -------
        ILayout
            The created layout.

        Raises
        ------
        ContradictionError
            If the layouter cannot resolve the given tile-configuration.
        UnknownSubprocessCallError
            If the call to the De Broglie subprocess fails.
        """
        # Create modified config with room constraints
        config_file = self._make_config(space_hulk)

        # Make sure that no existing output file is present
        if self.output_file.is_file():
            msg = f"Deleting existing De Broglie output file '{self.output_file}'"
            logging.getLogger(__name__).warning(msg)
            self.output_file.unlink()

        try:
            for retry_id in range(self.number_of_retries):
                # Clear existing contraction file
                self.contradiction_file.unlink(missing_ok=True)

                # Run DeBroglie with the modified config
                subprocess.run([DE_BROGLIE_EXECUTABLE, config_file], check=False)  # noqa: S603  # TODO(djm): https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/issues/28
                if self.output_file.is_file():
                    # Create CSV representation and return wrapper with room mapping
                    return DeBroglieLayoutWrapper(self.output_file)

                logging.getLogger(__name__).info(f"Failed resolving constraints, retrying ({retry_id + 1})...")

        finally:
            # Clean up temporary config
            # temp_config_path.unlink(missing_ok=True)
            pass

        if self.contradiction_file.is_file():
            raise ContradictionError

        raise UnknownSubprocessCallError


class DeBroglieLayoutWrapper(ILayout):
    def __init__(self, output_file: Path) -> None:
        if not output_file.exists():
            msg = "De Broglie output file not found"
            raise FileNotFoundError(msg)
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
