# The Wire Subtitle Search

Search all dialogue from all 5 seasons of The Wire (HBO, 2002–2008).

## Quick Start

Download [`wire-search.html`](wire-search.html) and open it in any browser. No install required.

## Features

- Full-text search across 55,332 subtitle lines
- Filter by season and episode
- Show surrounding context lines
- Case-sensitive mode
- Regex support (falls back to literal on invalid pattern)
- Results highlight matched text

## For Developers

Subtitles are stored as SRT files in `Season_1/` through `Season_5/`. The pre-built index is at `index.json`.

**CLI search:**
```bash
python search.py "you come at the king"
python search.py omar --context 2 --season 1
python search.py --rebuild   # regenerate index.json from SRT files
```

**Rebuild the HTML:**
```bash
python build.py   # generates wire-search.html
```

## License

MIT © 2026 ilikeeatingrice
