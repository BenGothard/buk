from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from .cover import CoverBuilder
from .manuscript import ManuscriptBuilder
from .metadata import MetadataBuilder
from .models import BookIdea, BookAssets


class BookWorkflow:
    def __init__(self, idea: BookIdea, output_dir: Path = Path("output")) -> None:
        self.idea = idea
        self.output_dir = output_dir

    def run(self) -> BookAssets:
        metadata = MetadataBuilder(self.idea).build()
        manuscript = ManuscriptBuilder(self.idea).build()
        cover = CoverBuilder(self.idea, metadata).build()
        assets = BookAssets(metadata=metadata, manuscript=manuscript, cover=cover)
        assets.export(self.output_dir)
        return assets

    def describe(self) -> str:
        summary = {
            "idea": asdict(self.idea),
            "output_directory": str(self.output_dir.resolve()),
        }
        return json.dumps(summary, indent=2)


def build_from_cli_args(**kwargs) -> BookWorkflow:
    idea = BookIdea(**kwargs)
    return BookWorkflow(idea=idea, output_dir=Path(kwargs.get("output_dir", "output")))
