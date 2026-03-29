"""
snapfix/parser/traceback.py

Author: Snapfix Contributors
License: MIT

TracebackParser: regex-based extractor that converts raw Python traceback
text into a structured ParsedTraceback dataclass.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from snapfix.constants import (
    ERROR_LINE_PATTERN,
    FRAME_PATTERN,
    GENERIC_ERROR_PATTERN,
    HASH_ALGORITHM,
    TRACEBACK_HEADER,
)


@dataclass
class TracebackFrame:
    """A single stack frame extracted from a Python traceback."""
    file_path: str
    line_number: int
    func_name: str
    source_line: str = ""


@dataclass
class ParsedTraceback:
    """Structured representation of a Python traceback."""
    error_type: str
    error_message: str
    frames: list[TracebackFrame] = field(default_factory=list)
    file_path: str = ""
    line_number: int = 0
    raw: str = ""
    traceback_hash: str = ""


class TracebackParser:
    """Parses raw Python traceback text into a :class:`ParsedTraceback`."""

    _frame_re: re.Pattern[str] = re.compile(FRAME_PATTERN, re.MULTILINE)
    _error_re: re.Pattern[str] = re.compile(ERROR_LINE_PATTERN, re.MULTILINE)
    _generic_re: re.Pattern[str] = re.compile(GENERIC_ERROR_PATTERN, re.MULTILINE)

    def parse(self, raw: str) -> ParsedTraceback | None:
        """Parse a raw traceback string."""
        if TRACEBACK_HEADER not in raw and not self._error_re.search(raw):
            return None

        frames = self._extract_frames(raw)
        error_type, error_message = self._extract_error(raw)

        innermost = frames[-1] if frames else None
        file_path = innermost.file_path if innermost else ""
        line_number = innermost.line_number if innermost else 0

        normalised = self.normalize(raw)
        tb_hash = hashlib.new(HASH_ALGORITHM, normalised.encode()).hexdigest()

        return ParsedTraceback(
            error_type=error_type,
            error_message=error_message,
            frames=frames,
            file_path=file_path,
            line_number=line_number,
            raw=raw,
            traceback_hash=tb_hash,
        )

    def normalize(self, raw: str) -> str:
        """Normalise a traceback for stable cache key generation."""
        text = re.sub(r"0x[0-9a-fA-F]+", "0xADDR", raw)
        text = "\n".join(line.rstrip() for line in text.splitlines())
        return text.strip()

    def _extract_frames(self, raw: str) -> list[TracebackFrame]:
        frames: list[TracebackFrame] = []
        lines = raw.splitlines()

        i = 0
        while i < len(lines):
            m = self._frame_re.match(lines[i])
            if m:
                file_path, lineno, func = m.group(1), int(m.group(2)), m.group(3)
                source_line = ""
                if i + 1 < len(lines) and lines[i + 1].startswith("    "):
                    source_line = lines[i + 1].strip()
                    i += 1
                frames.append(
                    TracebackFrame(
                        file_path=file_path,
                        line_number=lineno,
                        func_name=func,
                        source_line=source_line,
                    )
                )
            i += 1

        return frames

    def _extract_error(self, raw: str) -> tuple[str, str]:
        matches = list(self._error_re.finditer(raw))
        if not matches:
            matches = list(self._generic_re.finditer(raw))
        if matches:
            last = matches[-1]
            return last.group(1), last.group(2).strip()
        return "UnknownError", ""
