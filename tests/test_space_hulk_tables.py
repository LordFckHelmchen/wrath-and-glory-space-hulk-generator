import unittest
from dataclasses import fields

from src.wrath_and_glory_space_hulk_generator.random_table_event_collection import EventCountConstraint
from src.wrath_and_glory_space_hulk_generator.random_table import RandomTable
from src.wrath_and_glory_space_hulk_generator.random_table_event import RandomTableEventInfo
from src.wrath_and_glory_space_hulk_generator.sequenced_die import SequencedSixSidedDieRange
from src.wrath_and_glory_space_hulk_generator.space_hulk_tables import SpaceHulkTables

DUMMY_TABLE = RandomTable(table_name="Dummy table",
                          event_count_constraint=EventCountConstraint(maximum=5),
                          events=[RandomTableEventInfo(name="dummy event",
                                                       range=SequencedSixSidedDieRange(minimum=1, maximum=5))])


class TestSpaceHulkTables(unittest.TestCase):
    def setUp(self) -> None:
        self.dummy_tables = SpaceHulkTables(*tuple([DUMMY_TABLE] * 5))

    def test_getitem_with_all_valid_items_expect_correct_table_returned(self):
        for table_field in fields(self.dummy_tables):
            with self.subTest(i=table_field.name):
                self.assertEqual(self.dummy_tables[table_field.name], DUMMY_TABLE)

    def test_getitem_with_invalid_item_expect_AttributeError(self):
        with self.assertRaises(AttributeError):
            _ = self.dummy_tables["asdf932nass"]


if __name__ == '__main__':
    unittest.main()
