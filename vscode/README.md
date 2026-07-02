# VS Code (Continue / Cline)

Both extensions accept an OpenAI-compatible provider.

## Continue

Edit `~/.continue/config.json` (or use the "Open config" command) and add the
model block from [`continue.config.json`](./continue.config.json):

```json
{
  "models": [
    {
      "title": "talos-auto",
      "provider": "openai",
      "model": "talos-auto",
      "apiBase": "https://api.talos.ai/v1",
      "apiKey": "talos_YOUR_KEY"
    }
  ]
}
```

For development use `"apiBase": "http://localhost:8080/v1"`.

## Cline

1. Open Cline settings -> **API Provider**: choose **OpenAI Compatible**.
2. **Base URL**: `https://api.talos.ai/v1`
3. **API Key**: `talos_YOUR_KEY`
4. **Model ID**: `talos-auto` (or `talos-llama-3.1-8b`).

Both extensions use streaming `chat/completions`, which the gateway supports.