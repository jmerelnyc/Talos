"""Persistent worker configuration."""
from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_SERVER = os.environ.get("TALOS_SERVER", "http://localhost:8080")
DEFAULT_OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")


@dataclass
class WorkerConfig:
    server: str = DEFAULT_SERVER
    ollama: str = DEFAULT_OLLAMA