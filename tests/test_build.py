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
