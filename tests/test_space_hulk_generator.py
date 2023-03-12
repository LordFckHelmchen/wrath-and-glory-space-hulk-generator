import unittest
from pathlib import Path

from src.generator.space_hulk_generator import SpaceHulkGenerator


class TestSpaceHulkGenerator(unittest.TestCase):
    def test_create_hulk_expect_no_errors(self):
        generator = SpaceHulkGenerator(Path("src/generator/assets/"))
        _ = generator.create_hulk()


if __name__ == "__main__":
    unittest.main()
