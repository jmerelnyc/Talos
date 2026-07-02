# Examples

Small, runnable scripts that call the live Talos gateway with official SDKs.
These hit the hosted API directly, the same way any other OpenAI- or
Anthropic-compatible client would; none of this talks to your local worker.

All examples read the API key from `TALOS_API_KEY`. Create one on your
[dashboard](https://talos.ai/dashboard).

## Python

```bash
pip install openai anthropic
export TALOS_API_KEY=talos_YOUR_KEY

python python_openai_sdk.py
python python_anthropic_sdk.py
```

## Node.js

```bash
cd examples
npm install
export TALOS_API_KEY=talos_YOUR_KEY

node node_openai_sdk.mjs
```

## Environment variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `TALOS_API_KEY` | (required) | Your Talos gateway key |
| `TALOS_BASE_URL` | `https://api.talos.ai/v1` (`https://api.talos.ai` for the Anthropic example) | Override for local development |
| `TALOS_MODEL` | `talos-auto` | Swap in an open model, e.g. `talos-llama-3.1-8b` |