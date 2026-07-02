"""WebSocket client: registers with the gateway, sends heartbeats, and serves
inference jobs from the scheduler by streaming tokens from local Ollama."""
from __future__ import annotations

import asyncio
import contextlib
import json
from typing import Dict

import aiohttp

from .config import WorkerConfig
from .dashboard import start_dashboard
from .gpu import detect_gpu
from .inference import list_models, stream_chat
from .state import RuntimeState


async def _run_job(ws: aiohttp.ClientWebSocketResponse, session: aiohttp.ClientSession,
                   ollama: str, state: RuntimeState, job: dict) -> None:
    job_id = job["jobId"]
    usage: Dict[str, int] = {"prompt": 0, "completion": 0}
    state.jobs_active += 1
    try:
        async for delta in stream_chat(session, ollama, job["model"], job["messages"], usage):
            await ws.send_json({"type": "job_chunk", "jobId": job_id, "delta": delta})
        await ws.send_json(
            {
                "type": "job_done",
                "jobId": job_id,
                "promptTokens": usage["prompt"],
                "completionTokens": usage["completion"],
            }
        )
        state.jobs_handled += 1
        state.tokens_served += usage["prompt"] + usage["completion"]
    except asyncio.CancelledError:
        with contextlib.suppress(Exception):
            await ws.send_json({"type": "job_error", "jobId": job_id, "message": "cancelled"})
        raise
    except Exception as exc:  # noqa: BLE001 - report any inference failure upstream
        with contextlib.suppress(Exception):
            await ws.send_json({"type": "job_error", "jobId": job_id, "message": str(exc)})
    finally:
        state.jobs_active = max(0, state.jobs_active - 1)


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
            jobs: Dict[str, asyncio.Task] = {}

            try:
                async for msg in ws:
                    if msg.type != aiohttp.WSMsgType.TEXT:
                        continue
                    data = json.loads(msg.data)
                    kind = data.get("type")

                    if kind == "welcome":
                        interval = max(5.0, data.get("heartbeatIntervalMs", 15000) / 1000)
                        hb_task = asyncio.create_task(_heartbeat(ws, state, interval))
                    elif kind == "job":
                        task = asyncio.create_task(_run_job(ws, session, config.ollama, state, data))
                        jobs[data["jobId"]] = task
                        task.add_done_callback(lambda t, jid=data["jobId"]: jobs.pop(jid, None))
                    elif kind == "job_cancel":
                        t = jobs.get(data.get("jobId"))
                        if t:
                            t.cancel()
            finally:
                state.connected = False
                if hb_task:
                    hb_task.cancel()
                for t in jobs.values():
                    t.cancel()


async def run_worker(config: WorkerConfig, dashboard_port: int | None) -> None:
    if not config.token:
        raise SystemExit("Not paired. Run `talos-worker pair` first.")

    gpu = detect_gpu()
    state = RuntimeState(
        server=config.server,
        worker_id=config.worker_id,
        allocation=config.allocation,
        gpu_name=gpu["name"] if gpu else None,
        vram_mb=gpu["vramMb"] if gpu else None,
    )

    runner = None
    if dashboard_port:
        runner = await start_dashboard(state, dashboard_port)
        print(f"[talos] local dashboard at http://127.0.0.1:{dashboard_port}")

    backoff = 1.0
    try:
        while True:
            try:
                await _connect_once(config, state)
                backoff = 1.0  # clean disconnect: reset backoff
                print("[talos] disconnected, reconnecting...")
            except (aiohttp.ClientError, OSError) as exc:
                print(f"[talos] connection error: {exc}; retrying in {backoff:.0f}s")
                await asyncio.sleep(backoff)
                backoff = min(30.0, backoff * 2)
    except asyncio.CancelledError:
        pass
    finally:
        if runner:
            await runner.cleanup()