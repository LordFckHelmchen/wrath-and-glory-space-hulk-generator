import shutil
import unittest
from pathlib import Path

from src.wrath_and_glory_space_hulk_generator.space_hulk_layouter import LayoutEngine
from tests.helpers import get_all_rooms_layout
from tests.helpers import get_all_rooms_space_hulk


class TestSpaceHulkLayouter(unittest.TestCase):
    def test_construction_expect_no_errors(self):
        graph_folder = Path("./generated_graphs/")
        shutil.rmtree(graph_folder, ignore_errors=True)
        graph_folder.mkdir()

        space_hulk = get_all_rooms_space_hulk()
        layout = get_all_rooms_layout()

        (graph_folder / f"space_hulk.json").write_text(space_hulk.json(exclude_none=True))
        layout.save(directory=graph_folder, filename="space_hulk_layout.dot")
        print(layout)

        for engine in LayoutEngine:
            engine_name = engine.value
            with self.subTest(i=engine_name):
                layout.engine = engine_name
                layout.view(directory=graph_folder, filename=engine_name, cleanup=True)

    def test_number_properties_on_all_rooms_hulk_expect_correct_numbers_returned(self):
        layout = get_all_rooms_layout()

        with self.subTest(i="Number of nodes"):
            self.assertEqual(layout.number_of_nodes, 21)
        with self.subTest(i="Number of edges"):
            self.assertEqual(layout.number_of_edges, 20)


if __name__ == '__main__':
    unittest.main()
