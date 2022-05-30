import pickle
from pathlib import Path

from src.wrath_and_glory_space_hulk_generator.layout_graph import LayoutGraph
from src.wrath_and_glory_space_hulk_generator.space_hulk import SpaceHulk
from src.wrath_and_glory_space_hulk_generator.space_hulk_layouter import SpaceHulkLayouter


def get_all_rooms_space_hulk(path_to_space_hulk: Path = Path("space_hulk_for_test.json")) -> SpaceHulk:
    return SpaceHulk.parse_file(path_to_space_hulk)


def get_all_rooms_layout(path_to_layout: Path = Path("space_hulk_layout_for_test.pickle")) -> LayoutGraph:
    if not path_to_layout.exists():
        layout = SpaceHulkLayouter().create_layout(get_all_rooms_space_hulk())
        with path_to_layout.open("wb") as file:
            pickle.dump(layout, file)

    with path_to_layout.open("rb") as file:
        return pickle.load(file)
