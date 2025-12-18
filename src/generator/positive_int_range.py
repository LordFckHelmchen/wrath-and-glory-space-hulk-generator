# SPDX-FileCopyrightText: Copyright (c) 2025 LordFckHelmchen
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterator
from typing import SupportsInt

from pydantic import BaseModel
from pydantic import PositiveInt
from pydantic import ValidationInfo
from pydantic import field_validator


class PositiveIntRange(BaseModel):
    minimum: PositiveInt
    maximum: PositiveInt

    @field_validator("maximum")
    @classmethod
    def assert_min_not_larger_than_max(cls, maximum: PositiveInt, info: ValidationInfo) -> PositiveInt:
        if (minimum := info.data.get("minimum", False)) and minimum > maximum:
            msg = f"Maximum must be larger than minimum, was: minimum {minimum}, maximum {maximum}"
            raise ValueError(msg)
        return maximum

    def __contains__(self, other: SupportsInt) -> bool:
        return self.minimum <= int(other) <= self.maximum

    def __iter__(self) -> Iterator[PositiveInt]:
        yield self.minimum
        yield self.maximum
