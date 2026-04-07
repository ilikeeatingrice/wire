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
(function(){
// --- Dropdown population ---
var seasons = {};
INDEX.forEach(function(e){
  if(!seasons[e.season]) seasons[e.season]=new Set();
  seasons[e.season].add(e.episode);
});
var seasonSel = document.getElementById('season');
var episodeSel = document.getElementById('episode');
Object.keys(seasons).sort(function(a,b){return a-b;}).forEach(function(s){
  var opt = document.createElement('option');
  opt.value = s; opt.textContent = 'Season '+s;
  seasonSel.appendChild(opt);
});

function populateEpisodes(season){
  episodeSel.innerHTML = '<option value="all">All</option>';
  if(season === 'all') return;
  var eps = [...seasons[season]].sort(function(a,b){return a-b;});
  eps.forEach(function(ep){
    var opt = document.createElement('option');
    opt.value = ep; opt.textContent = 'Episode '+ep;
    episodeSel.appendChild(opt);
  });
}
seasonSel.addEventListener('change', function(){ populateEpisodes(seasonSel.value); });

// --- Helpers ---
function escapeHtml(t){
  return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function highlight(text, pattern){
  // Build a global version of the pattern
  var gp = new RegExp(pattern.source, pattern.flags.replace('g','') + 'g');
  var result = '';
  var last = 0;
  var m;
  while((m = gp.exec(text)) !== null){
    result += escapeHtml(text.slice(last, m.index));
    result += '<mark>' + escapeHtml(m[0]) + '</mark>';
    last = gp.lastIndex;
    if(m[0].length === 0){ gp.lastIndex++; } // prevent infinite loop on zero-width match
  }
  result += escapeHtml(text.slice(last));
  return result;
}

// --- Search ---
function runSearch(){
  var query = document.getElementById('query').value.trim();
  if(!query) return;
  var caseSensitive = document.getElementById('case-sensitive').checked;
  var season = seasonSel.value;
  var episode = episodeSel.value;
  var ctxN = parseInt(document.getElementById('context').value, 10);

  var flags = caseSensitive ? '' : 'i';
  var pattern;
  try { pattern = new RegExp(query, flags); }
  catch(e){ pattern = new RegExp(query.replace(/[.*+?^${}()|[\\]\\\\]/g,'\\\\$&'), flags); }

  var pool = INDEX;
  if(season !== 'all') pool = pool.filter(function(e){ return e.season == season; });
  if(episode !== 'all') pool = pool.filter(function(e){ return e.episode == episode; });

  var matches = [];
  for(var i=0; i<pool.length; i++){
    if(!pattern.test(pool[i].text)) continue;
    var before=[], after=[];
    for(var j=Math.max(0,i-ctxN); j<i; j++){
      if(pool[j].season===pool[i].season && pool[j].episode===pool[i].episode) before.push(pool[j]);
    }
    for(var j=i+1; j<=Math.min(pool.length-1,i+ctxN); j++){
      if(pool[j].season===pool[i].season && pool[j].episode===pool[i].episode) after.push(pool[j]);
    }
    matches.push({match:pool[i], before:before, after:after});
  }

  renderResults(matches, pattern);
}

// --- Render ---
function pad(n){ return String(n).padStart(2,'0'); }

function renderResults(matches, pattern){
  var LIMIT = 50;
  var countEl = document.getElementById('count');
  var container = document.getElementById('results');

  if(matches.length === 0){
    countEl.textContent = 'No results found.';
    container.innerHTML = '';
    return;
  }

  var shown = matches.slice(0, LIMIT);
  countEl.textContent = matches.length > LIMIT
    ? 'Showing first 50 of '+matches.length+' results \u2014 refine your query to see fewer'
    : matches.length + (matches.length===1?' result':' results');

  container.innerHTML = shown.map(function(r){
    var m = r.match;
    var lbl = 'S'+pad(m.season)+'E'+pad(m.episode)+' \u2014 '+escapeHtml(m.title)
              +'&nbsp;&nbsp;['+m.start.replace(',','.')+' \u2192 '+m.end.replace(',','.')+']';
    var bef = r.before.map(function(c){ return '<div class="ctx">'+escapeHtml(c.text)+'</div>'; }).join('');
    var aft = r.after.map(function(c){ return '<div class="ctx">'+escapeHtml(c.text)+'</div>'; }).join('');
    return '<div class="result"><div class="ep-label">'+lbl+'</div>'
           +bef+'<div class="match-line">'+highlight(m.text, pattern)+'</div>'+aft+'</div>';
  }).join('');
}

// --- Events ---
document.getElementById('search-btn').addEventListener('click', runSearch);
document.getElementById('query').addEventListener('keydown', function(e){
  if(e.key==='Enter') runSearch();
});
})();
</script>
</body>
</html>"""


def build_html(index_data):
    """Return the complete HTML string with index_data embedded."""
    json_str = json.dumps(index_data, ensure_ascii=False, separators=(",", ":"))
    return HTML_TEMPLATE.replace("__INDEX__", json_str)


def main():
    try:
        with open(INDEX_FILE, encoding="utf-8") as f:
            index_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: index.json not found at {INDEX_FILE}")
        print("Run: python search.py --rebuild")
        return
    except json.JSONDecodeError as e:
        print(f"Error: index.json is malformed: {e}")
        return
    html = build_html(index_data)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    size_mb = os.path.getsize(OUTPUT_FILE) / 1_000_000
    print(f"Built {OUTPUT_FILE} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
