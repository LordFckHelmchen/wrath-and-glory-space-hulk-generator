import json
import shutil
import unittest
from pathlib import Path

from pydantic.json import pydantic_encoder

from src.wrath_and_glory_space_hulk_generator.map_object_size import MapObjectSizeConstraint
from src.wrath_and_glory_space_hulk_generator.random_table import RandomTable
from src.wrath_and_glory_space_hulk_generator.sequenced_die import SequencedDie
from src.wrath_and_glory_space_hulk_generator.space_hulk import SpaceHulk


class TestSchemaGeneration(unittest.TestCase):
    @staticmethod
    def generate_schema(schema_cls, target_folder: Path = "."):
        with open(target_folder / f"{schema_cls.__name__}.json", "w") as schema_file:
            json.dump(schema_cls.schema(), schema_file, indent=2, default=pydantic_encoder)

    def test_generate_json_schemas_expect_no_errors(self):
        schema_folder = Path("./generated_json_schema/")
        shutil.rmtree(schema_folder, ignore_errors=True)
        schema_folder.mkdir()

        for schema_cls in [MapObjectSizeConstraint, RandomTable, SequencedDie, SpaceHulk]:
            with self.subTest(i=schema_cls.__name__):
                self.generate_schema(schema_cls, schema_folder)


if __name__ == '__main__':
    unittest.main()
