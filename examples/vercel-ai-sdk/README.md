# Vercel AI SDK example

```bash
npm install
export TALOS_API_KEY=talos_YOUR_KEY
npx tsx index.ts
```

Uses `talos.chat(model)` rather than the default `talos(model)` factory,
since the gateway implements Chat Completions rather than the OpenAI
Responses API. Reads `TALOS_BASE_URL` and `TALOS_MODEL` too; see the
top-level [`examples/README.md`](../README.md) for defaults.