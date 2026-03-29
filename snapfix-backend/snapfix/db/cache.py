"""
snapfix/db/cache.py

Author: Snapfix Contributors
License: MIT

CacheLayer: async SQLite read/write helpers for the analysis cache.
Uses aiosqlite for non-blocking DB access.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

import aiosqlite

from snapfix.constants import CACHE_DB_PATH
from snapfix.db.models import ALL_DDL

logger = logging.getLogger(__name__)


class CacheLayer:
    """Async SQLite-backed cache for Snapfix Engine analysis results.
    Stores results in a centralized 'analysis_json' column for flexibility.
    """

    def __init__(self, db_path: Path = CACHE_DB_PATH) -> None:
        self._db_path = db_path

    async def initialize(self) -> None:
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self._db_path) as db:
            for ddl in ALL_DDL:
                await db.execute(ddl)
            await db.commit()
        logger.debug("CacheLayer initialised at %s", self._db_path)

    def generate_key(self, traceback: str) -> str:
        """Returns a stable SHA-256 hex digest of the traceback string."""
        return hashlib.sha256(traceback.encode("utf-8")).hexdigest()

    async def get(self, traceback_hash: str) -> dict[str, Any] | None:
        """Look up a cached result by hash. Returns raw dict on hit."""
        async with aiosqlite.connect(self._db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT analysis_json FROM analysis_cache WHERE traceback_hash = ?",
                (traceback_hash,),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            
            try:
                return json.loads(row["analysis_json"])
            except json.JSONDecodeError:
                return None

    async def set(
        self,
        traceback_hash: str,
        analysis_dict: dict[str, Any],
        provider: str = "ollama",
    ) -> int:
        """Insert a result. Existing entries for the same hash are ignored (duplicate analysis)."""
        async with aiosqlite.connect(self._db_path) as db:
            cursor = await db.execute(
                """
                INSERT OR IGNORE INTO analysis_cache (traceback_hash, analysis_json, llm_provider)
                VALUES (?, ?, ?)
                """,
                (traceback_hash, json.dumps(analysis_dict), provider),
            )
            await db.commit()
            return cursor.lastrowid or 0

    async def clear(self) -> None:
        """Clear all tables."""
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute("DELETE FROM analysis_cache")
            await db.execute("DELETE FROM analysis_log")
            await db.commit()

    async def stats(self) -> dict[str, int]:
        async with aiosqlite.connect(self._db_path) as db:
            row = await (await db.execute("SELECT COUNT(*) FROM analysis_cache")).fetchone()
            total_entries = row[0] if row else 0
            
            log_row = await (await db.execute("SELECT COUNT(*) FROM analysis_log")).fetchone()
            total_requests = log_row[0] if log_row else 0

        return {
            "total_entries": total_entries,
            "total_hits": 0, # Simplified hit logic for now
            "total_requests": total_requests,
        }
