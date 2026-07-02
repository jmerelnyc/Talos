# Using talos-auto in your coding tools

The Talos gateway is OpenAI- and Anthropic-compatible, so most AI coding tools
can use it by setting a base URL, an API key, and a model name.

- Base URL (OpenAI clients): `https://api.talos.ai/v1` (or your own server, e.g.
  `http://localhost:8080/v1` in development)
- API key: create one on your [dashboard](https://talos.ai/dashboard); it looks
  like `talos_...`
- Model: `talos-auto` (auto-routing), or an open model such as
  `talos-llama-3.1-8b`

`talos-auto` is a routing model: it forwards to the best available backend. Open
`talos-*` models are served by the community GPU pool.

Guides:

- [Cursor](./cursor.md)
- [VS Code (Continue / Cline)](./vscode.md)
- [Claude Code](./claude-code.md)

## Quick check

```bash
curl https://api.talos.ai/v1/chat/completions \
  -H "Authorization: Bearer talos_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"talos-auto","messages":[{"role":"user","content":"Say hi"}]}'
```