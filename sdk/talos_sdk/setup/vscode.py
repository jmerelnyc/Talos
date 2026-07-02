"""Auto-configure the Continue VS Code extension to use talos-auto."""
from __future__ import annotations

import json

from ..config import DEFAULT_BASE_URL, DEFAULT_MODEL
from .common import write_with_backup
from .paths import vscode_continue_config

TITLE = "talos-auto"


def setup(
    api_key: str,
    base_url: str = DEFAULT_BASE_URL,
    model: str = DEFAULT_MODEL,
    dry_run: bool = False,
) -> str:
    path = vscode_continue_config()

    data: dict = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
    data.setdefault("models", [])

    entry = {
        "title": TITLE,
        "provider": "openai",
        "model": model,
        "apiBase": base_url,
        "apiKey": api_key,
    }
    data["models"] = [m for m in data["models"] if m.get("title") != TITLE] + [entry]

    content = json.dumps(data, indent=2) + "\n"
    result = write_with_backup(path, content, dry_run=dry_run)
    return result + f"\nPick '{TITLE}' as the model in Continue's chat panel."
