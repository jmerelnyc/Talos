"""JetBrains AI Assistant's third-party provider settings live in the IDE,
not a plain config file, so this prints the exact values instead.
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
        "JetBrains AI Assistant has no plain config file for this, so it's a manual step:\n\n"
        "1. Settings -> Tools -> AI Assistant -> Models -> Third-party AI providers\n"
        "2. Add a custom OpenAI-compatible service with:\n"
        f"   URL: {base_url}\n"
        f"   API key: {api_key}\n"
        f"   Model name: {model}\n"
        "3. Apply, then pick the new provider in the AI Assistant chat dropdown\n\n"
        "See jetbrains/README.md for details."
    )
