import unittest

from src.generator.positive_int_range import PositiveIntRange
from src.generator.sequenced_die import SequencedSixSidedDieRange


class TestPositiveIntRange(unittest.TestCase):
    def test_init_with_out_of_order_limits_expect_ValueError(self):
        with self.assertRaises(ValueError):
            _ = PositiveIntRange(minimum=2, maximum=1)

    def test_init_with_equal_limits_expect_success(self):
        _ = SequencedSixSidedDieRange(minimum=1, maximum=1)


class TestSequencedSixSidedDieRange(unittest.TestCase):

    def test_init_with_out_of_range_limits_expect_ValueError(self):
        with self.assertRaises(ValueError):
            _ = SequencedSixSidedDieRange(minimum=0, maximum=5)


if __name__ == '__main__':
    unittest.main()
