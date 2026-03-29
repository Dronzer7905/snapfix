"""
snapfix/config.py

Author: Snapfix Contributors
License: MIT

TOML-based configuration loader for Snapfix Engine.
Creates default config if none exists at ~/.snapfix/config.toml.
"""

from __future__ import annotations

import toml
from pathlib import Path
from pydantic import BaseModel, Field

from snapfix.constants import (
    CONFIG_PATH,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_LLM_PROVIDER,
    DEFAULT_LLM_MODEL,
    DEFAULT_LLM_API_BASE,
    CACHE_ENABLED_DEFAULT,
    AUTO_ANALYZE_DEFAULT,
    PYLOGAI_DIR,
)


# ── Pydantic config models ────────────────────────────────────────────────────


class ServerConfig(BaseModel):
    """Server binding configuration."""

    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT


class LLMConfig(BaseModel):
    """LLM provider configuration."""

    provider: str = DEFAULT_LLM_PROVIDER
    model: str = DEFAULT_LLM_MODEL
    api_key: str = ""
    api_base: str = DEFAULT_LLM_API_BASE


class BehaviorConfig(BaseModel):
    """Runtime behavior toggles."""

    auto_analyze: bool = AUTO_ANALYZE_DEFAULT
    cache_enabled: bool = CACHE_ENABLED_DEFAULT


class SnapfixConfig(BaseModel):
    """Root configuration model."""

    server: ServerConfig = Field(default_factory=ServerConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    behavior: BehaviorConfig = Field(default_factory=BehaviorConfig)


# ── Default TOML content ──────────────────────────────────────────────────────

DEFAULT_CONFIG_TOML: str = f"""\
[server]
host = "{DEFAULT_HOST}"
port = {DEFAULT_PORT}

[llm]
provider = "{DEFAULT_LLM_PROVIDER}"
model    = "{DEFAULT_LLM_MODEL}"
api_key  = ""         # set GEMINI_API_KEY environment variable or enter here
api_base = "{DEFAULT_LLM_API_BASE}"

[behavior]
auto_analyze  = {str(AUTO_ANALYZE_DEFAULT).lower()}
cache_enabled = {str(CACHE_ENABLED_DEFAULT).lower()}
"""


# ── Loader ────────────────────────────────────────────────────────────────────


class ConfigLoader:
    """Loads, validates, and exposes the Snapfix TOML configuration.

    Creates the ``~/.snapfix/`` directory and a default ``config.toml``
    on first run so users have a ready-to-edit template.
    """

    def __init__(self, path: Path = CONFIG_PATH) -> None:
        self._path = path

    def load(self) -> SnapfixConfig:
        """Load config from disk, creating defaults if absent.

        Returns:
            SnapfixConfig: Validated configuration object.
        """
        self._ensure_defaults()
        raw: dict = toml.load(self._path)  # type: ignore[type-arg]
        return SnapfixConfig.model_validate(raw)

    def _ensure_defaults(self) -> None:
        """Create the config directory and file if they do not exist."""
        PYLOGAI_DIR.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._path.write_text(DEFAULT_CONFIG_TOML, encoding="utf-8")


# Module-level singleton — import and call wherever needed.
_loader = ConfigLoader()


def load_config() -> SnapfixConfig:
    """Convenience function to load the global Snapfix config.

    Returns:
        SnapfixConfig: The loaded and validated configuration.
    """
    return _loader.load()
