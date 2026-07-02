"""Local inference via Ollama's HTTP API (streaming chat + model listing)."""
from __future__ import annotations

from typing import List

import aiohttp


async def list_models(session: aiohttp.ClientSession, ollama_url: str) -> List[str]:
    """Returns the model tags installed in the local Ollama (e.g. llama3.1:8b)."""
    try:
        async with session.get(f"{ollama_url.rstrip('/')}/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []