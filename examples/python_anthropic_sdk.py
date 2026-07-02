"""Example: call the Talos gateway with the official Anthropic Python SDK.

The gateway implements POST /v1/messages, so any Anthropic client works by
pointing base_url at the Talos host (no /v1 suffix; the SDK adds it).

Install:
    pip install anthropic

Run:
    export TALOS_API_KEY=talos_YOUR_KEY
    python python_anthropic_sdk.py
"""
from __future__ import annotations

import os
import sys

from anthropic import Anthropic

BASE_URL = os.environ.get("TALOS_BASE_URL", "https://api.talos.ai")
MODEL = os.environ.get("TALOS_MODEL", "talos-auto")


def main() -> None:
    api_key = os.environ.get("TALOS_API_KEY")
    if not api_key:
        sys.exit("Set TALOS_API_KEY to a key from your Talos dashboard.")

    client = Anthropic(api_key=api_key, base_url=BASE_URL)

    with client.messages.stream(
        model=MODEL,
        max_tokens=128,
        messages=[{"role": "user", "content": "Say hi in five words or fewer."}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print()


if __name__ == "__main__":
    main()