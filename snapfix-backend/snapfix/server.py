"""
snapfix/server.py

Author: Snapfix Contributors
License: MIT

FastAPI server for Snapfix Engine.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from snapfix.config import load_config
from snapfix.db.cache import CacheLayer
from snapfix.llm.handler import LLMHandler
from snapfix.parser.traceback import TracebackParser

app = FastAPI(
    title="Snapfix Engine API",
    description="Analysis engine for Python exceptions.",
    version="0.2.0",
)

# Initialize singletons
config = load_config()
_cache = CacheLayer()
_llm = LLMHandler(config)
_parser = TracebackParser()


class AnalyzeRequest(BaseModel):
    """Input payload for POST /analyze."""
    traceback: str = Field(..., description="The raw Python traceback string.")
    context: str = Field("python", description="Language of the log.")
    session_id: str | None = None
    project_path: str | None = None


class AnalyzeResponse(BaseModel):
    """Output payload for POST /analyze (Snapfix structure)."""
    what_happened: dict[str, str]
    fix: dict[str, str]
    stack_frames: list[dict[str, Any]]
    prevention: dict[str, str]
    docs: dict[str, str]
    meta: dict[str, Any]
    cached: bool = False


@app.on_event("startup")
async def startup() -> None:
    """Initialize resources on server start."""
    await _cache.initialize()


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "engine": "Snapfix"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze a Python traceback and return a structured Snapfix report."""
    config = load_config()

    # 1. Hashing and caching check
    cache_key = _cache.generate_key(payload.traceback)
    if config.behavior.cache_enabled:
        cached_result = await _cache.get(cache_key)
        if cached_result:
            # We assume cached result was already in the new format
            return AnalyzeResponse(**cached_result, cached=True)

    # 2. Parse the traceback to extract frames
    parsed = _parser.parse(payload.traceback)
    if not parsed or not parsed.error_type:
        raise HTTPException(status_code=400, detail="Could not detect valid Python traceback structure.")

    # 3. Request analysis from AI
    try:
        response_dict = await _llm.analyze(
            traceback=payload.traceback,
            parsed_data=parsed,
            project_path=payload.project_path,
        )
    except Exception as e:
        logging.error(f"LLM analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    # 4. Persistence
    if config.behavior.cache_enabled:
        await _cache.set(cache_key, response_dict)

    return AnalyzeResponse(**response_dict, cached=False)


@app.post("/cache/clear")
async def clear_cache() -> dict[str, bool]:
    """Clear all cached analyses."""
    await _cache.clear()
    return {"success": True}
