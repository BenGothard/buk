from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent
from typing import List

from .models import BookIdea, Manuscript


@dataclass
class ManuscriptBuilder:
    idea: BookIdea

    def build(self) -> Manuscript:
        outline = self._outline()
        body = self._body_from_outline(outline)
        return Manuscript(outline=outline, body=body)

    def _outline(self) -> List[str]:
        base_sections = [
            "Introduction",
            "Vision & Reader Promise",
            "Core Concepts",
            "Practical Steps",
            "Case Study",
            "Common Pitfalls",
            "Action Plan",
            "Summary & Next Steps",
        ]
        chapters = base_sections[: self.idea.chapter_count]
        return chapters

    def _body_from_outline(self, outline: List[str]) -> str:
        sections = [self._chapter_text(title, idx + 1) for idx, title in enumerate(outline)]
        front_matter = self._front_matter()
        return "\n\n".join([front_matter] + sections)

    def _front_matter(self) -> str:
        intro = dedent(
            f"""
            # {self.idea.idea.title()}
            
            *A {self.idea.genre} book for {self.idea.audience} written in a {self.idea.tone} voice.*
            
            This manuscript was generated to be Kindle Direct Publishing ready. It includes reader-friendly pacing, short paragraphs, and end-of-chapter recaps so your audience can apply ideas right away.
            """
        ).strip()
        return intro

    def _chapter_text(self, title: str, number: int) -> str:
        recap = "Key Takeaways:\n- Highlight the main idea.\n- Offer one actionable step.\n- Invite the reader to continue."
        content = dedent(
            f"""
            ## Chapter {number}: {title}
            
            {self._paragraph(1)}
            
            {self._paragraph(2)}
            
            {self._paragraph(3)}
            
            {recap}
            """
        ).strip()
        return content

    def _paragraph(self, seed: int) -> str:
        templates = [
            "This chapter explores {idea} through the lens of {tone}, giving readers clarity on why it matters now.",
            "Practical prompts encourage the {audience} to try small experiments, tracking progress in a simple worksheet.",
            "Each section includes KDP-friendly headings, short sentences, and direct language to keep readers engaged.",
        ]
        chosen = templates[seed % len(templates)]
        return chosen.format(idea=self.idea.idea, audience=self.idea.audience, tone=self.idea.tone)
