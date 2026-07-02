"""WebSocket client: registers with the gateway, sends heartbeats, and serves
inference jobs from the scheduler by streaming tokens from local Ollama."""
from __future__ import annotations

import asyncio
import json

import aiohttp

from .config import WorkerConfig
from .inference import list_models
from .state import RuntimeState


async def _heartbeat(ws: aiohttp.ClientWebSocketResponse, state: RuntimeState, interval: float) -> None:
    while True:
        await asyncio.sleep(interval)
        await ws.send_json(
            {"type": "heartbeat", "allocation": state.allocation, "busy": state.jobs_active > 0}
        )


async def _connect_once(config: WorkerConfig, state: RuntimeState) -> None:
    async with aiohttp.ClientSession() as session:
        models = await list_models(session, config.ollama)
        state.models = models

        async with session.ws_connect(config.ws_url, heartbeat=30) as ws:
            await ws.send_json(
                {
                    "type": "register",
                    "name": config.name,
                    "gpu": {"name": state.gpu_name, "vramMb": state.vram_mb}
                    if state.gpu_name
                    else None,
                    "models": models,
                }
            )
            state.connected = True
            print(f"[talos] connected to {config.server} as worker {config.worker_id}")
            print(f"[talos] serving models: {', '.join(models) or '(none - install some in Ollama)'}")

            hb_task: asyncio.Task | None = None

            try:
                async for msg in ws:
                    if msg.type != aiohttp.WSMsgType.TEXT:
                        continue
                    data = json.loads(msg.data)
                    kind = data.get("type")

                    if kind == "welcome":
                        interval = max(5.0, data.get("heartbeatIntervalMs", 15000) / 1000)
                        hb_task = asyncio.create_task(_heartbeat(ws, state, interval))
            finally:
                state.connected = False
                if hb_task:
                    hb_task.cancel()