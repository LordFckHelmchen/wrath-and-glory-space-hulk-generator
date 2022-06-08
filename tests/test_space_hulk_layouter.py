import unittest

from src.wrath_and_glory_space_hulk_generator.random_table_event import RandomTableEvent
from src.wrath_and_glory_space_hulk_generator.space_hulk_layouter import SpaceHulkLayouter
from tests.helpers import load_space_hulk


class TestSpaceHulkLayouter(unittest.TestCase):
    def test_create_layout_with_duplicated_rooms_expect_same_number_of_rooms_in_layout_and_hulk(self):
        space_hulk = load_space_hulk()
        space_hulk.rooms.events.append(RandomTableEvent(name=space_hulk.rooms.events[0].name,
                                                        size=space_hulk.rooms.events[1].size))

        layout = SpaceHulkLayouter().create_layout(space_hulk)
        self.assertEqual(len(space_hulk.rooms), layout.number_of_nodes)


if __name__ == '__main__':
    unittest.main()
