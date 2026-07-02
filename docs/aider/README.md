# Aider

Aider treats any OpenAI-compatible endpoint as a normal model through
environment variables.

```bash
export OPENAI_API_BASE="https://api.talos.ai/v1"
export OPENAI_API_KEY="talos_YOUR_KEY"
aider --model openai/talos-auto
```

For local development, point `OPENAI_API_BASE` at `http://localhost:8080/v1`.

You can also copy [`.aider.conf.yml`](./.aider.conf.yml) into your project or
home directory:

```yaml
openai-api-base: https://api.talos.ai/v1
openai-api-key: talos_YOUR_KEY
model: openai/talos-auto
```

Notes:

- Aider streams `chat/completions`, which the gateway supports.
- If Aider reports an auth error, confirm the key is active on your dashboard.

## Quick check

```bash
aider --model openai/talos-auto --message "Say hi"
```