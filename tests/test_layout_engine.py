import unittest

from pydantic import conint

from src.wrath_and_glory_space_hulk_generator.layout_engine import LayoutEngine


def get_layout_engine_from_index(index: conint(ge=0, le=len(LayoutEngine))) -> LayoutEngine:
    return next(e for i, e in enumerate(LayoutEngine) if i == index)


class TestLayoutEngine(unittest.TestCase):

    def test_index_with_member_attributes_expect_always_correct_index_returned(self):
        for expected_index, (engine, access_fun) in enumerate(
                zip(LayoutEngine, [lambda x: x, lambda x: x.value, lambda x: x.name])):
            with self.subTest(i=f"{access_fun(engine)}"):
                observed_index = LayoutEngine.index(access_fun(engine))
                self.assertEqual(observed_index, expected_index, f"Expected {expected_index} for {access_fun(engine)}")


if __name__ == '__main__':
    unittest.main()
