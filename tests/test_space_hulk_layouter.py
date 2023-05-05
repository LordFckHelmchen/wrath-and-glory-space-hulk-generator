import unittest

from src.layouter.graphviz_layouter.graphviz_layouter import SpaceHulkLayouter
from src.layouter.graphviz_layouter.indexable_enums import LayoutEdgeType
from src.layouter.graphviz_layouter.indexable_enums import LayoutEngine


class TestSpaceHulkLayouter(unittest.TestCase):
    def test_set_get_layout_edge_type_expect_set_type_returned(self):
        layouter = SpaceHulkLayouter()
        for expected_value in LayoutEdgeType:
            layouter.set_layout_edge_type(expected_value)
            self.assertEqual(expected_value, layouter.get_layout_edge_type())

    def test_set_get_layout_engine_expect_set_engine_returned(self):
        layouter = SpaceHulkLayouter()
        for expected_value in LayoutEngine:
            layouter.set_layout_engine(expected_value)
            self.assertEqual(expected_value, layouter.get_layout_engine())
