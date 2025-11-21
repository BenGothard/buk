from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent

from .models import BookIdea, CoverArt, GeneratedMetadata


@dataclass
class CoverBuilder:
    idea: BookIdea
    metadata: GeneratedMetadata

    def build(self) -> CoverArt:
        svg = self._basic_svg()
        return CoverArt(svg_content=svg)

    def _basic_svg(self) -> str:
        palette = ["#2b2d42", "#8d99ae", "#edf2f4"]
        title = self.metadata.title
        subtitle = self.metadata.subtitle
        author = self.metadata.author
        return dedent(
            f"""
            <svg xmlns='http://www.w3.org/2000/svg' width='1800' height='2700' viewBox='0 0 1800 2700'>
              <rect width='1800' height='2700' fill='{palette[0]}' />
              <rect x='120' y='120' width='1560' height='2460' rx='48' fill='{palette[1]}' />
              <rect x='180' y='180' width='1440' height='2340' rx='36' fill='{palette[2]}' />
              <text x='900' y='900' font-family='Georgia, serif' font-size='120' fill='{palette[0]}' text-anchor='middle' font-weight='700'>{title}</text>
              <text x='900' y='1100' font-family='Georgia, serif' font-size='72' fill='{palette[0]}' text-anchor='middle'>{subtitle}</text>
              <text x='900' y='2200' font-family='Helvetica, sans-serif' font-size='64' fill='{palette[0]}' text-anchor='middle'>by {author}</text>
            </svg>
            """
        ).strip()
