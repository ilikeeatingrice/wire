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
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Wire — Subtitle Search</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,sans-serif;font-size:14px;color:#111;background:#fff;max-width:720px;margin:40px auto;padding:0 20px}
.label-sub{font-size:11px;color:#aaa;letter-spacing:.05em;text-transform:uppercase;margin-bottom:6px}
h1{font-size:1.25rem;font-weight:600;margin-bottom:24px}
.search-row{display:flex;gap:8px;margin-bottom:10px}
#query{flex:1;padding:7px 10px;border:1px solid #ccc;font-size:14px;outline:none}
#query:focus{border-color:#888}
button{padding:7px 18px;background:#111;color:#fff;border:none;cursor:pointer;font-size:14px}
button:hover{background:#333}
.filter-row{display:flex;flex-wrap:wrap;gap:16px;align-items:center;margin-bottom:20px;font-size:13px;color:#444}
.filter-row label{display:flex;align-items:center;gap:6px}
select{padding:4px 6px;border:1px solid #ccc;font-size:13px;background:#fff}
#count{font-size:12px;color:#888;margin-bottom:14px;min-height:16px}
#results{}
.result{padding:10px 0;border-top:1px solid #eee}
#results .result:first-child{border-top:none}
.ep-label{font-family:monospace;font-size:11px;color:#aaa;margin-bottom:5px}
.match-line{color:#111;line-height:1.5}
.ctx{color:#bbb;font-size:13px;line-height:1.5}
mark{background:#ff0;padding:0 1px}
</style>
</head>
<body>
<div class="label-sub">HBO · 2002–2008</div>
<h1>The Wire — Subtitle Search</h1>
<div class="search-row">
  <input type="text" id="query" placeholder="Search dialogue…" autocomplete="off" autocorrect="off" spellcheck="false">
  <button id="search-btn">Search</button>
</div>
<div class="filter-row">
  <label>Season <select id="season"><option value="all">All</option></select></label>
  <label>Episode <select id="episode"><option value="all">All</option></select></label>
  <label>Context <select id="context">
    <option value="0">0</option><option value="1">1</option><option value="2">2</option>
    <option value="3">3</option><option value="4">4</option><option value="5">5</option>
  </select> lines</label>
  <label><input type="checkbox" id="case-sensitive"> Case-sensitive</label>
</div>
<div id="count"></div>
<div id="results"></div>
<script>const INDEX=__INDEX__;</script>
<script>
// populated by JS in Task 3
</script>
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
