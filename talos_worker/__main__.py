"""Talos worker CLI: pair | run | status."""
from __future__ import annotations

import argparse
import asyncio

import aiohttp

from .client import run_worker
from .config import WorkerConfig
from .gpu import detect_gpu
from .inference import list_models
from .pairing import redeem_code


async def _pair(args: argparse.Namespace) -> None:
    config = WorkerConfig.load()
    if args.server:
        config.server = args.server
    if args.ollama:
        config.ollama = args.ollama
    if args.name:
        config.name = args.name

    code = args.code or input("Enter the pairing code from your Talos dashboard: ").strip()
    if not code:
        raise SystemExit("A pairing code is required.")

    gpu = detect_gpu()
    print(f"[talos] detected GPU: {gpu['name'] if gpu else 'none (CPU only)'}")

    async with aiohttp.ClientSession() as session:
        models = await list_models(session, config.ollama)
    print(f"[talos] Ollama models available: {', '.join(models) or '(none)'}")

    result = await redeem_code(config.server, code, config.name, gpu, models)
    config.token = result["workerToken"]
    config.worker_id = result["workerId"]
    config.save()
    print(f"[talos] paired successfully. Worker id: {config.worker_id}")
    print("[talos] start sharing with: talos-worker run")


async def _run(args: argparse.Namespace) -> None:
    config = WorkerConfig.load()
    if args.server:
        config.server = args.server
    if args.allocation is not None:
        config.allocation = args.allocation
        config.save()
    port = None if args.no_dashboard else args.dashboard_port
    await run_worker(config, port)


def main() -> None:
    parser = argparse.ArgumentParser(prog="talos-worker", description="Talos GPU worker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_pair = sub.add_parser("pair", help="Pair this machine using a code from the dashboard")
    p_pair.add_argument("--code", help="Pairing code (otherwise prompted)")
    p_pair.add_argument("--server", help="Talos server URL")
    p_pair.add_argument("--ollama", help="Ollama base URL")
    p_pair.add_argument("--name", help="Friendly worker name")
    p_pair.set_defaults(func=_pair)

    p_run = sub.add_parser("run", help="Connect and start serving inference jobs")
    p_run.add_argument("--server", help="Override server URL")
    p_run.add_argument("--allocation", type=float, help="Power allocation 0..1 (e.g. 0.5)")
    p_run.add_argument("--dashboard-port", type=int, default=8674, help="Local dashboard port")
    p_run.add_argument("--no-dashboard", action="store_true", help="Disable the local dashboard")
    p_run.set_defaults(func=_run)

    args = parser.parse_args()
    asyncio.run(args.func(args))


if __name__ == "__main__":
    main()