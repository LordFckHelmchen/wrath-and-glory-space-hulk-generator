class MaximumMustBeLargerThanMinimumError(ValueError):
    """Raise when a monotonic range is not monotonic"""


class DigitsMustBeInRangeOfItsSidesError(ValueError):
    """Raise when a die-digit is initialized with outside its defined sides"""
