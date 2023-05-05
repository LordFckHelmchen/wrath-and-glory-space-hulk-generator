import unittest
from copy import copy

from src.layouter.graphviz_layouter.graphviz_edge_type import GraphvizEdgeType
from src.layouter.graphviz_layouter.graphviz_engine import GraphvizEngine
from src.layouter.layout_file_type import LayoutFileType
from tests.assets.helpers import create_clean_test_folder
from tests.assets.helpers import load_space_hulk
from tests.assets.helpers import load_space_hulk_layout


class TestLayoutGraph(unittest.TestCase):
    output_folder = create_clean_test_folder("generated_graph_layouts")
    _space_hulk = load_space_hulk()
    _layout = load_space_hulk_layout()

    @classmethod
    def setUpClass(cls) -> None:
        # Store hulk & layout
        space_hulk_file = cls.output_folder / "space_hulk.json"
        space_hulk_file.write_text(cls._space_hulk.json(exclude_none=True, indent=2))
        cls._layout.save(directory=cls.output_folder, filename="space_hulk_layout.dot")

    def setUp(self) -> None:
        self.space_hulk = copy(self._space_hulk)
        self.layout = copy(self._layout)

    def test_number_properties_on_all_rooms_hulk_expect_correct_numbers_returned(self) -> None:
        with self.subTest(i="Number of nodes"):
            self.assertEqual(self.layout.number_of_nodes, 21)
        with self.subTest(i="Number of edges"):
            self.assertEqual(self.layout.number_of_edges, 22)

    def test_str_with_same_comment_on_multiple_calls_expect_comment_unchanged_after_each_call(self) -> None:
        expected_comment = self.layout.comment
        _ = str(self.layout)
        self.assertEqual(expected_comment, self.layout.comment)

    def test_render_all_possible_engines_expect_no_errors(self) -> None:
        for engine in GraphvizEngine:
            engine_name = engine.value
            with self.subTest(i=engine_name):
                self.layout.engine = engine_name
                self.layout.render(
                    directory=self.output_folder, filename=engine_name, format="png", cleanup=True, view=False
                )

    def test_layout_edge_type_property_access_expect_set_type_returned(self) -> None:
        for expected_value in GraphvizEdgeType:
            self.layout.edge_type = expected_value
            self.assertEqual(expected_value, self.layout.edge_type)

    def test_layout_engine_property_access_expect_set_engine_returned(self) -> None:
        for expected_value in GraphvizEngine:
            self.layout.layout_engine = expected_value
            self.assertEqual(expected_value, self.layout.layout_engine)

    def test_render_to_file_as_pdf_expect_no_errors(self) -> None:
        self.layout.render_to_file(file_name=self.output_folder / f"space_hulk.{LayoutFileType.PDF.value}")


if __name__ == "__main__":
    unittest.main()
