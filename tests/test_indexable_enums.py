import unittest

from src.graphviz_layouter.indexable_enums import IndexableEnum


class TestIndexableEnum(unittest.TestCase):
    def test_get_index_expect_always_correct_index_returned(self) -> None:
        for indexable_enum_subclass in IndexableEnum.__subclasses__():
            for expected_index, member in enumerate(indexable_enum_subclass):
                self.assertEqual(expected_index, member.index)


if __name__ == "__main__":
    unittest.main()
