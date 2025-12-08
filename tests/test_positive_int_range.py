import unittest

import pytest

from src.generator.exceptions import DigitOutOfRangeOfDieError
from src.generator.exceptions import RangeNotSortedError
from src.generator.positive_int_range import PositiveIntRange
from src.generator.sequenced_die import SequencedSixSidedDieRange


class TestPositiveIntRange(unittest.TestCase):
    def test_init_with_out_of_order_limits_expect_error(self) -> None:
        with pytest.raises(RangeNotSortedError):
            _ = PositiveIntRange(minimum=2, maximum=1)


class TestSequencedSixSidedDieRange(unittest.TestCase):
    def test_init_with_out_of_range_limits_expect_error(self) -> None:
        with pytest.raises(DigitOutOfRangeOfDieError):
            _ = SequencedSixSidedDieRange(minimum=0, maximum=5)

    def test_init_with_equal_limits_expect_success(self) -> None:
        _ = SequencedSixSidedDieRange(minimum=1, maximum=1)


if __name__ == "__main__":
    unittest.main()
