from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterable, List

from .models import BookIdea, GeneratedMetadata


ADJECTIVES = ["ultimate", "essential", "friendly", "fast", "practical"]
PUBLISHING_CATEGORIES = {
    "general nonfiction": ["Nonfiction", "Self-Help"],
    "business": ["Business & Money", "Entrepreneurship"],
    "fantasy": ["Fantasy", "Adventure"],
    "sci-fi": ["Science Fiction", "Technology"],
    "children": ["Children's Books", "Education"],
}


@dataclass
class MetadataBuilder:
    idea: BookIdea

    def build(self) -> GeneratedMetadata:
        title = self._seo_title()
        subtitle = self._subtitle()
        description = self._description(title, subtitle)
        keywords = self._keywords()
        categories = PUBLISHING_CATEGORIES.get(self.idea.genre, [self.idea.genre.title()])
        pricing_suggestion = self._pricing_suggestion()
        author = self.idea.author or "Anonymous Creator"

        return GeneratedMetadata(
            title=title,
            subtitle=subtitle,
            description=description,
            keywords=keywords,
            categories=categories,
            pricing_suggestion=pricing_suggestion,
            language=self.idea.language,
            author=author,
        )

    def _seo_title(self) -> str:
        base = self.idea.idea.strip().rstrip(".")
        adjective = ADJECTIVES[len(base) % len(ADJECTIVES)].title()
        return f"The {adjective} Guide to {base.title()}"

    def _subtitle(self) -> str:
        if self.idea.subtitle:
            return self.idea.subtitle
        return f"{self.idea.genre.title()} Strategies for {self.idea.audience.title()}"

    def _description(self, title: str, subtitle: str) -> str:
        paragraphs = [
            f"{title}: {subtitle} combines approachable storytelling with actionable guidance to turn the idea of '{self.idea.idea}' into a publish-ready experience.",
            "Inside you'll find concise chapters, worksheets, and reader-friendly summaries that make it easy to apply what you learn immediately.",
            "Formatted with Kindle Direct Publishing best practices, each section is optimized for readability on mobile and e-ink devices.",
        ]
        return "\n\n".join(paragraphs)

    def _keywords(self) -> List[str]:
        base_keywords = [
            self.idea.genre,
            self.idea.audience,
            self.idea.tone,
            self.idea.idea,
        ]
        combined = self.idea.normalized_keywords() + base_keywords
        return _unique_keywords(combined)[:7]

    def _pricing_suggestion(self) -> str:
        word_count = max(self.idea.target_word_count, 3000)
        bucket = "short guide" if word_count < 10000 else "full-length handbook"
        return f"${self._price_for_words(word_count):.2f} ({bucket})"

    @staticmethod
    def _price_for_words(word_count: int) -> float:
        # Simple heuristic: $2.99 minimum, add $1 per 8k words
        return max(2.99, 2.99 + (word_count // 8000))


def _unique_keywords(candidates: Iterable[str]) -> List[str]:
    flattened = itertools.chain.from_iterable(
        (kw.lower().strip().replace("  ", " ").split(",") for kw in candidates)
    )
    cleaned = []
    for kw in flattened:
        normalized = kw.strip()
        if normalized and normalized not in cleaned:
            cleaned.append(normalized)
    return cleaned
