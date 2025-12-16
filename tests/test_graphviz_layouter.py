# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025 The Wrath & Glory Space Hulk Generator contributors


import unittest

from src.layouter.graphviz_layouter.graphviz_edge_type import GraphvizEdgeType
from src.layouter.graphviz_layouter.graphviz_engine import GraphvizEngine
from src.layouter.graphviz_layouter.graphviz_layouter import GraphvizLayouter


class TestGraphvizLayouter(unittest.TestCase):
    def test_set_get_layout_edge_type_expect_set_type_returned(self) -> None:
        layouter = GraphvizLayouter()
        for expected_value in GraphvizEdgeType:
            layouter.set_layout_edge_type(expected_value)
            assert expected_value == layouter.get_layout_edge_type()

    def test_set_get_layout_engine_expect_set_engine_returned(self) -> None:
        layouter = GraphvizLayouter()
        for expected_value in GraphvizEngine:
            layouter.set_layout_engine(expected_value)
            assert expected_value == layouter.get_layout_engine()
