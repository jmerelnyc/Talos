"""Auto-configure aider's config file to use talos-auto.

Aider's config file is just flat `key: value` lines, so this parses and
rewrites only that subset instead of pulling in a full YAML dependency.
"""
from __future__ import annotations

from ..config import DEFAULT_BASE_URL, DEFAULT_MODEL
from .common import write_with_backup
from .paths import aider_conf


def _parse_flat_yaml(text: str) -> dict:
    result: dict = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        result[key.strip()] = value.strip()
    return result


def setup(
    api_key: str,
    base_url: str = DEFAULT_BASE_URL,
    model: str = DEFAULT_MODEL,
    dry_run: bool = False,
) -> str:
    path = aider_conf()
    data = _parse_flat_yaml(path.read_text(encoding="utf-8")) if path.exists() else {}

    data["openai-api-base"] = base_url
    data["openai-api-key"] = api_key
    data["model"] = f"openai/{model}"

    content = "\n".join(f"{key}: {value}" for key, value in data.items()) + "\n"
    return write_with_backup(path, content, dry_run=dry_run)
