# Contributing to talos-worker

Thanks for taking a look. This is the client that lets people share GPU time
with the Talos network, so changes here run on other people's machines,
please keep that in mind.

## Dev setup

```bash
git clone https://github.com/jmerelnyc/Talos.git
cd Talos
pip install -e .
```

Run the fake Ollama server for local testing without a real model:

```bash
python tests/fake_ollama.py
```

Then in another terminal:

```bash
talos-worker status
```

## Code style

- Python 3.9+, type hints, and `from __future__ import annotations` at the
  top of new modules.
- Keep the worker dependency-light; `aiohttp` and `nvidia-ml-py` are the only
  runtime dependencies for a reason.
- GPU and Ollama detection should always degrade gracefully and never raise
  on a machine without an NVIDIA GPU or without Ollama running.

## Reporting issues

Open a GitHub issue with:

- Your OS and Python version
- Output of `talos-worker status`
- Steps to reproduce

## Pull requests

- Keep PRs focused: one change per PR is easier to review than a bundle.
- Add or update a page under `docs/` if you change CLI flags or behavior.
- No breaking changes to the `pair`, `run`, or `status` command surface
  without discussion first, since existing installs depend on it.