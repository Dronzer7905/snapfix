"""
pylogai/constants.py

Author: Snapfix Contributors
License: MIT

Central constants for Snapfix Engine.
"""

from pathlib import Path

# ── Server ────────────────────────────────────────────────────────────────────
DEFAULT_HOST: str = "127.0.0.1"
DEFAULT_PORT: int = 7842
HEALTH_ENDPOINT: str = "/health"
ANALYZE_ENDPOINT: str = "/analyze"
SERVER_STARTUP_TIMEOUT_S: int = 15

# ── File system ───────────────────────────────────────────────────────────────
# We'll rename the config directory to .snapfix for better branding
PYLOGAI_DIR: Path = Path.home() / ".snapfix"
CONFIG_PATH: Path = PYLOGAI_DIR / "config.toml"
CACHE_DB_PATH: Path = PYLOGAI_DIR / "cache.db"

# ── LLM defaults ──────────────────────────────────────────────────────────────
DEFAULT_LLM_PROVIDER: str = "gemini"
DEFAULT_LLM_MODEL: str = "gemini/gemma-3-27b-it"
DEFAULT_LLM_API_BASE: str = ""
LLM_MAX_TOKENS: int = 2048
LLM_TEMPERATURE: float = 0.1

# ── Hashing ───────────────────────────────────────────────────────────────────
HASH_ALGORITHM: str = "sha256"
HASH_HEX_LENGTH: int = 64

# ── Frameworks ────────────────────────────────────────────────────────────────
FRAMEWORK_DJANGO: str = "django"
FRAMEWORK_FLASK: str = "flask"
FRAMEWORK_FASTAPI: str = "fastapi"
FRAMEWORK_PYTHON: str = "python"

FRAMEWORK_PATH_HINTS: dict[str, list[str]] = {
    FRAMEWORK_DJANGO: ["django/", "django\\", "site-packages/django"],
    FRAMEWORK_FLASK: ["flask/", "flask\\", "site-packages/flask"],
    FRAMEWORK_FASTAPI: ["fastapi/", "fastapi\\", "site-packages/fastapi", "starlette/"],
}

# ── Traceback parsing ─────────────────────────────────────────────────────────
TRACEBACK_HEADER: str = "Traceback (most recent call last):"
FRAME_PATTERN: str = r'^\s+File "(.+)", line (\d+), in (.+)$'
ERROR_LINE_PATTERN: str = r'^([A-Za-z][A-Za-z0-9_.]*(?:Error|Exception|Warning|Interrupt|Exit|Fault|Abort|Stop|GeneratorExit|KeyboardInterrupt|SystemExit))\s*:\s*(.*)$'
GENERIC_ERROR_PATTERN: str = r'^([A-Z][A-Za-z0-9_.]+):\s+(.+)$'

# ── Cache ─────────────────────────────────────────────────────────────────────
CACHE_ENABLED_DEFAULT: bool = True
AUTO_ANALYZE_DEFAULT: bool = True

# ── CLI ───────────────────────────────────────────────────────────────────────
APP_NAME: str = "snapfix"
APP_VERSION: str = "0.2.0"
