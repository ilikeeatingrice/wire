# The Wire Subtitle Index

This folder contains English subtitle files (SRT format) for all 5 seasons of The Wire (HBO), plus a search tool.

## Contents

- `Season_1/` through `Season_5/` — 62 `.srt` files, one per episode
- `index.json` — Pre-built flat index of all 55,332 subtitle lines across all seasons
- `search.py` — CLI search tool

## search.py Usage

```bash
python search.py "you come at the king"
python search.py omar --context 2
python search.py "it's all in the game" --context 3
python search.py McNulty --season 1
python search.py "stick up boys" --episode 4
python search.py --rebuild   # rebuild index.json from scratch
```

### Options
- `--context N` / `-c N` — show N lines before/after each match (same episode only)
- `--season N` / `-s N` — filter by season number
- `--episode N` / `-e N` — filter by episode number
- `--limit N` / `-l N` — max results to show (default 50)
- `--case-sensitive` — case-sensitive search
- `--rebuild` — regenerate index.json from SRT files

## index.json Schema

Each entry:
```json
{
  "season": 1,
  "episode": 8,
  "title": "Lessons",
  "start": "00:38:53,897",
  "end": "00:38:57,128",
  "text": "You come at the king, you best not miss."
}
```

## SRT Source

Downloaded from tvsubtitles.net (all seasons, English).
