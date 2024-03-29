import unittest

from src.generator.map_object_size import MapObjectDimensionConstraint
from src.generator.map_object_size import MapObjectSizeInt


class TestMapObjectSize(unittest.TestCase):
    def test_init_with_equal_limits_expect_ValueError(self):
        with self.assertRaises(ValueError):
            _ = MapObjectDimensionConstraint(minimum=MapObjectSizeInt(1), maximum=MapObjectSizeInt(1))


if __name__ == "__main__":
    unittest.main()
