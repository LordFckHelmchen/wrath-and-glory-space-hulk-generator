import unittest

from tests.helpers import load_layout


class TestLayoutGraph(unittest.TestCase):
    def test_number_properties_on_all_rooms_hulk_expect_correct_numbers_returned(self):
        layout = load_layout()

        with self.subTest(i="Number of nodes"):
            self.assertEqual(layout.number_of_nodes, 21)
        with self.subTest(i="Number of edges"):
            self.assertEqual(layout.number_of_edges, 22)
