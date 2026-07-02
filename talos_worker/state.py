"""Shared runtime state for the running worker (read by the local dashboard)."""
from __future__ import annotations

import time
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
    started_at: float = field(default_factory=time.time)

    @property
    def uptime_seconds(self) -> int:
        return int(time.time() - self.started_at)

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
            "uptimeSeconds": self.uptime_seconds,
        }