import unittest
from enum import Enum
from typing import Any
from typing import Callable
from typing import Type

from pydantic import NonNegativeInt

from src.generator.indexable_enums import IndexableEnum


class InvalidLayoutEngine(Enum):
    ONE = "001"
    ELEVEN = 0o11
    SIXTY_SIX = None


EvaluationFunction = Callable[[Type[IndexableEnum], NonNegativeInt, Any], None]


class TestIndexableEnum(unittest.TestCase):
    def run_for_each_subclass_and_member_access_type(self, eval_fun: EvaluationFunction) -> None:
        for indexable_enum_subclass in IndexableEnum.__subclasses__():
            for member_index, member in enumerate(indexable_enum_subclass):
                for access_fun in [lambda x: x, lambda x: x.value, lambda x: x.name]:
                    accessed_member = access_fun(member)
                    with self.subTest(i=f"{member}: {accessed_member}"):
                        eval_fun(indexable_enum_subclass, member_index, accessed_member)

    def test_is_parsable_to_member_with_members_expect_always_true(self) -> None:
        def validator(indexable_enum_subclass: Type[IndexableEnum],
                      member_index: NonNegativeInt,
                      accessed_member: Any) -> None:
            self.assertTrue(indexable_enum_subclass.is_parsable_to_member(accessed_member))

        self.run_for_each_subclass_and_member_access_type(validator)

    def test_is_parsable_to_member_with_non_members_and_types_expect_always_false(self) -> None:
        for indexable_enum_subclass in IndexableEnum.__subclasses__():
            for non_member in InvalidLayoutEngine:
                for access_fun in [lambda x: x, lambda x: x.value, lambda x: x.name]:
                    accessed_non_member = access_fun(non_member)
                    with self.subTest(i=f"{indexable_enum_subclass}: {accessed_non_member}"):
                        self.assertFalse(indexable_enum_subclass.is_parsable_to_member(accessed_non_member))

    def test_index_with_members_expect_always_correct_index_returned(self) -> None:
        def validator(indexable_enum_subclass: Type[IndexableEnum],
                      expected_member_index: NonNegativeInt,
                      accessed_member: Any) -> None:
            self.assertEqual(expected_member_index,
                             indexable_enum_subclass.index(accessed_member),
                             f"Expected '{expected_member_index}' "
                             f"for '{accessed_member}' of type {type(accessed_member)})")

        self.run_for_each_subclass_and_member_access_type(validator)


if __name__ == '__main__':
    unittest.main()
