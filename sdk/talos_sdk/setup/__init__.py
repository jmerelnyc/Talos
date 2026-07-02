"""Per-tool setup handlers, registered by name for the `talos setup` CLI."""
from __future__ import annotations

from . import aider, claude_code, cursor, jetbrains, vscode, zed

HANDLERS = {
    "cursor": cursor.setup,
    "vscode": vscode.setup,
    "claude-code": claude_code.setup,
    "jetbrains": jetbrains.setup,
    "zed": zed.setup,
    "aider": aider.setup,
}

__all__ = ["HANDLERS"]
