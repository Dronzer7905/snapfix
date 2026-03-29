"""
snapfix/db/models.py

Author: Snapfix Contributors
License: MIT

SQLite table DDL definitions for Snapfix's cache database.
"""

# ── DDL statements ────────────────────────────────────────────────────────────

CREATE_ANALYSIS_CACHE_SQL: str = """
CREATE TABLE IF NOT EXISTS analysis_cache (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    traceback_hash  TEXT    UNIQUE NOT NULL,
    analysis_json   TEXT    NOT NULL, -- Full Snapfix JSON response
    llm_provider    TEXT    NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    hit_count       INTEGER  DEFAULT 0
);
"""

CREATE_ANALYSIS_LOG_SQL: str = """
CREATE TABLE IF NOT EXISTS analysis_log (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id   TEXT    NOT NULL,
    cache_id     INTEGER REFERENCES analysis_cache(id),
    project_path TEXT,
    triggered_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

# Index for fast hash lookups
CREATE_HASH_INDEX_SQL: str = """
CREATE UNIQUE INDEX IF NOT EXISTS idx_traceback_hash
ON analysis_cache (traceback_hash);
"""

# All DDL in execution order
ALL_DDL: list[str] = [
    CREATE_ANALYSIS_CACHE_SQL,
    CREATE_ANALYSIS_LOG_SQL,
    CREATE_HASH_INDEX_SQL,
]
