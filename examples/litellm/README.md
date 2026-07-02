# LiteLLM proxy

Routes any LiteLLM-compatible client (or the OpenAI SDK pointed at the local
proxy) through the Talos gateway.

```bash
pip install "litellm[proxy]"
export TALOS_API_KEY=talos_YOUR_KEY
litellm --config config.yaml
```

This starts a local proxy at `http://localhost:4000`. Point any OpenAI client
at it:

```bash
curl http://localhost:4000/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"talos-auto","messages":[{"role":"user","content":"Say hi"}]}'
```

Add more open models by copying the `talos-llama-3.1-8b` block in
[`config.yaml`](./config.yaml) with a different `model_name`.