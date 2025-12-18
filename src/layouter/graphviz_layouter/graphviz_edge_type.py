# SPDX-FileCopyrightText: Copyright (c) 2025 LordFckHelmchen
# SPDX-License-Identifier: GPL-3.0-or-later

from src.layouter.indexable_enums import IndexableEnum


class GraphvizEdgeType(IndexableEnum):
    LINE = "line"
    ORTHO = "ortho"
    SPLINES = "spline"
