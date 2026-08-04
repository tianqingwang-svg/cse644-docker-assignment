"""
Unit tests for src/formatter.py
"""
import json
from src.formatter import format_currency, format_json_response


def test_format_currency():
    assert format_currency(1234.5) == "$1,234.50"
    assert format_currency(99.9, symbol="€") == "€99.90"


def test_format_json_response():
    data = {"b": 2, "a": 1}
    res = format_json_response(data)
    parsed = json.loads(res)
    assert parsed == data
