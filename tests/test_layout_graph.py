import shutil
import unittest
from pathlib import Path

from src.generator.indexable_enums import LayoutEngine
from src.generator.space_hulk_layouter import SpaceHulkLayouter
from tests.helpers import load_layout
from tests.helpers import load_space_hulk


class TestLayoutGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.layout = load_layout()

    def test_number_properties_on_all_rooms_hulk_expect_correct_numbers_returned(self):
        with self.subTest(i="Number of nodes"):
            self.assertEqual(self.layout.number_of_nodes, 21)
        with self.subTest(i="Number of edges"):
            self.assertEqual(self.layout.number_of_edges, 20)

    def test_str_with_same_comment_on_multiple_calls_expect_comment_unchanged_after_each_call(self):
        expected_comment = self.layout.comment
        _ = str(self.layout)
        self.assertEqual(expected_comment, self.layout.comment)

    def test_render_all_possible_engines_expect_no_errors(self):
        graph_folder = Path("./generated_graphs/")
        shutil.rmtree(graph_folder, ignore_errors=True)
        graph_folder.mkdir()
        layout = load_layout()

        # Store hulk & layout
        (graph_folder / f"space_hulk.json").write_text(load_space_hulk().json(exclude_none=True, indent=2))
        layout.graph_attr = SpaceHulkLayouter.DEFAULT_GRAPH_PROPERTIES["graph_attr"]
        layout.save(directory=graph_folder, filename="space_hulk_layout.dot")

        for engine in LayoutEngine:
            engine_name = engine.value
            with self.subTest(i=engine_name):
                layout.engine = engine_name
                layout.render(directory=graph_folder, filename=engine_name, format="png", cleanup=True, view=False)
