import hashlib
import unittest
from pathlib import Path

from src.layouter.de_broglie_layouter import DeBroglieLayouter
from src.layouter.layout_file_type import LayoutFileType
from tests.assets.helpers import create_clean_test_folder
from tests.assets.helpers import load_space_hulk


class TestDeBroglieLayouter(unittest.TestCase):
    output_folder = create_clean_test_folder("generated_de_broglie_layouts")
    space_hulk = load_space_hulk()

    @staticmethod
    def get_file_hash(file_name: Path) -> str:
        return hashlib.md5(file_name.read_bytes()).hexdigest()  # noqa: S324  # We only use it to compare the contents

    def setUp(self) -> None:
        self.layouter = DeBroglieLayouter()

        # Make sure that the file does not exist
        self.layouter.output_file.unlink(missing_ok=True)

        self.output_file_hash = None

    def assertNonEmptyFileExists(self, file_name: Path) -> None:
        msg = f"'{file_name}' is not a valid file!"
        assert file_name.is_file(), msg

        msg = f"'{file_name}' was empty!"
        assert file_name.stat().st_size > 0, msg

    def assertOutputFileUnchanged(self) -> None:
        new_output_file_hash = self.get_file_hash(self.layouter.output_file)
        msg = new_output_file_hash, f"Content of output file '{self.layouter.output_file}' has changed!"
        assert self.output_file_hash == new_output_file_hash, msg

    def test_create_layout_expect_output_file_created(self) -> None:
        # Assert that the file did not exist before.
        assert not self.layouter.output_file.exists()

        _ = self.layouter.create_layout(self.space_hulk)
        self.assertNonEmptyFileExists(self.layouter.output_file)

    def test_render_to_file_expect_output_file_exists_unchanged_and_target_file_created(self) -> None:
        for file_type in LayoutFileType:
            with self.subTest(i=file_type):
                # ARRANGE
                target_file = self.output_folder / f"de_broglie_layout.{file_type.value}"
                layout = self.layouter.create_layout(self.space_hulk)
                expected_output_file_hash = self.get_file_hash(self.layouter.output_file)

                # ACT
                layout.render_to_file(target_file)
                actual_output_file_hash = self.get_file_hash(self.layouter.output_file)

                # ASSERT
                msg = f"Content of output file '{self.layouter.output_file}' has changed!"
                assert expected_output_file_hash == actual_output_file_hash, msg
                self.assertNonEmptyFileExists(target_file)
