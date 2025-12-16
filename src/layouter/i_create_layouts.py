# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025 The Wrath & Glory Space Hulk Generator contributors



from abc import ABC
from abc import abstractmethod

from src.generator.space_hulk import SpaceHulk

from .i_layout import ILayout


class ICreateLayouts(ABC):
    @abstractmethod
    def create_layout(self, space_hulk: SpaceHulk) -> ILayout:
        pass
