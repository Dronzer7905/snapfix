"""
snapfix/llm/handler.py

Author: Snapfix Contributors
License: MIT

Snapfix LLM handler logic.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import litellm

from snapfix.config import SnapfixConfig
from snapfix.constants import LLM_MAX_TOKENS, LLM_TEMPERATURE
from snapfix.llm.prompts import (
    SYSTEM_PROMPT,
    build_user_prompt,
)

logger = logging.getLogger(__name__)

# Suppress litellm's verbose logging unless DEBUG is set
litellm.suppress_debug_info = True


class LLMHandler:
    """Async LLM client for Snapfix Engine."""

    def __init__(self, config: SnapfixConfig | None = None) -> None:
        # If config is None, we'll use a global load_config() call.
        from snapfix.config import load_config
        self._config = config or load_config()
        self._model = self._config.llm.model
        self._api_key = self._config.llm.api_key or None
        self._api_base = self._config.llm.api_base or None

    async def analyze(
        self,
        *,
        traceback: str,
        parsed_data: Any,
        project_path: str | None = None,
    ) -> dict[str, Any]:
        """Call the LLM and return the Snapfix JSON structure."""
        user_prompt = build_user_prompt(
            traceback=traceback,
            parsed_data=parsed_data,
            project_path=project_path,
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

        kwargs: dict[str, object] = {
            "model": self._model,
            "messages": messages,
            "max_tokens": LLM_MAX_TOKENS,
            "temperature": LLM_TEMPERATURE,
        }
        if self._api_key:
            kwargs["api_key"] = self._api_key
        if self._api_base:
            kwargs["api_base"] = self._api_base

        try:
            logger.debug("Calling Snapfix Engine model=%s", self._model)
            response = await litellm.acompletion(**kwargs)
            raw_content: str = response.choices[0].message.content or ""
        except Exception as exc:
            logger.error("Snapfix Engine call failed: %s", exc)
            raise RuntimeError(f"Snapfix Engine call failed: {exc}") from exc

        return self._parse_snapfix_response(raw_content)

    def _parse_snapfix_response(self, raw: str) -> dict[str, Any]:
        """Parse and validate the Snapfix JSON response."""
        cleaned = raw.strip()
        # Remove markdown code blocks if present
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            if lines[0].startswith("```json"):
                cleaned = "\n".join(lines[1:-1])
            else:
                cleaned = "\n".join(lines[1:-1])

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            logger.warning("Snapfix Engine returned invalid JSON. Using fallback.")
            return self._get_fallback_response(raw)

        # Basic validation of required fields
        required_sections = ["what_happened", "fix", "stack_frames", "prevention", "docs", "meta"]
        for section in required_sections:
            if section not in data:
                logger.warning(f"Snapfix response missing section: {section}")
                data[section] = {}

        return data

    def _get_fallback_response(self, raw: str) -> dict[str, Any]:
        return {
            "what_happened": {
                "headline": "Analysis failed",
                "detail": "The AI engine returned a malformed response."
            },
            "fix": {
                "explanation": "Review the traceback manually.",
                "code": f"# Raw output:\n# {raw}",
                "language": "python"
            },
            "stack_frames": [],
            "prevention": {
                "tip": "Check your local AI model configuration.",
                "pattern": ""
            },
            "docs": {"label": "Python docs", "url": "https://docs.python.org/3/"},
            "meta": {"severity": "low", "category": "other", "framework_hint": "", "confidence": "low"}
        }
