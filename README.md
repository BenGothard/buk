# Buk Maker

Generate a Kindle Direct Publishing–ready bundle from a single book idea. The CLI turns a short prompt into:

- A structured manuscript in Markdown with chapter headings and reader takeaways.
- A simple, clean cover as an SVG file sized for KDP uploads.
- SEO-focused metadata (title, subtitle, description, keywords, categories, pricing suggestion) in JSON.

Everything runs locally with no external dependencies or API keys.

## Quick start

1. Make sure you have Python 3.11+ installed.
2. Run the generator with your idea:

```bash
python -m bookgen "Tiny Habits for Remote Workers" \
  --genre "business" \
  --audience "remote teams" \
  --tone "supportive and concise" \
  --keywords "remote work" "productivity" "habits" \
  --output-dir "output/demo"
```

3. Open the generated files:
   - `output/demo/manuscript.md`: ready to paste into KDP or export to DOCX/PDF.
   - `output/demo/cover.svg`: upload-ready cover that you can tweak or convert to PNG/JPEG.
   - `output/demo/metadata.json`: SEO title, subtitle, description, keywords, categories, and pricing guidance.

The CLI prints a summary with file paths after generation.

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `idea` (positional) | Short description of your book concept | _required_ |
| `--genre` | Genre or category string | `general nonfiction` |
| `--audience` | Target reader | `busy professionals` |
| `--tone` | Voice or tone for the manuscript | `friendly and encouraging` |
| `--language` | Manuscript language | `English` |
| `--author` | Author name for metadata and cover | `Anonymous Creator` |
| `--chapter-count` | Number of chapters to generate (up to 8 templates) | `8` |
| `--target-word-count` | Intended total word count for pricing guidance | `12000` |
| `--subtitle` | Custom subtitle override | auto-generated |
| `--keywords` | Extra SEO keyword phrases | `[]` |
| `--output-dir` | Destination folder for all assets | `output` |

## What gets generated

- **Manuscript:** Front matter plus templated chapters with Kindle-friendly formatting cues.
- **Cover:** Lightweight SVG with title, subtitle, and author—easy to customize further in a vector editor.
- **Metadata:** JSON payload you can paste into KDP including categories and pricing suggestion.

## Development

The project uses only the Python standard library. To iterate locally:

```bash
python -m bookgen "Your Idea Here"
```

Edit modules under `bookgen/` to adjust templates, metadata heuristics, or cover styling.
