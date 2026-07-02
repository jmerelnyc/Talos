"""Auto-configure Zed's OpenAI provider to use talos-auto.

Zed still asks for the API key interactively the first time you use the
provider (or reads OPENAI_API_KEY), so this only merges the URL and model
into settings.json.
"""
from __future__ import annotations

import json

from ..config import DEFAULT_BASE_URL, DEFAULT_MODEL
from .common import write_with_backup
from .paths import zed_settings


def setup(
    api_key: str,
    base_url: str = DEFAULT_BASE_URL,
    model: str = DEFAULT_MODEL,
    dry_run: bool = False,
) -> str:
    path = zed_settings()

    data: dict = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}

    language_models = data.setdefault("language_models", {})
    openai_cfg = language_models.setdefault("openai", {})
    openai_cfg["api_url"] = base_url

    models = [m for m in openai_cfg.get("available_models", []) if m.get("name") != model]
    models.append({"name": model, "display_name": "Talos Auto", "max_tokens": 128000})
    openai_cfg["available_models"] = models

    content = json.dumps(data, indent=2) + "\n"
    result = write_with_backup(path, content, dry_run=dry_run)
    return (
        result
        + f"\nZed will prompt for your key the first time you use the OpenAI provider "
        + f"(or export OPENAI_API_KEY={api_key[:8]}... before launching Zed)."
    )
