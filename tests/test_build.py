import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import build

MOCK_INDEX = [
    {"season": 1, "episode": 3, "title": "The Buys", "start": "00:38:53,897", "end": "00:38:57,128", "text": "You come at the king, you best not miss."},
    {"season": 1, "episode": 3, "title": "The Buys", "start": "00:39:00,000", "end": "00:39:02,000", "text": "That's the game."},
    {"season": 2, "episode": 1, "title": "Ebb Tide", "start": "00:01:00,000", "end": "00:01:02,000", "text": "It's all in the game."},
]

def test_build_html_returns_string():
    html = build.build_html(MOCK_INDEX)
    assert isinstance(html, str)

def test_build_html_is_valid_html():
    html = build.build_html(MOCK_INDEX)
    assert html.startswith("<!DOCTYPE html>")

def test_build_html_embeds_index():
    html = build.build_html(MOCK_INDEX)
    assert "You come at the king" in html

def test_build_html_contains_const_index():
    html = build.build_html(MOCK_INDEX)
    assert "constINDEX=" in html.replace(" ", "").replace("\n", "")

def test_build_html_has_search_input():
    html = build.build_html(MOCK_INDEX)
    assert 'id="query"' in html

def test_build_html_has_season_select():
    html = build.build_html(MOCK_INDEX)
    assert 'id="season"' in html

def test_build_html_has_episode_select():
    html = build.build_html(MOCK_INDEX)
    assert 'id="episode"' in html

def test_build_html_has_context_select():
    html = build.build_html(MOCK_INDEX)
    assert 'id="context"' in html

def test_build_html_has_search_function():
    html = build.build_html(MOCK_INDEX)
    assert "function runSearch()" in html

def test_build_html_has_highlight_function():
    html = build.build_html(MOCK_INDEX)
    assert "function highlight(" in html

def test_build_html_has_escape_function():
    html = build.build_html(MOCK_INDEX)
    assert "function escapeHtml(" in html
