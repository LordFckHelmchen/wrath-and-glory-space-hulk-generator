import shutil
import unittest
from pathlib import Path

from src.wrath_and_glory_space_hulk_generator.space_hulk_layouter import LayoutEngine
from tests.helpers import load_layout
from tests.helpers import load_space_hulk


class TestSpaceHulkLayouter(unittest.TestCase):
    def setUp(self) -> None:
        self.layout = load_layout()

    def test_construction_expect_no_errors(self):
        graph_folder = Path("./generated_graphs/")
        shutil.rmtree(graph_folder, ignore_errors=True)
        graph_folder.mkdir()

        # Store hulk & layout
        (graph_folder / f"space_hulk.json").write_text(load_space_hulk().json(exclude_none=True, indent=2))
        self.layout.save(directory=graph_folder, filename="space_hulk_layout.dot")

        for engine in LayoutEngine:
            engine_name = engine.value
            with self.subTest(i=engine_name):
                self.layout.engine = engine_name
                self.layout.render(directory=graph_folder, filename=engine_name, cleanup=True, view=False)

    def test_number_properties_on_all_rooms_hulk_expect_correct_numbers_returned(self):
        with self.subTest(i="Number of nodes"):
            self.assertEqual(self.layout.number_of_nodes, 21)
        with self.subTest(i="Number of edges"):
            self.assertEqual(self.layout.number_of_edges, 20)


if __name__ == '__main__':
    unittest.main()
