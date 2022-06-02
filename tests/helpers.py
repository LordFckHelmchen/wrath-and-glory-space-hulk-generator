import pickle
from pathlib import Path

from src.wrath_and_glory_space_hulk_generator.layout_graph import LayoutGraph
from src.wrath_and_glory_space_hulk_generator.space_hulk import SpaceHulk
from src.wrath_and_glory_space_hulk_generator.space_hulk_layouter import SpaceHulkLayouter

TEST_HULK_FILE = Path("space_hulk_for_test.json")
TEST_HULK_LAYOUT_FILE = Path("space_hulk_layout_for_test.pickle")


def load_space_hulk(path_to_space_hulk: Path = TEST_HULK_FILE) -> SpaceHulk:
    return SpaceHulk.parse_file(path_to_space_hulk)


def load_layout(path_to_layout: Path = TEST_HULK_LAYOUT_FILE) -> LayoutGraph:
    with path_to_layout.open("rb") as file:
        return pickle.load(file)


if __name__ == '__main__':
    # Recompute layout
    layout = SpaceHulkLayouter().create_layout(load_space_hulk())
    with TEST_HULK_LAYOUT_FILE.open("wb") as file:
        pickle.dump(layout, file)
