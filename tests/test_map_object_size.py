import unittest

import pytest
from pydantic import ValidationError

from src.generator.map_object_size import MapObjectDimensionConstraint


class TestMapObjectSize(unittest.TestCase):
    def test_init_with_equal_limits_expect_error(self) -> None:
        with pytest.raises(ValidationError, match="Minimum & maximum must not be equal"):
            _ = MapObjectDimensionConstraint(minimum=1, maximum=1)


if __name__ == "__main__":
    unittest.main()
