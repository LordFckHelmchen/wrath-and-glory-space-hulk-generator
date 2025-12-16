# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025 The Wrath & Glory Space Hulk Generator contributors

import unittest
from pathlib import Path

from src.generator.space_hulk_generator import SpaceHulkGenerator


class TestSpaceHulkGenerator(unittest.TestCase):
    def test_create_hulk_expect_no_errors(self) -> None:
        generator = SpaceHulkGenerator(Path("src/generator/assets/"))
        _ = generator.create_hulk()


if __name__ == "__main__":
    unittest.main()
