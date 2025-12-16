# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025 The Wrath & Glory Space Hulk Generator contributors


from .indexable_enums import IndexableEnum


class LayoutFileType(IndexableEnum):
    PDF = "pdf"  # For high-res files
    PNG = "png"  # For previews
