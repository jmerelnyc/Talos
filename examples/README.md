# Examples

Small, runnable scripts that call the live Talos gateway with official SDKs.
These hit the hosted API directly, the same way any other OpenAI- or
Anthropic-compatible client would; none of this talks to your local worker.

All examples read the API key from `TALOS_API_KEY`. Create one on your
[dashboard](https://talos.ai/dashboard).

| Folder | Stack |
| --- | --- |
| [`python/`](./python) | Official `openai` and `anthropic` Python SDKs |
| [`node/`](./node) | Official `openai` Node.js SDK |
| [`go/`](./go) | Community `go-openai` client |
| [`vercel-ai-sdk/`](./vercel-ai-sdk) | Vercel AI SDK (`ai` + `@ai-sdk/openai`) |
| [`litellm/`](./litellm) | LiteLLM proxy config, for any LiteLLM-compatible client |

Each folder has its own README with exact install and run steps.

## Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `TALOS_API_KEY` | (required) | Your Talos gateway key |
| `TALOS_BASE_URL` | `https://api.talos.ai/v1` (`https://api.talos.ai` for the Anthropic example) | Override for local development |
| `TALOS_MODEL` | `talos-auto` | Swap in an open model, e.g. `talos-llama-3.1-8b` |