# Claude Code

Claude Code speaks the Anthropic Messages API. The Talos gateway implements an
Anthropic-compatible endpoint (`POST /v1/messages`), so you can point Claude
Code at it with environment variables.

Set these before launching `claude`, or source [`env.sh`](./env.sh) directly:

```bash
export ANTHROPIC_BASE_URL="https://api.talos.ai"
export ANTHROPIC_API_KEY="talos_YOUR_KEY"
# Route Claude Code's model names to talos-auto:
export ANTHROPIC_MODEL="talos-auto"
export ANTHROPIC_SMALL_FAST_MODEL="talos-auto"
```

In development use `export ANTHROPIC_BASE_URL="http://localhost:8080"`.

Notes:

- Do **not** append `/v1` to `ANTHROPIC_BASE_URL`; the client adds
  `/v1/messages` itself.
- The gateway sends the Anthropic streaming event sequence
  (`message_start`, `content_block_delta`, `message_delta`, `message_stop`),
  so streaming works normally.
- The key is passed via the `x-api-key` header, which the gateway accepts in
  addition to `Authorization: Bearer`.

## Quick check

Run [`verify.sh`](./verify.sh) to confirm your key and the gateway work
before launching `claude`:

```bash
export TALOS_API_KEY=talos_YOUR_KEY
bash verify.sh
```

For a runnable client instead of curl, see
[`anthropic_sdk.py`](./anthropic_sdk.py) (same script as `examples/python/`).