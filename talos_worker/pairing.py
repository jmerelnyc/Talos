"""Device-code pairing: exchange a code from the site for a worker token."""
from __future__ import annotations

from typing import List, Optional

import aiohttp

from .gpu import GpuInfo


async def redeem_code(
    server: str,
    code: str,
    name: str,
    gpu: Optional[GpuInfo],
    models: List[str],
) -> dict:
    """Calls POST /pair/redeem. Returns {workerToken, workerId} or raises."""
    url = f"{server.rstrip('/')}/pair/redeem"
    body = {"code": code.strip().upper(), "name": name, "gpu": gpu, "models": models}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, timeout=aiohttp.ClientTimeout(total=15)) as resp:
            data = await resp.json()
            if resp.status != 200:
                msg = data.get("error", {}).get("message", f"HTTP {resp.status}")
                raise RuntimeError(msg)
            return data