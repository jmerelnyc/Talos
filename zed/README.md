# Zed

Zed's assistant panel supports OpenAI-compatible providers through
`settings.json`.

Open **Zed -> Settings -> Open Settings** and merge in the block from
[`settings.json`](./settings.json):

```json
{
  "language_models": {
    "openai": {
      "api_url": "https://api.usetalos.xyz/v1",
      "available_models": [
        {
          "name": "talos-auto",
          "display_name": "Talos Auto",
          "max_tokens": 128000
        }
      ]
    }
  }
}
```

Zed asks for the API key the first time you use the OpenAI provider; paste
your Talos key (`talos_...`). Then open the assistant panel and pick
`talos-auto` from the model dropdown.

For local development, point `api_url` at `http://localhost:8080/v1`.

Notes:

- Zed also accepts the key via the `OPENAI_API_KEY` environment variable set
  before launching the editor.

## Quick check

Run [`verify.sh`](./verify.sh) to confirm your key and the gateway work
before merging the settings block:

```bash
export TALOS_API_KEY=talos_YOUR_KEY
bash verify.sh
```

For a runnable client instead of curl, see [`openai_sdk.py`](./openai_sdk.py)
(same script as `examples/python/`).