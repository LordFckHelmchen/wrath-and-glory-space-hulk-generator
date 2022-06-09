import unittest
from enum import Enum

from src.generator.layout_engine import LayoutEngine


class InvalidLayoutEngine(Enum):
    ONE = "001"
    ELEVEN = 0o11
    SIXTY_SIX = None


class TestLayoutEngine(unittest.TestCase):
    def test_is_parsable_to_member_with_members_expect_always_true(self) -> None:
        for member_type, member in {"Member": LayoutEngine.FDP,
                                    "Member name": LayoutEngine.CIRCO.name,
                                    "Member value": LayoutEngine.OSAGE.value}.items():
            with self.subTest(i=member_type):
                self.assertTrue(LayoutEngine.is_parsable_to_member(member))

    def test_is_parsable_to_member_with_non_members_and_types_expect_always_false(self) -> None:
        for non_member in [InvalidLayoutEngine.ONE, 2, "3", {"4": 5.0}]:
            with self.subTest(i=type(non_member)):
                self.assertFalse(LayoutEngine.is_parsable_to_member(non_member))

    def test_index_with_all_members_expect_always_correct_index_returned(self) -> None:
        for expected_index, engine in enumerate(LayoutEngine):
            for access_fun in [lambda x: x, lambda x: x.value, lambda x: x.name]:
                with self.subTest(i=f"{access_fun(engine)}"):
                    member = access_fun(engine)
                    self.assertEqual(expected_index,
                                     LayoutEngine.index(member),
                                     f"Expected '{expected_index}' for '{member}' of type {type(member)})")


if __name__ == '__main__':
    unittest.main()
