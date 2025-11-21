from __future__ import annotations

import argparse
import json
from pathlib import Path

from .workflow import BookWorkflow
from .models import BookIdea


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Kindle-ready manuscript, cover, and SEO metadata from a simple idea.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("idea", help="Short description of the book idea")
    parser.add_argument("--genre", default="general nonfiction", help="Genre or category")
    parser.add_argument("--audience", default="busy professionals", help="Target reader")
    parser.add_argument("--tone", default="friendly and encouraging", help="Voice or tone")
    parser.add_argument("--language", default="English")
    parser.add_argument("--author", default="Anonymous Creator", help="Author name")
    parser.add_argument("--chapter-count", type=int, default=8, dest="chapter_count")
    parser.add_argument("--target-word-count", type=int, default=12000, dest="target_word_count")
    parser.add_argument("--subtitle", help="Custom subtitle override")
    parser.add_argument(
        "--keywords",
        nargs="*",
        default=[],
        help="Additional SEO keywords separated by spaces. Use quotes for multi-word phrases.",
    )
    parser.add_argument("--output-dir", default="output", dest="output_dir", help="Folder to write generated assets")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    idea = BookIdea(
        idea=args.idea,
        genre=args.genre,
        audience=args.audience,
        tone=args.tone,
        language=args.language,
        author=args.author,
        chapter_count=args.chapter_count,
        target_word_count=args.target_word_count,
        subtitle=args.subtitle,
        keywords=args.keywords,
    )
    workflow = BookWorkflow(idea=idea, output_dir=Path(args.output_dir))
    assets = workflow.run()

    summary = {
        "metadata": assets.metadata.to_dict(),
        "manuscript_path": str(Path(args.output_dir) / "manuscript.md"),
        "cover_path": str(Path(args.output_dir) / "cover.svg"),
        "metadata_path": str(Path(args.output_dir) / "metadata.json"),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
