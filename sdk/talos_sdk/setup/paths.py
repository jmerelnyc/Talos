"""Cross-platform paths for the config files each tool reads."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def home() -> Path:
    return Path.home()


def vscode_continue_config() -> Path:
    return home() / ".continue" / "config.json"


def zed_settings() -> Path:
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA", str(home() / "AppData" / "Roaming"))
        return Path(appdata) / "Zed" / "settings.json"
    return home() / ".config" / "zed" / "settings.json"


def aider_conf() -> Path:
    return home() / ".aider.conf.yml"


def claude_code_env() -> Path:
    return home() / ".talos" / "claude-code.env"
