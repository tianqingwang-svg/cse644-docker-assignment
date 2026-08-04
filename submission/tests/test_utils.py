"""
Unit tests for src/utils.py
"""
from src.utils import is_valid_email, clamp


def test_is_valid_email():
    assert is_valid_email("user@example.com") is True
    assert is_valid_email("invalid-email") is False
    assert is_valid_email("@no-user.com") is False


def test_clamp():
    assert clamp(5, 0, 10) == 5
    assert clamp(-5, 0, 10) == 0
    assert clamp(15, 0, 10) == 10
