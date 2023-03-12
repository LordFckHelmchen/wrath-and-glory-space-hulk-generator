import unittest

from src.generator.random_table_event import RandomTableEvent
from src.generator.random_table_event_collection import EventCountConstraint
from src.generator.random_table_event_collection import RandomTableEventCollection


class TestRandomTableEventCollection(unittest.TestCase):
    def test_set_events_with_duplicated_event_names_expect_all_events_present_but_with_modified_event_names(self):
        dummy_event = RandomTableEvent(name="test")
        expected_event_count = 2
        event_collection = RandomTableEventCollection(
            event_count_constraint=EventCountConstraint(), events=[dummy_event] * expected_event_count
        )
        self.assertEqual(expected_event_count, len(event_collection))
        self.assertNotEqual(event_collection.events[0].name, event_collection.events[1].name)


if __name__ == "__main__":
    unittest.main()
