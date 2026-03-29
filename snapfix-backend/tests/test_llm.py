"""
snapfix/tests/test_llm.py

Author: Snapfix Contributors
License: MIT

Tests for the LLMHandler and prompt generation logic.
"""

from __future__ import annotations

import pytest

from snapfix.config import SnapfixConfig, LLMConfig
from snapfix.llm.handler import LLMHandler
from snapfix.llm.prompts import build_user_prompt


def test_build_user_prompt_contains_traceback() -> None:
    """The generated prompt must include the raw traceback and exception info."""
    class MockParsed:
        error_type = "ZeroDivisionError"
        error_message = "division by zero"
        file_path = "main.py"
        line_number = 5

    raw_tb = "Traceback (most recent call last):\n  File \"main.py\", line 5\nZeroDivisionError"
    prompt = build_user_prompt(
        traceback=raw_tb,
        parsed_data=MockParsed(),
        project_path="/home/user/project",
    )
    
    assert "ZeroDivisionError" in prompt
    assert "division by zero" in prompt
    assert "main.py:5" in prompt


class TestLLMHandler:
    """Tests for the LLMHandler class (mostly configuration-based)."""

    def test_handler_initializes_with_config(self) -> None:
        cfg = SnapfixConfig(
            llm=LLMConfig(model="gpt-4", api_key="sk-test", api_base="https://api.openai.com/v1")
        )
        handler = LLMHandler(cfg)
        assert handler._model == "gpt-4"
        assert handler._api_key == "sk-test"
        assert handler._api_base == "https://api.openai.com/v1"
