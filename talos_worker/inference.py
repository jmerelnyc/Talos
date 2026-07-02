"""Local inference via Ollama's HTTP API (streaming chat + model listing)."""
from __future__ import annotations

import json
from typing import AsyncGenerator, Dict, List

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


async def stream_chat(
    session: aiohttp.ClientSession,
    ollama_url: str,
    model: str,
    messages: List[Dict[str, str]],
    usage_out: Dict[str, int],
) -> AsyncGenerator[str, None]:
    """
    Streams assistant token deltas from Ollama's /api/chat. Fills usage_out with
    {"prompt": n, "completion": m} from the final message. Raises on HTTP error.
    """
    payload = {"model": model, "messages": messages, "stream": True}
    url = f"{ollama_url.rstrip('/')}/api/chat"

    async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=None)) as resp:
        if resp.status != 200:
            detail = await resp.text()
            raise RuntimeError(f"ollama {resp.status}: {detail[:200]}")

        async for line in resp.content:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            if "error" in obj:
                raise RuntimeError(str(obj["error"]))

            delta = obj.get("message", {}).get("content", "")
            if delta:
                yield delta

            if obj.get("done"):
                usage_out["prompt"] = int(obj.get("prompt_eval_count", 0) or 0)
                usage_out["completion"] = int(obj.get("eval_count", 0) or 0)
                break