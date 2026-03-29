"""
snapfix/parser/frameworks.py

Author: Snapfix Contributors
License: MIT

FrameworkDetector: identifies the Python web framework (or plain Python)
from traceback text by scanning for well-known path fingerprints.
"""

from __future__ import annotations

from snapfix.constants import (
    FRAMEWORK_DJANGO,
    FRAMEWORK_FASTAPI,
    FRAMEWORK_FLASK,
    FRAMEWORK_PATH_HINTS,
    FRAMEWORK_PYTHON,
)


class FrameworkDetector:
    """Detects the web framework context from traceback text.

    Scans each line of the traceback for known ``site-packages`` paths
    associated with Django, Flask, and FastAPI.
    """

    _PRIORITY_ORDER: list[str] = [
        FRAMEWORK_FASTAPI,
        FRAMEWORK_FLASK,
        FRAMEWORK_DJANGO,
    ]

    def detect(self, traceback_text: str) -> str:
        """Detect the framework from raw traceback text."""
        lower = traceback_text.lower()
        for framework in self._PRIORITY_ORDER:
            hints = FRAMEWORK_PATH_HINTS.get(framework, [])
            if any(hint.lower() in lower for hint in hints):
                return framework
        return FRAMEWORK_PYTHON

    def detect_with_confidence(self, traceback_text: str) -> dict[str, float]:
        """Return a confidence score (0–1) for each framework."""
        lower = traceback_text.lower()
        scores: dict[str, float] = {}
        for framework, hints in FRAMEWORK_PATH_HINTS.items():
            matched = sum(1 for h in hints if h.lower() in lower)
            scores[framework] = matched / max(len(hints), 1)
        scores[FRAMEWORK_PYTHON] = 0.0
        return scores
