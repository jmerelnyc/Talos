"""Cursor's model override lives in Settings, not a plain config file, so
there is nothing safe to auto-write. This prints the exact values instead.
"""
from __future__ import annotations

from ..config import DEFAULT_BASE_URL, DEFAULT_MODEL


def setup(
    api_key: str,
    base_url: str = DEFAULT_BASE_URL,
    model: str = DEFAULT_MODEL,
    dry_run: bool = False,
) -> str:
    return (
        "Cursor has no plain config file for this, so it's a manual step:\n\n"
        "1. Settings -> Models -> OpenAI API Key -> paste your key below\n"
        f"2. Enable 'Override OpenAI Base URL' -> {base_url}\n"
        f"3. Add a custom model named exactly: {model}\n"
        "4. Click Verify, then pick it in the chat model picker\n\n"
        f"Your key: {api_key}\n\n"
        "See cursor/README.md for details and screenshots-in-words."
    )
