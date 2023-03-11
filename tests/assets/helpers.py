import pickle
from pathlib import Path

from src.generator.layout_graph import LayoutGraph
from src.generator.space_hulk import SpaceHulk
from src.generator.space_hulk_layouter import SpaceHulkLayouter

ASSET_PATH = Path(__file__).parent.resolve().absolute()
TEST_HULK_FILE = ASSET_PATH / "space_hulk_for_test.json"
TEST_HULK_LAYOUT_FILE = ASSET_PATH / "space_hulk_layout_for_test.pickle"
TEST_HULK_MARKDOWN_FILE = ASSET_PATH / "space_hulk_markdown_for_test.md"
TEST_PATH = ASSET_PATH.parent


def load_space_hulk(file_name: Path = TEST_HULK_FILE) -> SpaceHulk:
    return SpaceHulk.parse_file(file_name)


def load_space_hulk_markdown(file_name: Path = TEST_HULK_MARKDOWN_FILE) -> str:
    return file_name.read_text()


def load_space_hulk_layout(file_name: Path = TEST_HULK_LAYOUT_FILE) -> LayoutGraph:
    # noinspection PyShadowingNames
    with file_name.open("rb") as file:
        return pickle.load(file)


if __name__ == "__main__":
    space_hulk = load_space_hulk()

    # Recompute layout
    layout = SpaceHulkLayouter().create_layout(space_hulk)
    with TEST_HULK_LAYOUT_FILE.open("wb") as file:
        pickle.dump(layout, file)

    # Recompute markdown
    TEST_HULK_MARKDOWN_FILE.write_text(space_hulk.as_markdown())
