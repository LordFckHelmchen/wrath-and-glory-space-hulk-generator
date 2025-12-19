# SPDX-FileCopyrightText: Copyright (c) 2025 LordFckHelmchen
# SPDX-License-Identifier: GPL-3.0-or-later

import csv
import json
import shutil
import subprocess  # noqa: S404  # Required for calling De Broglie executable
import tempfile
import uuid
from pathlib import Path

import img2pdf

from src.generator.space_hulk import SpaceHulk
from src.layouter.i_create_layouts import ICreateLayouts
from src.layouter.i_layout import ILayout
from src.layouter.layout_file_type import LayoutFileType

DE_BROGLIE_EXECUTABLE = Path(__file__).parent / "DeBroglie_v2.0.0" / "bin" / "DeBroglie.Console"

DEFAULT_CONFIG_FILE = Path(__file__).parent / "tile_sets" / "space_hulk_game" / "tile_config.json"

# Tiles that contain rooms (extracted from tile_config.json)
ROOM_TILES = [
    "corridorCornered_with_roomSmallElongated_symF",
    "corridorCornered_with_roomSmall_symF",
    "corridorStraight_with_roomLarge_symI",
    "corridorStraight_with_room_symI",
    "corridorTurn_with_roomElongated_symL",
    "corridorTurn_with_roomSmall_symL",
    "corridorTurn_with_room_symL",
    "deadEnd_with_roomEnlongated_symT",
    "deadEnd_with_roomLargeWidening_symT",
    "deadEnd_with_roomSmall_symF",
    "intersection3way_with_roomSmall_symE",
    "intersection3way_with_room_symE",
    "intersection4wayAsym_with_roomLarge_symF",
    "intersection4wayAsym_with_roomSmall_symF",
    "intersection4way_with_room_symX",
]


class DeBroglieLayouter(ICreateLayouts):
    def __init__(self) -> None:
        self.config_file = DEFAULT_CONFIG_FILE
        with self.config_file.open("r") as f:
            self._config = json.load(f)

    @property
    def output_file(self) -> Path:
        base_dir = (self.config_file.parent / self._config.get("baseDirectory", ".")).expanduser().resolve()
        return (base_dir / self._config["dest"]).expanduser().resolve()

    def _create_modified_config(self, space_hulk: SpaceHulk) -> Path:
        """
        Creates a modified config with count constraints for room tiles.

        Parameters
        ----------
        space_hulk : SpaceHulk
            The space hulk with room data.

        Returns
        -------
        Path
            Path to the temporary modified config file.
        """
        modified_config = self._config.copy()

        # Add count constraint for room tiles
        number_of_rooms = space_hulk.number_of_rooms
        if number_of_rooms > 0:
            # Add or update count constraint for tiles with rooms
            room_count_constraint = {
                "type": "count",
                "comparison": "AtLeast",
                "count": min(number_of_rooms, len(ROOM_TILES)),  # Cap at available room tile types
                "tiles": ROOM_TILES,
            }

            # Add to constraints if not already present
            if "constraints" not in modified_config:
                modified_config["constraints"] = []

            # Remove any existing count constraint for room tiles
            modified_config["constraints"] = [
                c
                for c in modified_config["constraints"]
                if not (c.get("type") == "count" and any(t in ROOM_TILES for t in c.get("tiles", [])))
            ]

            modified_config["constraints"].append(room_count_constraint)

        # Write to temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, dir=self.config_file.parent, encoding="utf-8"
        ) as temp_config:
            json.dump(modified_config, temp_config, indent=2)
            return Path(temp_config.name)

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
        """
        # Create modified config with room constraints
        temp_config_path = self._create_modified_config(space_hulk)

        try:
            # Run DeBroglie with the modified config
            subprocess.run([DE_BROGLIE_EXECUTABLE, temp_config_path], check=False)  # noqa: S603  # TODO(djm): https://github.com/LordFckHelmchen/wrath-and-glory-space-hulk-generator/issues/28

            # Create CSV representation and return wrapper with room mapping
            return DeBroglieLayoutWrapper(self.output_file, space_hulk)
        finally:
            # Clean up temporary config
            temp_config_path.unlink(missing_ok=True)


class DeBroglieLayoutWrapper(ILayout):
    def __init__(self, output_file: Path, space_hulk: SpaceHulk | None = None) -> None:
        self._output_file = output_file
        self.space_hulk = space_hulk
        self.creation_id = uuid.uuid4()

        # Create CSV with room mapping if space hulk is provided
        if space_hulk is not None:
            self._csv_file = self._create_room_mapping_csv(space_hulk)
        else:
            self._csv_file = None

    def _create_room_mapping_csv(self, space_hulk: SpaceHulk) -> Path:
        """
        Creates a CSV file with room names mapped to potential tile locations.

        Parameters
        ----------
        space_hulk : SpaceHulk
            The space hulk with room data.

        Returns
        -------
        Path
            Path to the created CSV file.
        """
        csv_path = self._output_file.with_suffix(".csv")

        with csv_path.open("w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Room Number", "Room Name", "Room Description", "Assigned Tile Type"])

            # Write room information
            for i, room in enumerate(space_hulk.rooms, start=1):
                # Assign room to a room tile type in a round-robin fashion
                tile_type = ROOM_TILES[(i - 1) % len(ROOM_TILES)]
                writer.writerow([i, room.name, room.description or "", tile_type])

        return csv_path

    def render_to_file(self, file_name: Path) -> None:
        file_type = LayoutFileType(file_name.suffix[1:].casefold())  # Clip dot from suffix
        file_name.parent.mkdir(parents=True, exist_ok=True)  # Assert that the target directory exists
        if file_type == LayoutFileType.PNG:
            shutil.copyfile(self._output_file, file_name)
            # Also copy CSV if it exists
            if self._csv_file and self._csv_file.exists():
                csv_dest = file_name.with_suffix(".csv")
                shutil.copyfile(self._csv_file, csv_dest)
        elif file_type == LayoutFileType.PDF:
            with file_name.open("wb") as f:
                f.write(img2pdf.convert(str(self._output_file)))
