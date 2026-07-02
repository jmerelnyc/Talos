"""talos-sdk command line interface.

    talos setup list         List supported tools
    talos setup <tool>       Configure an editor to use talos-auto
    talos doctor             Check that your key and the gateway work
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Sequence

from .config import DEFAULT_BASE_URL, DEFAULT_MODEL, resolve_api_key, resolve_base_url, resolve_model
from .setup import HANDLERS


def _cmd_setup(args: argparse.Namespace) -> int:
    if args.tool == "list":
        print("Supported tools:")
        for name in sorted(HANDLERS):
            print(f"  - {name}")
        return 0

    handler = HANDLERS.get(args.tool)
    if handler is None:
        print(f"Unknown tool '{args.tool}'. Run `talos setup list` to see supported tools.", file=sys.stderr)
        return 1

    try:
        api_key = resolve_api_key(args.api_key)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1

    model = resolve_model(args.model)

    # Each handler has its own correct default base URL (OpenAI- vs
    # Anthropic-shaped), so only override it if the user passed one.
    kwargs = {"api_key": api_key, "model": model, "dry_run": args.dry_run}
    if args.base_url:
        kwargs["base_url"] = args.base_url

    result = handler(**kwargs)
    print(result)
    return 0


def _cmd_doctor(args: argparse.Namespace) -> int:
    try:
        api_key = resolve_api_key(args.api_key)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1

    base_url = resolve_base_url(args.base_url)
    model = resolve_model(args.model)

    payload = json.dumps(
        {"model": model, "messages": [{"role": "user", "content": "Say hi in five words or fewer."}]}
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(f"Gateway returned {exc.code}: {exc.read().decode('utf-8', 'replace')}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Could not reach {base_url}: {exc.reason}", file=sys.stderr)
        return 1

    reply = body.get("choices", [{}])[0].get("message", {}).get("content", "")
    print(f"OK: {model} replied: {reply.strip()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="talos",
        description="Use the Talos network (talos-auto) from your editor or Python.",
    )
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--api-key", default=None, help="Defaults to the TALOS_API_KEY environment variable.")
    common.add_argument("--base-url", default=None, help=f"Defaults to {DEFAULT_BASE_URL}.")
    common.add_argument("--model", default=None, help=f"Defaults to {DEFAULT_MODEL}.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_parser = subparsers.add_parser("setup", parents=[common], help="Configure an editor to use talos-auto")
    setup_parser.add_argument("tool", help="cursor, vscode, claude-code, jetbrains, zed, aider, or list")
    setup_parser.add_argument("--dry-run", action="store_true", help="Print what would change without writing files")
    setup_parser.set_defaults(func=_cmd_setup)

    doctor_parser = subparsers.add_parser("doctor", parents=[common], help="Check that your key and the gateway work")
    doctor_parser.set_defaults(func=_cmd_doctor)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
