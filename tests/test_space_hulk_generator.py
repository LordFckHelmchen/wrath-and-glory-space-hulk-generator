# SPDX-FileCopyrightText: Copyright (c) 2025 LordFckHelmchen
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from pathlib import Path

from src.generator.space_hulk_generator import SpaceHulkGenerator


class TestSpaceHulkGenerator(unittest.TestCase):
    def test_create_hulk_expect_no_errors(self) -> None:
        generator = SpaceHulkGenerator(Path("src/generator/assets/"))
        _ = generator.create_hulk()


if __name__ == "__main__":
    unittest.main()
