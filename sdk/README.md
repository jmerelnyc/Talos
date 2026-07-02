# talos-sdk

For people who just want to **use** the Talos network in their editor or
code, without sharing a GPU. If you want to contribute compute instead, see
the [root README](../README.md) for the `talos-worker` client.

This is a small Python package with two parts:

- A `talos` CLI that auto-configures your editor for `talos-auto` (writes the
  real config file for tools that have one, backs up the original first).
- A `Client` class that wraps the official `openai` SDK with Talos defaults
  baked in, for people coding directly against the gateway.

The manual, copy-paste version of the same setup lives in the per-tool
folders at the repo root ([`cursor/`](../cursor), [`vscode/`](../vscode),
[`claude-code/`](../claude-code), [`jetbrains/`](../jetbrains),
[`zed/`](../zed), [`aider/`](../aider)). This package automates that.

## Install

```bash
git clone https://github.com/jmerelnyc/Talos.git
cd Talos/sdk
pip install -e .
```

## CLI

```bash
export TALOS_API_KEY=talos_YOUR_KEY

talos setup list          # see supported tools
talos setup vscode        # merges Continue's config.json, backs up the original
talos setup zed --dry-run # preview the change without writing anything
talos doctor              # confirm your key and the gateway actually work
```

| Tool | What `talos setup <tool>` does |
| --- | --- |
| `vscode` | Merges a `talos-auto` model into Continue's `config.json` |
| `zed` | Merges the OpenAI provider block into Zed's `settings.json` |
| `aider` | Writes `openai-api-base` / `openai-api-key` / `model` into `.aider.conf.yml` |
| `claude-code` | Writes a sourceable env file (`~/.talos/claude-code.env`) |
| `cursor` | Prints the exact values to paste (no plain config file to write) |
| `jetbrains` | Prints the exact values to paste (no plain config file to write) |

Anything that gets edited is backed up first as `<file>.bak`. Pass
`--dry-run` on any `setup` call to see what would change without writing.

Flags available on every command: `--api-key`, `--base-url`, `--model`. All
three fall back to `TALOS_API_KEY`, `TALOS_BASE_URL`, and `TALOS_MODEL` if
omitted, and otherwise fall back to the hosted gateway and `talos-auto`.

## Client

```python
from talos_sdk import Client

client = Client()  # reads TALOS_API_KEY from the environment
print(client.ask("Say hi in five words or fewer."))

for chunk in client.stream("Write a haiku about idle GPUs."):
    print(chunk, end="", flush=True)

# Escape hatch: the full openai chat namespace, unmodified.
client.chat.completions.create(model=client.model, messages=[...])
```

For raw, un-wrapped SDK usage (Python, Node.js, Go, Vercel AI SDK, LiteLLM),
see [`../examples/`](../examples) instead.

## Development

```bash
pip install -e ".[dev]"
pytest
```
