# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025 The Wrath & Glory Space Hulk Generator contributors



import re
from dataclasses import dataclass
from typing import ClassVar
from typing import Literal

from fpdf import FPDF
from pydantic import PositiveInt


@dataclass
class FontFormat:
    style: Literal["", "B", "I", "U", "BU", "UB", "BI", "IB", "IU", "UI", "BIU", "BUI", "IBU", "IUB", "UBI", "UIB"]
    size: PositiveInt
    height: PositiveInt


class Markdown2PdfParser:
    font: str = "Arial"
    header_formats: ClassVar[dict[str, FontFormat]] = {
        "#": FontFormat(style="B", size=18, height=12),
        "##": FontFormat(style="B", size=16, height=10),
        "###": FontFormat(style="B", size=14, height=8),
    }
    body_format: FontFormat = FontFormat(style="", size=11, height=5)
    content_regex: str = r"((?P<header_level>#+) (?P<header>.+)\n|(?P<body>[^#]*))"

    def parse(self, text: str) -> FPDF:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font(self.font)

        for content_match in re.finditer(self.content_regex, text):
            font_format = self.header_formats.get(content_match.group("header_level"), self.body_format)
            pdf.set_font("", style=font_format.style, size=font_format.size)
            if content_match.group("header"):
                pdf.cell(w=0, h=font_format.height, txt=content_match.group("header"))
            else:
                pdf.multi_cell(w=0, h=font_format.height, txt=content_match.group("body"))
            pdf.ln()

        return pdf
