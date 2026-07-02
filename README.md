# Talos worker

Share your GPU with the Talos network and earn. This is the downloadable
client (intended to live in its own public GitHub repo, `talos-worker`). It
pairs with your Talos account using a code, then serves open-model inference
jobs from the network via your local [Ollama](https://ollama.com), reporting
uptime and earning a share of real usage revenue.

The Talos web app never imports this repo. The two only talk over the network:
a device code to pair, then jobs and heartbeats over a WebSocket.

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com) running locally with at least one model pulled,
  e.g. `ollama pull llama3.1:8b`
- NVIDIA GPU recommended (detected automatically; CPU also works)

## Install

```bash
pip install -e .
```

## Pair

Get a code from your dashboard (Pair a device), then:

```bash
talos-worker pair            # prompts for the code
# or non-interactively:
talos-worker pair --code TALOS-XXXX-XXXX --server https://api.talos.ai
```

## Run

```bash
talos-worker run --allocation 0.5
```

- Opens a local dashboard at http://127.0.0.1:8674 with live status and a power
  (allocation) slider.
- `--allocation 0..1` sets how much of the machine you offer. It maps to
  concurrency/duty-cycle, not a literal power percentage.
- Uptime accrues while connected; earnings are credited per served job and
  visible on your Talos dashboard.

## Commands

| Command | Description |
| --- | --- |
| `talos-worker pair` | Pair this machine with a code |
| `talos-worker run` | Connect and serve inference jobs |
| `talos-worker status` | Show config, GPU and available models |

## Using talos-auto in your editor

See [`docs/`](./docs) for Cursor, VS Code (Continue/Cline), Claude Code,
JetBrains AI Assistant, Zed and Aider setup. For runnable SDK scripts, see
[`examples/`](./examples).

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).