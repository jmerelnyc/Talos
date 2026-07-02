"""Shared runtime state for the running worker (read by the local dashboard)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RuntimeState:
    server: str = ""
    worker_id: Optional[str] = None
    gpu_name: Optional[str] = None
    vram_mb: Optional[int] = None
    models: List[str] = field(default_factory=list)
    allocation: float = 0.5
    connected: bool = False
    jobs_active: int = 0
    jobs_handled: int = 0
    tokens_served: int = 0

    def snapshot(self) -> dict:
        return {
            "server": self.server,
            "workerId": self.worker_id,
            "gpu": self.gpu_name,
            "vramMb": self.vram_mb,
            "models": self.models,
            "allocation": self.allocation,
            "connected": self.connected,
            "jobsActive": self.jobs_active,
            "jobsHandled": self.jobs_handled,
            "tokensServed": self.tokens_served,
        }