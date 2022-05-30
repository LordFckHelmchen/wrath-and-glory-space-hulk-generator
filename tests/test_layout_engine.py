import unittest

from pydantic import conint

from src.wrath_and_glory_space_hulk_generator.space_hulk_layouter import LayoutEngine


def get_layout_engine_from_index(index: conint(ge=0, le=len(LayoutEngine))) -> LayoutEngine:
    return next(e for i, e in enumerate(LayoutEngine) if i == index)


class TestLayoutEngine(unittest.TestCase):

    def test_index_with_member_and_member_value_expect_always_correct_index_returned(self):
        with self.subTest(i="Member"):
            expected_index = 1
            observed_index = LayoutEngine.index(get_layout_engine_from_index(expected_index).value)
            self.assertEqual(observed_index, expected_index)
        with self.subTest(i="Member.value"):
            expected_index = 0
            observed_index = LayoutEngine.index(get_layout_engine_from_index(expected_index))
            self.assertEqual(observed_index, expected_index)


if __name__ == '__main__':
    unittest.main()
