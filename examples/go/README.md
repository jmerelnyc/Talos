# Go example

Uses the community [go-openai](https://github.com/sashabaranov/go-openai)
client, pointed at the Talos gateway.

```bash
export TALOS_API_KEY=talos_YOUR_KEY
go run main.go
```

Reads `TALOS_BASE_URL` and `TALOS_MODEL` too; see the top-level
[`examples/README.md`](../README.md) for defaults.