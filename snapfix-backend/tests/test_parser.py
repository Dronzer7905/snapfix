"""
snapfix/tests/test_parser.py

Author: Snapfix Contributors
License: MIT

Parametrized unit tests for TracebackParser and FrameworkDetector.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from snapfix.parser.frameworks import FrameworkDetector
from snapfix.parser.traceback import TracebackParser

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    """Load a traceback fixture file by name."""
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


class TestTracebackParser:
    """Tests for the stateless TracebackParser class."""

    def setup_method(self) -> None:
        self.parser = TracebackParser()

    @pytest.mark.parametrize(
        "fixture_file, expected_error_type, expected_file_substr, expected_line",
        [
            ("plain_zero_division.txt", "ZeroDivisionError", "main.py", 5),
            ("plain_index_error.txt", "IndexError", "app.py", 12),
            ("flask_key_error.txt", "KeyError", "app.py", 28),
            ("fastapi_value_error.txt", "ValueError", "items.py", 55),
            ("django_does_not_exist.txt", "DoesNotExist", "views.py", 42),
        ],
    )
    def test_parse_returns_correct_error_type(
        self,
        fixture_file: str,
        expected_error_type: str,
        expected_file_substr: str,
        expected_line: int,
    ) -> None:
        raw = load_fixture(fixture_file)
        result = self.parser.parse(raw)
        assert result is not None
        assert expected_error_type in result.error_type

    def test_traceback_hash_is_deterministic(self) -> None:
        raw = load_fixture("plain_zero_division.txt")
        r1 = self.parser.parse(raw)
        r2 = self.parser.parse(raw)
        assert r1.traceback_hash == r2.traceback_hash


class TestFrameworkDetector:
    """Tests for the FrameworkDetector class."""

    def setup_method(self) -> None:
        self.detector = FrameworkDetector()

    @pytest.mark.parametrize(
        "fixture_file, expected_framework",
        [
            ("django_does_not_exist.txt", "django"),
            ("fastapi_value_error.txt", "fastapi"),
        ],
    )
    def test_detect_correct_framework(
        self, fixture_file: str, expected_framework: str
    ) -> None:
        raw = load_fixture(fixture_file)
        result = self.detector.detect(raw)
        assert result == expected_framework
