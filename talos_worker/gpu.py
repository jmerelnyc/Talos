"""GPU detection via NVIDIA's NVML. Degrades gracefully when unavailable."""
from __future__ import annotations

from typing import Optional, TypedDict


class GpuInfo(TypedDict):
    name: str
    vramMb: int


def detect_gpu() -> Optional[GpuInfo]:
    """Returns the primary NVIDIA GPU, or None if none / NVML is unavailable."""
    try:
        import pynvml  # provided by the nvidia-ml-py package
    except Exception:
        return None

    try:
        pynvml.nvmlInit()
    except Exception:
        return None

    try:
        count = pynvml.nvmlDeviceGetCount()
        if count == 0:
            return None
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        name = pynvml.nvmlDeviceGetName(handle)
        if isinstance(name, bytes):
            name = name.decode()
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return {"name": name, "vramMb": int(mem.total // (1024 * 1024))}
    except Exception:
        return None