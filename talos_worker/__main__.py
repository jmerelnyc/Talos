"""Talos worker CLI: pair | run | status."""
from __future__ import annotations

import argparse
import asyncio

import aiohttp

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


def main() -> None:
    parser = argparse.ArgumentParser(prog="talos-worker", description="Talos GPU worker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_pair = sub.add_parser("pair", help="Pair this machine using a code from the dashboard")
    p_pair.add_argument("--code", help="Pairing code (otherwise prompted)")
    p_pair.add_argument("--server", help="Talos server URL")
    p_pair.add_argument("--ollama", help="Ollama base URL")
    p_pair.add_argument("--name", help="Friendly worker name")
    p_pair.set_defaults(func=_pair)

    args = parser.parse_args()
    asyncio.run(args.func(args))


if __name__ == "__main__":
    main()