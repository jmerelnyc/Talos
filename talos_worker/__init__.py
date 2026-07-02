"""Talos GPU worker client.

Pairs a machine with a Talos account using a device code, then connects to the
Talos gateway over a WebSocket to serve open-model inference jobs (via a local
Ollama instance) and report uptime. A small local dashboard exposes power
(allocation) controls.
"""

__version__ = "0.1.0"