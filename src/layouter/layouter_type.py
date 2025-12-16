# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025 The Wrath & Glory Space Hulk Generator contributors


from .de_broglie_layouter import DeBroglieLayouter
from .graphviz_layouter import GraphvizLayouter
from .indexable_enums import IndexableEnum


class LayouterType(IndexableEnum):
    GRAPHVIZ = GraphvizLayouter
    DE_BROGLIE = DeBroglieLayouter
