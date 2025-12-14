import unittest

import pytest
from pydantic import ValidationError

from src.generator.positive_int_range import PositiveIntRange
from src.generator.sequenced_die import SequencedSixSidedDieRange


class TestPositiveIntRange(unittest.TestCase):
    def test_init_with_out_of_order_limits_expect_error(self) -> None:
        with pytest.raises(ValidationError, match="Maximum must be larger than minimum"):
            _ = PositiveIntRange(minimum=2, maximum=1)


class TestSequencedSixSidedDieRange(unittest.TestCase):
    def test_init_with_out_of_range_limits_expect_error(self) -> None:
        with pytest.raises(ValidationError, match="All digits must be within \\[1, 6\\]"):
            _ = SequencedSixSidedDieRange(minimum=1, maximum=7)

    def test_init_with_equal_limits_expect_success(self) -> None:
        _ = SequencedSixSidedDieRange(minimum=1, maximum=1)


if __name__ == "__main__":
    unittest.main()
