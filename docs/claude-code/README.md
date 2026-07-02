# Claude Code

Claude Code speaks the Anthropic Messages API. The Talos gateway implements an
Anthropic-compatible endpoint (`POST /v1/messages`), so you can point Claude
Code at it with environment variables.

Set these before launching `claude`:

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

```bash
curl "$ANTHROPIC_BASE_URL/v1/messages" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"talos-auto","max_tokens":128,"messages":[{"role":"user","content":"Say hi"}]}'
```