import unittest

from src.wrath_and_glory_space_hulk_generator.exceptions import EventCountOutOfRangeError
from src.wrath_and_glory_space_hulk_generator.exceptions import EventTypeError
from tests.helpers import get_all_rooms_space_hulk


class TestSpaceHulkTables(unittest.TestCase):
    def setUp(self) -> None:
        self.space_hulk = get_all_rooms_space_hulk()

    def test_getitem_with_all_valid_table_names_expect_always_correct_table_returned(self) -> None:
        for table_name, table_value in self.space_hulk:
            with self.subTest(i=table_name):
                self.assertEqual(self.space_hulk[table_name], table_value)

    def test_getitem_with_invalid_table_name_expect_AttributeError(self) -> None:
        with self.assertRaises(AttributeError):
            _ = self.space_hulk["asdf932nass"]

    def test_setitem_with_valid_non_empty_value_expect_success(self) -> None:
        self.space_hulk["occupations"].events = self.space_hulk["occupations"].events[:-1]

    def test_setitem_with_empty_value_for_table_that_prohibits_empty_values_expect_EventCountOutOfRangeError(
            self) -> None:
        with self.assertRaises(EventCountOutOfRangeError):
            self.space_hulk["rooms"].events = []

    # noinspection PyTypeChecker
    def test_setitem_with_invalid_value_type_on_table_with_previously_set_empty_value_expect_EventTypeError(
            self) -> None:
        with self.subTest(i="Set empty value on table that allows empty values"):
            self.space_hulk["hazards"].events = []
        with self.subTest(i="Set invalid value"):
            with self.assertRaises(EventTypeError):
                self.space_hulk["hazards"].events = [5]

    # noinspection PyTypeChecker
    def test_setitem_with_invalid_value_types_expect_always_EventTypeError(self) -> None:
        for table_name, table_value in self.space_hulk:
            with self.subTest(i=table_name):
                with self.assertRaises(EventTypeError):
                    self.space_hulk[table_name].events = table_value.events[0]

                with self.assertRaises(EventTypeError):
                    self.space_hulk[table_name].events = [2]

    def test_setitem_with_invalid_table_name_expect_AttributeError(self):
        with self.assertRaises(AttributeError):
            self.space_hulk["asdf932nass"].events = self.space_hulk["rooms"].events

    def test_is_valid_event_list_for_table_with_invalid_table_name_expect_AttributeError(self) -> None:
        with self.assertRaises(AttributeError):
            self.space_hulk.is_valid_event_list_for_table("asdf932nass", self.space_hulk["rooms"].events)

    def test_is_valid_event_list_for_table_with_out_of_bounds_sized_lists_expect_always_False(self) -> None:
        for event_list in [[], self.space_hulk["rooms"].events[0:1] * 500]:
            with self.subTest(i=f"List length {len(event_list)}"):
                self.assertFalse(self.space_hulk.is_valid_event_list_for_table("rooms", event_list))

    # noinspection PyTypeChecker
    def test_is_valid_event_list_for_table_with_invalid_outer_type_expect_False(self) -> None:
        self.assertFalse(self.space_hulk.is_valid_event_list_for_table("rooms", 5))

    # noinspection PyTypeChecker
    def test_is_valid_event_list_for_table_with_invalid_event_type_expect_False(self) -> None:
        self.assertFalse(self.space_hulk.is_valid_event_list_for_table("rooms", [5]))


if __name__ == '__main__':
    unittest.main()