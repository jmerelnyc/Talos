"""Shared helpers for setup handlers: safe writes with backups."""
from __future__ import annotations

import shutil
from pathlib import Path


def write_with_backup(path: Path, content: str, dry_run: bool = False) -> str:
    """Write `content` to `path`, backing up any existing file to `<path>.bak` first.

    Returns a short human-readable summary of what happened, or would happen.
    """
    path = Path(path)
    existed = path.exists()

    if dry_run:
        action = "update" if existed else "create"
        return f"[dry run] would {action} {path}\n---\n{content}"

    path.parent.mkdir(parents=True, exist_ok=True)
    if existed:
        backup = path.with_name(path.name + ".bak")
        shutil.copy2(path, backup)
        path.write_text(content, encoding="utf-8")
        return f"updated {path} (backup at {backup})"

    path.write_text(content, encoding="utf-8")
    return f"created {path}"
