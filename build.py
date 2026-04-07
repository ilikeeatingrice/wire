#!/usr/bin/env python3
"""Generate wire-search.html from index.json."""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(BASE_DIR, "index.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "wire-search.html")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The Wire — Subtitle Search</title>
</head>
<body>
<script>const INDEX=__INDEX__;</script>
</body>
</html>"""


def build_html(index_data):
    """Return the complete HTML string with index_data embedded."""
    json_str = json.dumps(index_data, ensure_ascii=False, separators=(",", ":"))
    return HTML_TEMPLATE.replace("__INDEX__", json_str)


def main():
    with open(INDEX_FILE, encoding="utf-8") as f:
        index_data = json.load(f)
    html = build_html(index_data)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    size_mb = os.path.getsize(OUTPUT_FILE) / 1_000_000
    print(f"Built {OUTPUT_FILE} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
