"""Example: call the Talos gateway with the official OpenAI Python SDK.

The gateway speaks standard OpenAI `chat/completions`, so the official SDK
works unmodified, pointed at the Talos base URL.

Install:
    pip install openai

Run:
    export TALOS_API_KEY=talos_YOUR_KEY
    python python_openai_sdk.py
"""
from __future__ import annotations

import os
import sys

from openai import OpenAI

BASE_URL = os.environ.get("TALOS_BASE_URL", "https://api.talos.ai/v1")
MODEL = os.environ.get("TALOS_MODEL", "talos-auto")


def main() -> None:
    api_key = os.environ.get("TALOS_API_KEY")
    if not api_key:
        sys.exit("TALOS_API_KEY is not set. Create a key on your Talos dashboard and export it.")

    client = OpenAI(api_key=api_key, base_url=BASE_URL)

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Say hi in five words or fewer."}],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)
    print()


if __name__ == "__main__":
    main()