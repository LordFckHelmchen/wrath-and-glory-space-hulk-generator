import shutil
import unittest
from copy import copy

from src.layouter.graphviz_layouter.graphviz_edge_type import GraphvizEdgeType
from src.layouter.graphviz_layouter.graphviz_engine import GraphvizEngine
from tests.assets.helpers import TEST_PATH
from tests.assets.helpers import load_space_hulk
from tests.assets.helpers import load_space_hulk_layout


class TestLayoutGraph(unittest.TestCase):
    OUTPUT_FOLDER = TEST_PATH / "generated_graphs"
    _SPACE_HULK = load_space_hulk()
    _LAYOUT = load_space_hulk_layout()

    @classmethod
    def setUpClass(cls) -> None:
        shutil.rmtree(cls.OUTPUT_FOLDER, ignore_errors=True)
        cls.OUTPUT_FOLDER.mkdir()

        # Store hulk & layout
        space_hulk_file = cls.OUTPUT_FOLDER / "space_hulk.json"
        space_hulk_file.write_text(cls._SPACE_HULK.json(exclude_none=True, indent=2))
        cls._LAYOUT.save(directory=cls.OUTPUT_FOLDER, filename="space_hulk_layout.dot")

    def setUp(self) -> None:
        self.space_hulk = copy(self._SPACE_HULK)
        self.layout = copy(self._LAYOUT)

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
                    directory=self.OUTPUT_FOLDER, filename=engine_name, format="png", cleanup=True, view=False
                )

    def test_layout_edge_type_property_access_expect_set_type_returned(self) -> None:
        for expected_value in GraphvizEdgeType:
            self.layout.edge_type = expected_value
            self.assertEqual(expected_value, self.layout.edge_type)

    def test_layout_engine_property_access_expect_set_engine_returned(self) -> None:
        for expected_value in GraphvizEngine:
            self.layout.layout_engine = expected_value
            self.assertEqual(expected_value, self.layout.layout_engine)

    def test_render_pdf_expect_no_errors(self) -> None:
        self.layout.render_pdf(file_name=self.OUTPUT_FOLDER / "space_hulk.pdf", space_hulk=self.space_hulk)


if __name__ == "__main__":
    unittest.main()
