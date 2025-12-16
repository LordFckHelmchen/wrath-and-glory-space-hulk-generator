# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025 The Wrath & Glory Space Hulk Generator contributors



from collections.abc import Iterable
from enum import Enum
from math import ceil
from math import log10
from random import randint
from typing import ClassVar
from typing import Self

from pydantic import BaseModel
from pydantic import Field
from pydantic import PositiveInt
from pydantic import field_validator

from .positive_int_range import PositiveIntRange


class DieType(Enum):
    D6 = "D6"
    D66 = "D66"


class SequencedDie(BaseModel):
    sides: PositiveInt = Field(exclude=True)
    number_of_dice: PositiveInt = Field(exclude=True)

    @classmethod
    def from_die_type(cls, die_type: DieType) -> Self:
        match die_type:
            case DieType.D6:
                return cls(sides=6, number_of_dice=1)
            case DieType.D66:
                return cls(sides=6, number_of_dice=2)
            case _:
                msg = f"Unsupported die type '{die_type}'"
                raise ValueError(msg)

    @staticmethod
    def _make_roll_from_sequence(sequence_of_rolls: Iterable[PositiveInt]) -> PositiveInt:
        return int("".join(str(i) for i in sequence_of_rolls))

    @staticmethod
    def _get_sequence_from_roll(roll: PositiveInt) -> list[PositiveInt]:
        return [PositiveInt(s) for s in str(roll)]

    def roll(self) -> PositiveInt:
        return self._make_roll_from_sequence(randint(1, self.sides) for _ in range(self.number_of_dice))

    def roll_bulk(self, number_of_rolls: PositiveInt) -> list[PositiveInt]:
        return [self.roll() for _ in range(number_of_rolls)]

    def get_ones_die_from_roll(self, roll: PositiveInt) -> PositiveInt:
        return roll % 10**self.decimal_dimension

    @property
    def decimal_dimension(self) -> PositiveInt:
        return ceil(log10(self.sides + 0.1))  # 0.1 to get the exact matches right

    def are_consecutive_rolls(self, roll_1: PositiveInt, roll_2: PositiveInt) -> bool:
        if roll_1 == roll_2:
            return True

        next_roll_to_1_single_rolls = self._get_sequence_from_roll(roll_1 + 1)

        i = len(next_roll_to_1_single_rolls) - 1
        while next_roll_to_1_single_rolls[i] >= self.sides and i > 0:
            next_roll_to_1_single_rolls[i - 1] += next_roll_to_1_single_rolls[i] % self.sides
            next_roll_to_1_single_rolls[i] = 1

        return roll_2 == self._make_roll_from_sequence(next_roll_to_1_single_rolls)

    @classmethod
    def from_events(cls, events: list) -> Self:
        if len(events) == 0:
            msg = "Events list must be non-empty!"
            raise ValueError(msg)

        number_of_dice = 0
        sides = 0
        for event in events:
            for lim in event.range:
                lim_digits = cls._get_sequence_from_roll(lim)
                number_of_dice = max(number_of_dice, len(lim_digits))
                sides = max(sides, *lim_digits)
        return cls(sides=sides, number_of_dice=number_of_dice)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, SequencedDie)
            and self.sides == other.sides
            and self.number_of_dice == other.number_of_dice
        )

    def __hash__(self) -> int:
        return hash((self.sides, self.number_of_dice))


class SequencedSixSidedDieRange(PositiveIntRange):
    SIDES: ClassVar[PositiveInt] = 6

    @field_validator("*")
    @classmethod
    def assert_digits_in_range_for_six_sided_die(cls, v: PositiveInt) -> PositiveInt:
        if not all(1 <= int(d) <= cls.SIDES for d in str(v)):
            msg = f"All digits must be within [1, {cls.SIDES}], was {v}"
            raise ValueError(msg)

        return v
