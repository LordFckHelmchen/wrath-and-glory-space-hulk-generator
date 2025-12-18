# SPDX-FileCopyrightText: Copyright (c) 2025 LordFckHelmchen
# SPDX-License-Identifier: GPL-3.0-or-later

from .indexable_enums import IndexableEnum


class LayoutFileType(IndexableEnum):
    PDF = "pdf"  # For high-res files
    PNG = "png"  # For previews
