#!/usr/bin/env python3
"""
The Wire - Searchable Subtitle Index
Usage: python search.py <query>
       python search.py "you come at the king"
       python search.py omar --context 2
"""

import os
import re
import sys
import json
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(BASE_DIR, "index.json")


def parse_srt(filepath):
    """Parse an SRT file into a list of subtitle entries."""
    entries = []
    with open(filepath, encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Split on blank lines between subtitle blocks
    blocks = re.split(r"\n\n+", content.strip())
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        # Line 0: index number
        # Line 1: timestamp
        # Line 2+: text
        ts_match = re.match(
            r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})", lines[1]
        )
        if not ts_match:
            continue
        text = " ".join(lines[2:]).strip()
        text = re.sub(r"<[^>]+>", "", text)  # strip HTML tags like <i>
        entries.append({
            "start": ts_match.group(1),
            "end": ts_match.group(2),
            "text": text,
        })
    return entries


def build_index():
    """Build index from all SRT files and save to index.json."""
    index = []
    for season_num in range(1, 6):
        season_dir = os.path.join(BASE_DIR, f"Season_{season_num}")
        if not os.path.isdir(season_dir):
            continue
        for fname in sorted(os.listdir(season_dir)):
            if not fname.endswith(".srt"):
                continue
            # Parse episode info from filename e.g. "The Wire - 2x05 - Undertow.en.srt"
            ep_match = re.search(r"(\d+)x(\d+)\s*-\s*(.+?)(?:\.\w+)?\.srt$", fname, re.IGNORECASE)
            if not ep_match:
                continue
            season = int(ep_match.group(1))
            episode = int(ep_match.group(2))
            title = ep_match.group(3).strip()

            filepath = os.path.join(season_dir, fname)
            entries = parse_srt(filepath)
            for entry in entries:
                index.append({
                    "season": season,
                    "episode": episode,
                    "title": title,
                    "start": entry["start"],
                    "end": entry["end"],
                    "text": entry["text"],
                })

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False)
    print(f"Index built: {len(index):,} lines across all 5 seasons -> {INDEX_FILE}")
    return index


def load_index():
    """Load index from file, building it first if needed."""
    if not os.path.exists(INDEX_FILE):
        print("Building index for the first time...")
        return build_index()
    with open(INDEX_FILE, encoding="utf-8") as f:
        return json.load(f)


def search(query, index, context=0, case_sensitive=False):
    """Search the index for lines matching query."""
    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        pattern = re.compile(query, flags)
    except re.error:
        # Fall back to literal search if not valid regex
        pattern = re.compile(re.escape(query), flags)

    results = []
    for i, entry in enumerate(index):
        if pattern.search(entry["text"]):
            result = {"match": entry, "context_before": [], "context_after": []}
            if context > 0:
                # Context: same episode only
                for j in range(max(0, i - context), i):
                    if (index[j]["season"] == entry["season"] and
                            index[j]["episode"] == entry["episode"]):
                        result["context_before"].append(index[j])
                for j in range(i + 1, min(len(index), i + context + 1)):
                    if (index[j]["season"] == entry["season"] and
                            index[j]["episode"] == entry["episode"]):
                        result["context_after"].append(index[j])
            results.append(result)
    return results


def format_results(results, show_context=False):
    """Pretty-print search results."""
    if not results:
        print("No results found.")
        return

    print(f"\n{len(results)} result(s) found:\n")
    print("=" * 70)

    for r in results:
        m = r["match"]
        header = f"S{m['season']:02d}E{m['episode']:02d} - {m['title']}  [{m['start']} --> {m['end']}]"
        print(header)

        if show_context and r["context_before"]:
            for c in r["context_before"]:
                print(f"  {c['text']}")

        print(f"  >>> {m['text']}")

        if show_context and r["context_after"]:
            for c in r["context_after"]:
                print(f"  {c['text']}")

        print("-" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Search The Wire subtitles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python search.py "you come at the king"
  python search.py omar --context 2
  python search.py "it's all in the game" --context 3
  python search.py McNulty --season 1
  python search.py "stick up boys" --episode 4
  python search.py --rebuild
        """
    )
    parser.add_argument("query", nargs="?", help="Search query (supports regex)")
    parser.add_argument("--context", "-c", type=int, default=0,
                        help="Lines of context to show before/after match")
    parser.add_argument("--season", "-s", type=int, help="Filter by season number")
    parser.add_argument("--episode", "-e", type=int, help="Filter by episode number")
    parser.add_argument("--case-sensitive", action="store_true", help="Case-sensitive search")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the index")
    parser.add_argument("--limit", "-l", type=int, default=50,
                        help="Max results to show (default: 50)")

    args = parser.parse_args()

    if args.rebuild:
        build_index()
        if not args.query:
            return

    if not args.query:
        parser.print_help()
        return

    index = load_index()

    # Filter by season/episode
    if args.season:
        index = [e for e in index if e["season"] == args.season]
    if args.episode:
        index = [e for e in index if e["episode"] == args.episode]

    results = search(args.query, index, context=args.context,
                     case_sensitive=args.case_sensitive)

    if len(results) > args.limit:
        print(f"(Showing first {args.limit} of {len(results)} results. Use --limit to see more.)")
        results = results[:args.limit]

    format_results(results, show_context=args.context > 0)


if __name__ == "__main__":
    main()
