from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import List, Dict


@dataclass
class BookIdea:
    idea: str
    genre: str = "general nonfiction"
    audience: str = "broad audience"
    tone: str = "friendly and encouraging"
    language: str = "English"
    author: str | None = None
    target_word_count: int = 12000
    chapter_count: int = 8
    keywords: List[str] | None = None
    subtitle: str | None = None

    def normalized_keywords(self) -> List[str]:
        keywords = self.keywords or []
        extra = [self.genre, self.audience]
        return [kw.strip() for kw in keywords + extra if kw.strip()]


@dataclass
class GeneratedMetadata:
    title: str
    subtitle: str
    description: str
    keywords: List[str]
    categories: List[str]
    pricing_suggestion: str
    language: str
    author: str
    created_on: date = field(default_factory=date.today)

    def to_dict(self) -> Dict[str, str | List[str]]:
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "description": self.description,
            "keywords": self.keywords,
            "categories": self.categories,
            "pricing_suggestion": self.pricing_suggestion,
            "language": self.language,
            "author": self.author,
            "created_on": self.created_on.isoformat(),
        }


@dataclass
class Manuscript:
    outline: List[str]
    body: str

    def write(self, path: Path) -> None:
        path.write_text(self.body, encoding="utf-8")


@dataclass
class CoverArt:
    svg_content: str

    def write(self, path: Path) -> None:
        path.write_text(self.svg_content, encoding="utf-8")


@dataclass
class BookAssets:
    metadata: GeneratedMetadata
    manuscript: Manuscript
    cover: CoverArt

    def export(self, out_dir: Path) -> None:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "metadata.json").write_text(
            _json_dumps(self.metadata.to_dict()), encoding="utf-8"
        )
        self.manuscript.write(out_dir / "manuscript.md")
        self.cover.write(out_dir / "cover.svg")


def _json_dumps(payload: Dict[str, str | List[str]]) -> str:
    import json

    return json.dumps(payload, indent=2, ensure_ascii=False)
