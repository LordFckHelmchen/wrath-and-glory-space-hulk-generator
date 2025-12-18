# SPDX-FileCopyrightText: Copyright (c) 2025 LordFckHelmchen
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest

from src.generator.random_table_event import RandomTableEvent
from src.generator.random_table_event_collection import EventCountConstraint
from src.generator.random_table_event_collection import RandomTableEventCollection


class TestRandomTableEventCollection(unittest.TestCase):
    def test_set_events_with_duplicated_event_names_expect_all_events_present_but_with_modified_event_names(
        self,
    ) -> None:
        dummy_event = RandomTableEvent(name="test")
        expected_event_count = 2
        event_collection = RandomTableEventCollection(
            event_count_constraint=EventCountConstraint(), events=[dummy_event] * expected_event_count
        )
        assert expected_event_count == len(event_collection)
        assert event_collection.events[0].name != event_collection.events[1].name


if __name__ == "__main__":
    unittest.main()
