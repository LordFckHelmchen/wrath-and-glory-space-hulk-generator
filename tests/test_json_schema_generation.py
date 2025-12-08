import json
import unittest

from pydantic.v1.json import pydantic_encoder
from pydantic.v1.main import ModelMetaclass

from src.generator.map_object_size import MapObjectSizeConstraint
from src.generator.random_table import RandomTable
from src.generator.sequenced_die import SequencedDie
from src.generator.space_hulk import SpaceHulk
from tests.assets.helpers import create_clean_test_folder


class TestSchemaGeneration(unittest.TestCase):
    output_folder = create_clean_test_folder("generated_json_schema")

    @classmethod
    def generate_schema(cls, schema_cls: ModelMetaclass) -> None:
        schema_file = cls.output_folder / f"{schema_cls.__name__}.json"
        with schema_file.open("w") as schema_file:
            json.dump(schema_cls.schema(), schema_file, indent=2, default=pydantic_encoder)

    def test_generate_json_schemas_expect_no_errors(self) -> None:
        for schema_cls in [MapObjectSizeConstraint, RandomTable, SequencedDie, SpaceHulk]:
            with self.subTest(i=schema_cls.__name__):
                self.generate_schema(schema_cls)


if __name__ == "__main__":
    unittest.main()
