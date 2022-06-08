import unittest

from tests.helpers import load_layout


class TestLayoutGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.layout = load_layout()

    def test_number_properties_on_all_rooms_hulk_expect_correct_numbers_returned(self):
        with self.subTest(i="Number of nodes"):
            self.assertEqual(self.layout.number_of_nodes, 21)
        with self.subTest(i="Number of edges"):
            self.assertEqual(self.layout.number_of_edges, 22)

    def test_str_with_same_comment_on_multiple_calls_expect_comment_unchanged_after_each_call(self):
        expected_comment = self.layout.comment
        _ = str(self.layout)
        self.assertEqual(expected_comment, self.layout.comment)
