# SPDX-FileCopyrightText: Copyright (c) 2025 LordFckHelmchen
# SPDX-License-Identifier: GPL-3.0-or-later

import csv
import hashlib
import unittest
from pathlib import Path

from src.layouter.de_broglie_layouter import ROOM_TILES
from src.layouter.de_broglie_layouter import DeBroglieLayouter
from src.layouter.layout_file_type import LayoutFileType
from tests.assets.helpers import create_clean_test_folder
from tests.assets.helpers import load_space_hulk


class TestDeBroglieLayouter(unittest.TestCase):
    output_folder = create_clean_test_folder("generated_de_broglie_layouts")
    space_hulk = load_space_hulk()

    @staticmethod
    def get_file_hash(file_name: Path) -> str:
        return hashlib.md5(file_name.read_bytes()).hexdigest()  # noqa: S324  # We only use it to compare the contents

    def setUp(self) -> None:
        self.layouter = DeBroglieLayouter()

        # Make sure that the file does not exist
        self.layouter.output_file.unlink(missing_ok=True)

        self.output_file_hash = None

    def assert_nonempty_file_exists(self, file_name: Path) -> None:
        msg = f"'{file_name}' is not a valid file!"
        assert file_name.is_file(), msg

        msg = f"'{file_name}' was empty!"
        assert file_name.stat().st_size > 0, msg

    def assert_output_file_unchanged(self) -> None:
        new_output_file_hash = self.get_file_hash(self.layouter.output_file)
        msg = f"Content of output file '{self.layouter.output_file}' has changed!"
        assert self.output_file_hash == new_output_file_hash, msg

    def test_create_layout_expect_output_file_created(self) -> None:
        # Assert that the file did not exist before.
        assert not self.layouter.output_file.exists()

        _ = self.layouter.create_layout(self.space_hulk)
        self.assert_nonempty_file_exists(self.layouter.output_file)

    def test_render_to_file_expect_output_file_exists_unchanged_and_target_file_created(self) -> None:
        for file_type in LayoutFileType:
            with self.subTest(i=file_type):
                # ARRANGE
                target_file = self.output_folder / f"de_broglie_layout.{file_type.value}"
                layout = self.layouter.create_layout(self.space_hulk)
                expected_output_file_hash = self.get_file_hash(self.layouter.output_file)

                # ACT
                layout.render_to_file(target_file)
                actual_output_file_hash = self.get_file_hash(self.layouter.output_file)

                # ASSERT
                msg = f"Content of output file '{self.layouter.output_file}' has changed!"
                assert expected_output_file_hash == actual_output_file_hash, msg
                self.assert_nonempty_file_exists(target_file)

    def test_create_layout_expect_csv_file_created(self) -> None:
        # ACT
        _ = self.layouter.create_layout(self.space_hulk)
        csv_file = self.layouter.output_file.with_suffix(".csv")

        # ASSERT
        self.assert_nonempty_file_exists(csv_file)

    def test_create_layout_expect_csv_contains_all_rooms(self) -> None:
        # ACT
        _ = self.layouter.create_layout(self.space_hulk)
        csv_file = self.layouter.output_file.with_suffix(".csv")

        # Read CSV and check rooms
        with csv_file.open("r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # ASSERT
        assert len(rows) == self.space_hulk.number_of_rooms, (
            f"Expected {self.space_hulk.number_of_rooms} rooms in CSV, got {len(rows)}"
        )

        # Check that all room names are present
        room_names_in_csv = [row["Room Name"] for row in rows]
        room_names_in_hulk = [room.name for room in self.space_hulk.rooms]
        assert room_names_in_csv == room_names_in_hulk, "Room names in CSV don't match room names in space hulk"

    def test_create_layout_expect_csv_maps_rooms_to_room_tiles(self) -> None:
        # ACT
        _ = self.layouter.create_layout(self.space_hulk)
        csv_file = self.layouter.output_file.with_suffix(".csv")

        # Read CSV and check tile assignments
        with csv_file.open("r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # ASSERT
        for row in rows:
            tile_type = row["Assigned Tile Type"]
            assert tile_type in ROOM_TILES, f"Tile type '{tile_type}' is not a valid room tile"

    def test_render_to_file_png_expect_csv_copied(self) -> None:
        # ARRANGE
        target_file = self.output_folder / "de_broglie_layout_with_csv.png"
        layout = self.layouter.create_layout(self.space_hulk)

        # ACT
        layout.render_to_file(target_file)

        # ASSERT
        csv_file = target_file.with_suffix(".csv")
        self.assert_nonempty_file_exists(csv_file)
