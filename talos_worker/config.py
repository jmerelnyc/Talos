"""Persistent worker configuration stored at ~/.talos/worker.json."""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

CONFIG_DIR = Path(os.environ.get("TALOS_HOME", Path.home() / ".talos"))
CONFIG_PATH = CONFIG_DIR / "worker.json"

DEFAULT_SERVER = os.environ.get("TALOS_SERVER", "http://localhost:8080")
DEFAULT_OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")


@dataclass
class WorkerConfig:
    server: str = DEFAULT_SERVER
    ollama: str = DEFAULT_OLLAMA

    def save(self) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(asdict(self), indent=2))
        try:
            os.chmod(CONFIG_PATH, 0o600)
        except OSError:
            pass

    @classmethod
    def load(cls) -> "WorkerConfig":
        if CONFIG_PATH.exists():
            data = json.loads(CONFIG_PATH.read_text())
            known = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
            return cls(**known)
        return cls()