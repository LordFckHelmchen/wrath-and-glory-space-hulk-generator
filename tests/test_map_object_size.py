import unittest

import pytest

from src.generator.exceptions import DimensionConstraintOfZeroSizeError
from src.generator.map_object_size import MapObjectDimensionConstraint
from src.generator.map_object_size import MapObjectSizeInt


class TestMapObjectSize(unittest.TestCase):
    def test_init_with_equal_limits_expect_error(self) -> None:
        with pytest.raises(DimensionConstraintOfZeroSizeError):
            _ = MapObjectDimensionConstraint(minimum=MapObjectSizeInt(1), maximum=MapObjectSizeInt(1))


if __name__ == "__main__":
    unittest.main()
